from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class PipelineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pipeline'

    def ready(self):
        logger.info("[OK] Pipeline app ready with LLM service initialized")
        try:
            from pipeline.services.llm_service import llm_service
            if llm_service:
                logger.info("[OK] Azure OpenAI LLM service initialized")
        except Exception as e:
            logger.warning(f"LLM service not initialized: {e}")
