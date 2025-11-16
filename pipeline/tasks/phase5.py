import asyncio
import json
import logging
from typing import Any, Dict, List

from django.db import transaction
from asgiref.sync import sync_to_async

from pipeline.models import Task, Vendor, Subtask, CapabilityMapping, FinalAnalysis
from pipeline.services.utils import safe_json_extract
from pipeline.services.llm_service import llm_service
from pipeline.prompts.prompt_4 import get_prompt_4

logger = logging.getLogger(__name__)

BATCH_SIZE = 8  # tweak if needed


# --------- Sync helper placed at module scope (safer for sync_to_async) ----------
def _store_final_analysis_sync(task_id: int, final_data: Dict[str, Any]) -> bool:
    """
    Synchronous DB write -- run inside thread via sync_to_async.
    """
    fa = final_data or {}
    # Defensive parsing / defaults
    def _to_float(v, default=0.0):
        try:
            if v is None:
                return float(default)
            s = str(v).strip()
            if s.endswith('%'):
                s = s.replace('%', '')
            return float(s)
        except Exception:
            return float(default)

    automation_2024 = _to_float(fa.get('automation_2024', fa.get('task_automation_percent_2024', 0)))
    automation_2025 = _to_float(fa.get('automation_2025', fa.get('task_automation_percent_2025', 0)))
    automation_2026 = _to_float(fa.get('automation_2026', fa.get('task_automation_percent_2026', 0)))

    # Ensure numeric ranges
    automation_2024 = max(0.0, min(100.0, automation_2024))
    automation_2025 = max(0.0, min(100.0, automation_2025))
    automation_2026 = max(0.0, min(100.0, automation_2026))

    hrf_scores = fa.get('hrf_scores', {}) or {}
    rpi_score = float(fa.get('rpi_score', 0) or 0)
    recommendations = fa.get('recommendations', []) or []

    with transaction.atomic():
        FinalAnalysis.objects.update_or_create(
            task_id=task_id,
            defaults={
                'best_vendor_name': fa.get('best_vendor_name', fa.get('best_vendor_current', 'Unknown')),
                'automation_2024': automation_2024,
                'automation_2025': automation_2025,
                'automation_2026': automation_2026,
                'hrf_scores': hrf_scores,
                'rpi_score': rpi_score,
                'recommendations': recommendations,
            }
        )
    return True
# -------------------------------------------------------------------------------


async def run_phase5(task_id: int):
    """
    PHASE 5: Final Analysis Batch/Async Safe
    """
    try:
        # load task
        task = await sync_to_async(Task.objects.get)(id=task_id)
        task.status = 'phase5_running'
        await sync_to_async(task.save)()
        logger.info(f"[PHASE5] Starting for task {task_id}")

        # Load vendors and mappings via sync_to_async
        vendors = await sync_to_async(lambda: list(Vendor.objects.filter(task_id=task_id)))()

        mappings = await sync_to_async(lambda: list(
            CapabilityMapping.objects
            .filter(task_id=task_id)
            .select_related('vendor', 'subtask')
        ))()

        if not vendors or not mappings:
            raise ValueError(f"Missing: {len(vendors)} vendors, {len(mappings)} mappings")

        logger.info(f"[PHASE5] Preparing analysis for {len(vendors)} vendors and {len(mappings)} mappings")

        all_results: List[Dict[str, Any]] = []

        # Process mappings in batches
        for b_idx in range(0, len(mappings), BATCH_SIZE):
            mappings_chunk = mappings[b_idx:b_idx + BATCH_SIZE]
            mapping_json = json.dumps([{
                "vendor": (m.vendor.vendor_name if m.vendor else ""),
                "subtask": (m.subtask.subtask_name if m.subtask else ""),
                "can_handle": (m.can_handle if hasattr(m, "can_handle") else "partially"),
                "aps_2024": float(m.aps_2024) if getattr(m, "aps_2024", None) is not None else 0.0,
                "aps_2025": float(m.aps_2025) if getattr(m, "aps_2025", None) is not None else 0.0,
                "aps_2026": float(m.aps_2026) if getattr(m, "aps_2026", None) is not None else 0.0
            } for m in mappings_chunk])

            logger.info(f"[PHASE5] Analysis batch {b_idx // BATCH_SIZE + 1}: mappings {b_idx}-{b_idx + len(mappings_chunk) - 1}")

            # call LLM
            prompt = get_prompt_4(task.task_description, mapping_json)
            response = await llm_service.call_llm(prompt)
            logger.debug(f"[PHASE5] LLM batch output type={type(response)} len={len(str(response)) if response else 0}")

            data = None
            if isinstance(response, dict):
                data = response
            elif isinstance(response, str):
                # try parse JSON; fallback to safe extractor
                try:
                    data = json.loads(response)
                except Exception:
                    data = safe_json_extract(response)

            if not isinstance(data, dict):
                logger.error(f"[PHASE5] LLM batch failed to return JSON dict for batch {b_idx // BATCH_SIZE + 1}")
                continue

            final_analysis = data.get('final_analysis')
            if not final_analysis or not isinstance(final_analysis, dict):
                logger.error(f"[PHASE5] final_analysis missing/invalid in batch {b_idx // BATCH_SIZE + 1}")
                continue

            logger.info(f"[PHASE5] Received valid final_analysis from batch {b_idx // BATCH_SIZE + 1}")
            all_results.append(final_analysis)

        if not all_results:
            raise ValueError("No valid final_analysis chunks found from LLM batches.")

        # combine/aggregate results -- for now take first valid chunk (extendable)
        combined = all_results[0]

        # store using module-scoped sync function via sync_to_async
        await sync_to_async(_store_final_analysis_sync, thread_sensitive=True)(task_id, combined)

        task.status = 'completed'
        await sync_to_async(task.save)()
        logger.info(f"[PHASE5] COMPLETE. Final analysis stored for task {task_id}")
        return {"status": "completed", "phase": "phase5", "from_llm": True}

    except Exception as e:
        logger.exception(f"[PHASE5] FAILED: {e}")
        # Attempt to mark task as error (safe)
        try:
            task = await sync_to_async(Task.objects.get)(id=task_id)
            task.status = 'error'
            task.error_message = f"Phase5: {str(e)}"
            await sync_to_async(task.save)()
        except Exception:
            logger.exception("[PHASE5] FAILED to update Task status after error.")
        raise


def run_phase5_sync(task_id):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(run_phase5(task_id))
