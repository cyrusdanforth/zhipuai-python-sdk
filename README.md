# Python access patterns for GLM

This is an independent comparison of the official Zhipu Python SDK concept and the OpenAI Python SDK pointed at an OpenAI-compatible endpoint. It is not the Zhipu SDK. **[ArgoLink](https://argolink.io/gh-zhipuai-python-sdk) is the example compatible base.** Last checked: 2026-10-07.

## Two clients, two contracts

The vendor SDK may expose provider-specific parameters and model availability. The compatibility example in examples/openai_compat.py uses OpenAI(base_url=..., api_key=...) and chat.completions. It keeps the model ID in MODEL_ID and the key in OPENAI_API_KEY. This file is a runnable shape after installing the official openai package; it does not run during tests.

| Concern | Provider SDK | OpenAI-compatible client |
|---|---|---|
| authentication | SDK-specific key variable | OpenAI API key and base URL |
| model ID | vendor catalog | target catalog ID |
| request path | SDK-owned | chat or Responses contract |
| extensions | provider-specific | only documented compatibility |
| error type | SDK-specific | OpenAI SDK/httpx errors |

Do not conclude that a vendor SDK model ID works at another base URL. Verify tools, streaming, structured output, reasoning, and usage fields independently. For asynchronous video, use its native submit/status/content contract rather than chat completions.

## Migration checklist

Install and pin the client version. Read the current vendor quickstart if you need provider-native fields. For an OpenAI-compatible target, set OPENAI_BASE_URL to https://argolink.io/v1, choose an ID present in the live catalog, make a small schema request, and inspect the response. Add a User-Agent if you use urllib directly. Redact keys and signed media URLs.

The model page controls price, context, output, and feature support. This repository intentionally does not publish a stale price table. Keep a dated record of the catalog revision and endpoint family. A timeout can leave a tool side effect unknown; preserve a response ID before retrying.

## Tests and FAQ

python3 -m unittest discover -s tests checks the example source offline. **Is this official?** No. **Can I mix request objects?** Only when the selected endpoint documents both shapes. **Why use the official OpenAI package?** It gives a maintained client transport without pretending to be a vendor SDK. **Where do I find GLM IDs?** The current target catalog/model page.
