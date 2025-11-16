 

import asyncio
import json
import logging
from django.db import transaction
from asgiref.sync import sync_to_async

from pipeline.models import Task, Subtask
from pipeline.services.utils import safe_json_extract, validate_aps_score, get_years
from pipeline.services.llm_service import llm_service
from pipeline.prompts.prompt_2 import get_prompt_2

logger = logging.getLogger(__name__)

async def run_phase2(task_id: int):
    """PHASE 2: Subtask Decomposition - Calls PROMPT 2"""
    try:
        task = await sync_to_async(Task.objects.get)(id=task_id)
        task.status = 'phase2_running'
        await sync_to_async(task.save)()
        
        logger.info(f"[PHASE2] Starting subtask decomposition for task {task_id}")
        
        task_desc = task.task_description
        
        # Call PROMPT 2 to decompose task
        from pipeline.prompts.prompt_2 import get_prompt_2
        prompt = get_prompt_2(task_desc)
        
        logger.info("[PHASE2] Calling LLM for subtask decomposition...")
        response = await llm_service.call_llm(prompt)
        logger.debug(f"[PHASE2] LLM Response length: {len(response)}")
        
        # Extract and parse JSON
        data = safe_json_extract(response)
        if not isinstance(data, dict) or 'subtasks' not in data:
            logger.error(f"[PHASE2] Invalid response structure: {type(data)}")
            raise ValueError(f"Invalid response structure: {type(data)}")
        
        subtasks = data.get('subtasks', [])
        if not isinstance(subtasks, list) or not subtasks:
            logger.error(f"[PHASE2] No subtasks in response")
            raise ValueError("Subtasks must be non-empty list")
        
        logger.info(f"[PHASE2] Parsed {len(subtasks)} subtasks from LLM")
        
        # Store subtasks with O*NET weights
        @sync_to_async
        def create_subtasks():
            count = 0
            with transaction.atomic():
                for s in subtasks[:10]:
                    try:
                        weight = float(s.get('importance', 0.5)) * (float(s.get('time_percent', 20)) / 100)
                        subtask, created = Subtask.objects.update_or_create(
                            task_id=task_id,
                            subtask_name=str(s.get('subtask_name', ''))[:200],
                            defaults={
                                'description': str(s.get('description', ''))[:500],
                                'time_percent': float(s.get('time_percent', 0)),
                                'importance': float(s.get('importance', 0)),
                                'ai_applicable': str(s.get('ai_applicable', 'no'))[:20],
                                'onet_weight': weight
                            }
                        )
                        count += 1
                        logger.info(f"[PHASE2] ✅ Subtask: {subtask.subtask_name} ({s.get('time_percent', 0)}%)")
                    except Exception as e:
                        logger.warning(f"[PHASE2] Subtask error: {e}")
                        continue
            return count
        
        count = await create_subtasks()
        task.status = 'phase2_done'
        await sync_to_async(task.save)()
        
        logger.info(f"✅ [PHASE2] Done: {count} subtasks created")
        return {"status": "phase2_done", "subtasks_created": count}
        
    except Exception as e:
        logger.error(f"❌ [PHASE2] {type(e).__name__}: {e}", exc_info=True)
        task = await sync_to_async(Task.objects.get)(id=task_id)
        task.status = 'error'
        task.error_message = str(e)
        await sync_to_async(task.save)()
        raise


def run_phase2_sync(task_id):
    """Sync wrapper for Django views"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(run_phase2(task_id))