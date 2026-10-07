"""Safe OpenAI-compatible GLM examples.

The functions return SDK response objects and are deliberately not called at import
or test time. Put credentials in the environment, never in source control.
"""
from __future__ import annotations

import os
from typing import Any


def _client() -> Any:
    from openai import OpenAI

    return OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.getenv("OPENAI_BASE_URL", "https://argolink.io/v1"),
        timeout=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60")),
        max_retries=0,
    )


def complete(prompt: str, *, model: str | None = None, effort: str | None = None) -> Any:
    """Call the target catalog through the OpenAI SDK's Chat Completions API."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    body: dict[str, Any] = {
        "model": model or os.getenv("MODEL_ID", "glm-5.3"),
        "messages": [{"role": "user", "content": prompt}],
    }
    if effort:
        body["reasoning_effort"] = effort
    return _client().chat.completions.create(**body)


def stream(prompt: str, *, model: str | None = None, effort: str | None = None) -> Any:
    """Return a stream; the caller must consume it and close the client in long jobs."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    body: dict[str, Any] = {
        "model": model or os.getenv("MODEL_ID", "glm-5.3"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    if effort:
        body["reasoning_effort"] = effort
    return _client().chat.completions.create(**body)


if __name__ == "__main__":
    result = complete("Say one sentence about reproducible benchmarks.")
    print(result.choices[0].message.content)
