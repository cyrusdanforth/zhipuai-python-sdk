# Python client patterns for GLM-compatible APIs

This is an independent, community-maintained comparison of two Python client shapes: the vendor-specific SDK and the official OpenAI Python SDK pointed at an OpenAI-compatible service. It is **not** the vendor SDK and is not affiliated with Zhipu, OpenAI, or ArgoLink. **[ArgoLink](https://argolink.io/gh-zhipuai-python-sdk)** is the compatible endpoint used in the example. Last checked: 2026-10-07.

## What this repository answers

The vendor SDK is the right choice when an application needs vendor-only resources or parameters. An OpenAI-compatible client is usually the smaller integration when the target only needs chat completions and the provider documents the compatibility contract. The examples keep those contracts separate: `examples/openai_compat.py` lazily creates an OpenAI client, validates input locally, supports an optional reasoning effort, and never runs a request during import or tests.

The official SDK references used for this comparison are the [vendor Python SDK repository](https://github.com/MetaGLM/zhipuai-sdk-python-v4) and its [current release notes](https://github.com/MetaGLM/zhipuai-sdk-python-v4/releases). The compatibility client follows the [OpenAI Python SDK](https://github.com/openai/openai-python) configuration pattern. Read those pages again before pinning a production dependency; this repository does not mirror either project.

## Compatible example

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install --upgrade openai
export OPENAI_API_KEY='replace-me'
export OPENAI_BASE_URL='https://argolink.io/v1'
export MODEL_ID='glm-5.3'
python examples/openai_compat.py
```

The code defaults to `glm-5.3`, uses `POST /v1/chat/completions` through the SDK, and disables SDK retries (`max_retries=0`) so a caller does not unknowingly replay a request. Use `complete()` for a single response and `stream()` for streamed chunks. Consume a stream in the caller and record its response ID and usage before closing the job. Never commit a key or copy a signed media URL into a public issue.

```python
from examples.openai_compat import complete, stream

response = complete("Summarize this change in one sentence", effort="high")
print(response.choices[0].message.content)

for chunk in stream("List two regression checks", effort="high"):
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
```

`reasoning_effort` is accepted only where the selected model page says it is supported. An unsupported effort is a request error, not a reason to silently downgrade the model.

## Vendor SDK shape

The vendor SDK uses its own package, key variable, endpoint, error classes, and model catalog. A typical shape from the official guide is:

```python
import os
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
reply = client.chat.completions.create(
    model="<model listed by that service>",
    messages=[{"role": "user", "content": "Hello"}],
)
print(reply.choices[0].message.content)
```

Do not paste that provider-only key, URL, model ID, or exception type into the OpenAI-compatible example. The two clients can have similarly named methods while differing in streaming events, tool fields, usage accounting, retry behavior, and available models.

| Concern | Vendor-specific SDK | OpenAI-compatible example |
| --- | --- | --- |
| key | Provider key variable | `OPENAI_API_KEY` |
| base | Provider-owned API root | `OPENAI_BASE_URL=https://argolink.io/v1` |
| model | Provider catalog | Verify the target catalog; default example is `glm-5.3` |
| endpoint | SDK contract | Chat Completions; do not assume Responses support |
| retries | SDK/provider policy | Explicitly disabled in this example; handle idempotent reads only |
| errors | Provider exception classes | OpenAI SDK errors plus HTTP status and request ID |

## Current model facts

The target's live catalog and model pages are authoritative for model IDs, context, maximum output, reasoning options, tools, and effective prices. At the 2026-10-07 check, `glm-5.3` and `glm-5.2` were Chat Completions models with a 1,000,000-token context and 128,000-token maximum output. `glm-5.3` listed `low`, `high`, and `max`; `glm-5.2` listed `high` and `max`, with `reasoning_effort: none` disabling reasoning. Verify [GET /v1/models](https://argolink.io/v1/models), the [GLM-5.2 page](https://argolink.io/en/models/glm-5-2), and the [GLM-5.3 page](https://argolink.io/en/models/glm-5-3) on the day you ship. Prices are intentionally not copied into this README because a stale number is worse than a dated lookup.

## Error and safety checklist

- `401`: check the environment key, account, and base URL; never print the Authorization header.
- `400`: check the exact model ID, endpoint family, message shape, and reasoning option.
- `404`: inspect whether a client duplicated `/v1` or requested an endpoint the model does not support.
- `429` or `503`: honor `Retry-After`; do not replay a side-effecting request unless the provider documents idempotency.
- timeouts: retain the request ID when available and treat a write's outcome as unknown until checked.

The examples make no live call in CI. Run the offline checks with `python3 -m unittest discover -s tests -v`.
