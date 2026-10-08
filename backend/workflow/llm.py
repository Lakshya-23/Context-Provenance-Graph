"""LiteLLM wrapper — provider-agnostic LLM interface with rate limiting and Groq support.

The model is read from the LLM_MODEL environment variable.
Supports Gemini, Groq, OpenAI, Anthropic, and other LiteLLM-compatible providers.
Includes in-process rate limiting (RPM throttling) and exponential backoff retry for 429s.
"""

from __future__ import annotations

import os
import time
import threading
import litellm
from litellm.exceptions import RateLimitError
from dotenv import load_dotenv

load_dotenv()

# Suppress LiteLLM's noisy debug logs
litellm.suppress_debug_info = True


class RateLimiter:
    """Thread-safe rate limiter with sliding window RPM enforcement and minimum call interval."""

    def __init__(self, requests_per_minute: int = 30, min_interval_seconds: float = 1.0):
        self.rpm = max(1, requests_per_minute)
        self.min_interval = max(0.0, min_interval_seconds)
        self.lock = threading.Lock()
        self.timestamps: list[float] = []
        self.last_call_time = 0.0

    def wait(self) -> None:
        """Block until a request is permitted under RPM and minimum interval constraints."""
        with self.lock:
            now = time.time()

            # 1. Enforce minimum interval since last call
            elapsed_since_last = now - self.last_call_time
            if elapsed_since_last < self.min_interval:
                time.sleep(self.min_interval - elapsed_since_last)
                now = time.time()

            # 2. Enforce sliding-window requests per minute (RPM)
            cutoff = now - 60.0
            self.timestamps = [t for t in self.timestamps if t > cutoff]

            if len(self.timestamps) >= self.rpm:
                # Wait until the oldest call in the window falls outside 60s
                wait_time = 60.0 - (now - self.timestamps[0]) + 0.1
                if wait_time > 0:
                    time.sleep(wait_time)
                now = time.time()
                self.timestamps = [t for t in self.timestamps if t > (now - 60.0)]

            self.timestamps.append(now)
            self.last_call_time = now


# Initialize global rate limiter from env vars
_rpm_limit = int(os.getenv("LLM_RPM_LIMIT", "30"))
_min_delay = float(os.getenv("LLM_MIN_DELAY_SECONDS", "1.0"))
_limiter = RateLimiter(requests_per_minute=_rpm_limit, min_interval_seconds=_min_delay)


def get_model() -> str:
    """Read the configured model from environment with sensible fallbacks."""
    load_dotenv(override=True)
    model = os.getenv("LLM_MODEL")
    if model:
        return model.strip()

    # Auto-detect based on available API keys if LLM_MODEL is not set
    if os.getenv("GROQ_API_KEY"):
        return "groq/llama-3.3-70b-versatile"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini/gemini-2.0-flash"

    raise ValueError(
        "LLM_MODEL environment variable is not set. "
        "Set LLM_MODEL to a LiteLLM-supported model string:\n"
        "  - Groq: 'groq/llama-3.3-70b-versatile' (requires GROQ_API_KEY)\n"
        "  - Gemini: 'gemini/gemini-2.0-flash' (requires GEMINI_API_KEY)\n"
        "  - OpenAI: 'gpt-4o-mini' (requires OPENAI_API_KEY)"
    )


from pydantic import BaseModel

def call_llm(
    prompt: str,
    system: str = "",
    temperature: float = 0.1,
    response_format: dict | type[BaseModel] | None = None,
    max_tokens: int = 4096,
    max_retries: int = 4,
) -> dict:
    """Call the configured LLM through LiteLLM with rate limiting and exponential backoff.

    Returns:
        dict with keys:
            - content: str (the response text)
            - prompt_tokens: int
            - completion_tokens: int
    """
    model = get_model()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    # Explicitly supply API key if present for provider
    if model.startswith("groq/"):
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            kwargs["api_key"] = groq_key
    elif model.startswith("gemini/"):
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            kwargs["api_key"] = gemini_key
    elif model.startswith("openai/") or model.startswith("gpt-"):
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            kwargs["api_key"] = openai_key

    if response_format:
        kwargs["response_format"] = response_format

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            # Apply rate limiting before each call attempt
            _limiter.wait()

            response = litellm.completion(**kwargs)

            usage = response.usage
            return {
                "content": response.choices[0].message.content,
                "prompt_tokens": usage.prompt_tokens if usage else 0,
                "completion_tokens": usage.completion_tokens if usage else 0,
            }

        except RateLimitError as e:
            last_error = e
            if attempt == max_retries:
                raise
            backoff = (2 ** attempt) * 2.0  # 2s, 4s, 8s, 16s...
            print(f"[RateLimit] Hit rate limit on {model}. Retrying in {backoff:.1f}s (attempt {attempt + 1}/{max_retries})...")
            time.sleep(backoff)

        except Exception as e:
            # Check if exception string indicates 429 or rate limit
            err_msg = str(e).lower()
            if "429" in err_msg or "rate limit" in err_msg or "too many requests" in err_msg:
                last_error = e
                if attempt == max_retries:
                    raise
                backoff = (2 ** attempt) * 2.0
                print(f"[RateLimit] 429 response on {model}. Retrying in {backoff:.1f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(backoff)
            else:
                raise

    if last_error:
        raise last_error
    raise RuntimeError("Unexpected failure in call_llm")


def verify_llm_connection() -> dict:
    """Perform a lightweight test API call to ensure the configured LLM API key and model respond.

    Returns:
        dict: {"status": "ok", "model": model, "response": response_str}
    Raises:
        RuntimeError: with clear, actionable message if key is missing or model fails.
    """
    load_dotenv(override=True)
    model = get_model()

    if model.startswith("groq/") and not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(f"GROQ_API_KEY is missing. Model '{model}' requires a valid Groq API key in .env.")
    if model.startswith("gemini/") and not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(f"GEMINI_API_KEY is missing. Model '{model}' requires a valid Gemini API key in .env.")
    if (model.startswith("openai/") or model.startswith("gpt-")) and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(f"OPENAI_API_KEY is missing. Model '{model}' requires a valid OpenAI API key in .env.")

    try:
        res = call_llm(
            prompt="Respond with only the single word 'OK'.",
            system="Health check probe.",
            max_tokens=10,
            max_retries=1,
            temperature=0.0,
        )
        content = res.get("content", "").strip()
        return {
            "status": "ok",
            "model": model,
            "response": content,
        }
    except Exception as e:
        err_msg = str(e)
        raise RuntimeError(
            f"LLM test call failed for model '{model}'. "
            f"Please verify your API key and network connection. Details: {err_msg}"
        ) from e

