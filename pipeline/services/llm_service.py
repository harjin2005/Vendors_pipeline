 

import os
import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Any

logger = logging.getLogger(__name__)

# make threadpool size configurable
_max_workers = int(os.getenv("LLM_MAX_WORKERS", "3"))
executor = ThreadPoolExecutor(max_workers=_max_workers)


def _extract_text_from_response(resp: Any) -> str:
    """Best-effort extraction of text from various response shapes.

    Handles object-like SDK responses and dict-like responses.
    Returns empty string if nothing is found.
    """
    try:
        # object-style: resp.choices
        choices = getattr(resp, "choices", None)
        if choices:
            c0 = choices[0]
            # nested message.content (SDKs)
            message = getattr(c0, "message", None)
            if message:
                return message.get("content") if isinstance(message, dict) else getattr(message, "content", "")
            # fallback to text attribute
            return c0.get("text") if isinstance(c0, dict) else getattr(c0, "text", "")

        # dict-style
        if isinstance(resp, dict):
            choices = resp.get("choices")
            if choices and len(choices) > 0:
                c0 = choices[0]
                msg = c0.get("message") if isinstance(c0, dict) else None
                if msg:
                    return msg.get("content", "")
                return c0.get("text", "")

    except Exception:
        logger.debug("_extract_text_from_response failed; raw: %r", resp)

    # Fallback to string conversion
    try:
        return str(resp)
    except Exception:
        return ""


class AzureOpenAILLMService:
    """Azure OpenAI LLM client with flexible SDK support.

    Tries to support either `openai` package (Azure usage) or
    the `azure-ai-openai` SDK. It will raise ImportError with
    actionable message if neither is available.
    """

    def __init__(self):
        # prefer the `openai` package Azure shim if available
        self.sdk: Optional[str] = None
        self.client = None
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.api_version = os.getenv("AZURE_API_VERSION", "2025-01-01-preview")

        if not all([self.api_key, self.endpoint, self.deployment]):
            missing = [k for k, v in (
                ("AZURE_OPENAI_API_KEY", self.api_key),
                ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                ("AZURE_OPENAI_DEPLOYMENT", self.deployment),
            ) if not v]
            raise ValueError(f"Missing env vars: {', '.join(missing)}")

        # try openai package first
        try:
            from openai import AzureOpenAI  # type: ignore

            # instantiate similarly to previous usage
            self.client = AzureOpenAI(api_version=self.api_version, azure_endpoint=self.endpoint, api_key=self.api_key)
            self.sdk = "openai"
            logger.info("Using `openai.AzureOpenAI` as client (openai package)")
            return
        except Exception:
            logger.debug("openai.AzureOpenAI not available or failed to init")

        # try azure.ai.openai SDK
        try:
            from azure.ai.openai import OpenAIClient  # type: ignore
            from azure.core.credentials import AzureKeyCredential  # type: ignore

            self.client = OpenAIClient(self.endpoint, AzureKeyCredential(self.api_key))
            self.sdk = "azure_sdk"
            logger.info("Using `azure.ai.openai.OpenAIClient` as client (azure sdk)")
            return
        except Exception:
            logger.debug("azure.ai.openai OpenAIClient not available or failed to init")

        # if neither worked, raise a clear error
        raise ImportError("No supported Azure OpenAI client found. Install `openai` or `azure-ai-openai` packages.")

    async def call_llm(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, retries: int = 2) -> str:
        """Asynchronously call the LLM using a thread executor and return text.

        This method is safe to call from async Django/ASGI views. For sync
        Django views, use the `call_llm_sync` helper below.
        """
        loop = asyncio.get_event_loop()

        def make_request():
            attempt = 0
            while True:
                try:
                    # prefer chat completions when available
                    if self.sdk == "openai":
                        resp = self.client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "Output ONLY valid JSON. No markdown, no extra text."},
                                {"role": "user", "content": prompt},
                            ],
                            max_tokens=max_tokens,
                            temperature=temperature,
                            model=self.deployment,
                        )
                    elif self.sdk == "azure_sdk":
                        # azure.ai.openai OpenAIClient shape: get_chat_completions(deployment, messages=...)
                        try:
                            resp = self.client.get_chat_completions(self.deployment, messages=[
                                {"role": "system", "content": "Output ONLY valid JSON. No markdown, no extra text."},
                                {"role": "user", "content": prompt},
                            ], temperature=temperature, max_tokens=max_tokens)
                        except Exception:
                            # some versions expose get_completions / get_chat_completions differently
                            resp = self.client.get_completions(self.deployment, prompt, temperature=temperature, max_tokens=max_tokens)
                    else:
                        raise RuntimeError("Unsupported LLM SDK configuration")

                    text = _extract_text_from_response(resp)
                    return text

                except Exception as err:
                    attempt += 1
                    logger.warning("LLM request failed (attempt %d/%d): %s", attempt, retries + 1, err)
                    if attempt > retries:
                        logger.exception("LLM failed after retries")
                        raise
                    backoff = 1.0 * (2 ** (attempt - 1))
                    time.sleep(backoff)

        result = await loop.run_in_executor(executor, make_request)
        logger.debug("LLM response length: %d", len(result) if result else 0)
        return result


def call_llm_sync(prompt: str, temperature: float = 0.7, max_tokens: int = 2000, retries: int = 2) -> str:
    """Sync wrapper for calling the async `call_llm` from synchronous code.

    If called inside an already-running event loop, it will run the coroutine
    on that loop using `asyncio.get_event_loop().run_until_complete` only when
    appropriate; otherwise it uses `asyncio.run`.
    """
    if llm_service is None:
        raise RuntimeError("LLM service is not initialized")

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Running event loop (e.g., inside ASGI). Run in executor via a new loop.
            coro = llm_service.call_llm(prompt, temperature=temperature, max_tokens=max_tokens, retries=retries)
            # schedule and wait synchronously is tricky when loop is running; run in a new thread
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as tpe:
                fut = tpe.submit(lambda: asyncio.run(coro))
                return fut.result()
        else:
            return asyncio.run(llm_service.call_llm(prompt, temperature=temperature, max_tokens=max_tokens, retries=retries))
    except RuntimeError:
        # Fallback: run directly
        return asyncio.run(llm_service.call_llm(prompt, temperature=temperature, max_tokens=max_tokens, retries=retries))


# Create global instance
try:
    llm_service = AzureOpenAILLMService()
except Exception as e:
    logger.error("Failed to initialize LLM: %s", e)
    llm_service = None