# Prompt Refiner 🗑️

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Prompt Refiner** is a Python module to refine and optimize prompts for large language models (LLMs) using [Alibaba Cloud Bailian](https://www.aliyun.com/product/bailian). It helps improve clarity, specificity, and overall effectiveness of prompts effortlessly.

---

## Features

* **`PromptRefiner.refine(prompt)`** — Refine any user prompt.
* **`PromptRefiner.refine_system_prompt()`** — Refine the internal system prompt.

---

## Quick Install

```bash
pip install prompt_refiner_cb
```

> **Note:** Requires a valid LLM API key (Aliyun Bailian).

---

## Usage

```python
from prompt_refiner import PromptRefiner

# Initialize the refiner
refiner = PromptRefiner(api_key="YOUR_LLM_API_KEY")

# Refine a user prompt
user_prompt = "Write a story about a dragon and a princess."
refined_prompt = refiner.refine(user_prompt)
print(refined_prompt)

# Refine the system prompt itself
refined_system = refiner.refine_system_prompt()
print(refined_system)
```

---

## Environment Variables

Create a `.env` file in your project root:

```
LLM_API_KEY="your_api_key_here"
```

Pipenv or your environment will automatically load this variable.

---

## API Reference

### `PromptRefiner(api_key=None, model="deepseek-r1")`

Initialize the refiner. Uses the environment variable `LLM_API_KEY` if `api_key` is not provided.

**Parameters:**

| Parameter | Type | Default         | Description       |
| --------- | ---- | --------------- | ----------------- |
| `api_key` | str  | `None`          | LLM API key.      |
| `model`   | str  | `"deepseek-r1"` | LLM model to use. |

---

### `refine(prompt, system_prompt=None, temperature=0)`

Refine a user prompt.

**Parameters:**

| Parameter       | Type  | Default          | Description                                      |
| --------------- | ----- | ---------------- | ------------------------------------------------ |
| `prompt`        | str   | -                | The text to refine.                              |
| `system_prompt` | str   | `_SYSTEM_PROMPT` | Optional system instructions guiding refinement. |
| `temperature`   | float | 0                | Sampling temperature (controls creativity).      |

**Returns:** `str` — The refined prompt.

---

### `refine_system_prompt(temperature=0)`

Refines the internal system prompt itself.

**Parameters:**

| Parameter     | Type  | Default | Description                          |
| ------------- | ----- | ------- | ------------------------------------ |
| `temperature` | float | 0       | Sampling temperature for refinement. |

**Returns:** `str` — The refined system prompt.

---

## License

MIT License
