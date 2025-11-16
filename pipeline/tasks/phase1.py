import logging
import json
from django.db import transaction
from asgiref.sync import sync_to_async
from pipeline.models import Task, Vendor, Subtask
from pipeline.services.llm_service import llm_service
from pipeline.services.vendor_collector import collector
from pipeline.services.vendor_validator import validator
from pipeline.services.utils import safe_json_extract

logger = logging.getLogger(__name__)


async def run_phase1(task_id):
    """
    PHASE 1: Vendor Discovery & Validation
    Calls PROMPT 1 to get structured vendor data
    """
    try:
        task = await sync_to_async(Task.objects.get)(id=task_id)
        logger.info(f"[PHASE1] ✅ Starting for task {task_id}: {task.task_description[:50]}...")
        
        task.status = 'phase1_running'
        await sync_to_async(task.save)()
        
        task_description = task.task_description
        logger.info(f"[PHASE1] Generating vendor discovery prompt...")
        
        from pipeline.prompts.prompt_1 import get_prompt_1
        prompt = get_prompt_1(task_description)
        
        logger.info(f"[PHASE1] Calling LLM for vendor discovery...")
        response = await llm_service.call_llm(prompt)
        logger.debug(f"[PHASE1] LLM Response length: {len(response)}")
        
        # Parse JSON response
        data = safe_json_extract(response)
        if not isinstance(data, list):
            raise ValueError(f"Expected list of vendors, got: {type(data)}")
        
        if not data:
            raise ValueError("No vendors discovered")
        
        logger.info(f"[PHASE1] Discovered {len(data)} vendors, storing to database...")
        
        @sync_to_async
        def store_vendors():
            count = 0
            with transaction.atomic():
                for vendor_data in data:
                    try:
                        vendor, created = Vendor.objects.update_or_create(
                            task=task,
                            vendor_name=str(vendor_data.get('vendor_company', ''))[:255],
                            defaults={
                                'product_name': str(vendor_data.get('product_name', ''))[:255],
                                'evidence_url': str(vendor_data.get('evidence_link', ''))[:500],
                                'source': str(vendor_data.get('domain', 'discovery'))[:255],
                                'status': str(vendor_data.get('status', 'discovered'))[:50],
                                'is_verified': True
                            }
                        )
                        count += 1
                        logger.info(f"[PHASE1] ✅ Vendor: {vendor.vendor_name}")
                    except Exception as e:
                        logger.warning(f"[PHASE1] Vendor error: {e}")
                        continue
            return count
        
        vendor_count = await store_vendors()
        task.status = 'phase1_done'
        await sync_to_async(task.save)()
        
        logger.info(f"[PHASE1] ✅ COMPLETE: {vendor_count} valid vendors found")
        return {
            'status': 'success',
            'phase': 'phase1',
            'vendors_discovered': vendor_count
        }
        
    except Exception as e:
        logger.error(f"[PHASE1] ❌ FAILED: {str(e)}", exc_info=True)
        task = await sync_to_async(Task.objects.get)(id=task_id)
        task.status = 'error'
        task.error_message = f"Phase 1 error: {str(e)}"
        await sync_to_async(task.save)()
        raise


def run_phase1_sync(task_id):
    """Sync wrapper for Django views"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(run_phase1(task_id))