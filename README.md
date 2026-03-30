<div align="center">

# apicost

**Know your AI API costs before you spend.**

Calculate and compare LLM pricing from the terminal. 25+ models, all major providers.

[![PyPI](https://img.shields.io/pypi/v/apicost)](https://pypi.org/project/apicost/)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

</div>

---

## Install

```bash
pip install apicost
```

## Usage

### Calculate cost for a specific model

```bash
$ apicost calc gpt-4o -i 10000 -o 2000

  Model:    gpt-4o (OpenAI)
  Input:    10,000 tokens  →  $0.0250
  Output:   2,000 tokens   →  $0.0200
  ─────────────────────────────────
  Total:    $0.0450
```

### Compare costs across ALL models

```bash
$ apicost compare -i 10000 -o 2000

  Cost comparison: 10,000 input + 2,000 output tokens

  Model                     Provider        Input        Output       Total
  ───────────────────────── ─────────────── ──────────── ──────────── ────────────
  ollama                    Local (Ollama)  $0.00 (free) $0.00 (free) $0.00 (free)
  mistral-nemo              Mistral         $0.000200    $0.000040    $0.000240
  llama-3.3-70b             Meta (Groq)     $0.000600    $0.000120    $0.000720
  deepseek-v3               DeepSeek        $0.0028      $0.000840    $0.0036
  gpt-4o-mini               OpenAI          $0.0015      $0.0012      $0.0027
  ...
  claude-opus-4-6           Anthropic       $0.0500      $0.0500      $0.10
```

### List all models and pricing

```bash
$ apicost list
```

### Use as a Python library

```python
from apicost import calculate_cost, estimate_cost

# Exact token count
result = calculate_cost("gpt-4o", input_tokens=5000, output_tokens=1000)
print(f"Total: ${result['total_cost']:.4f}")

# Estimate from text
result = estimate_cost("claude-sonnet-4-6", input_text="Your prompt here...", output_tokens=500)
print(f"Estimated: ${result['total_cost']:.6f}")
```

## Supported Models

| Provider | Models |
|----------|--------|
| **Anthropic** | Claude Opus 4.6, Sonnet 4.6, Haiku 4.5 |
| **OpenAI** | GPT-5.2, GPT-5.2 Mini, GPT-4o, GPT-4o Mini, o3, o3-mini |
| **Google** | Gemini 3.1 Pro, 3 Flash, 2.5 Pro, 2.0 Flash, 2.0 Flash-Lite |
| **DeepSeek** | V3, R1 |
| **Mistral** | Large, Small, Nemo |
| **Meta** | Llama 4 Maverick, Scout, 3.3 70B (via Groq) |
| **Cohere** | Command R+, Command R |
| **Local** | Ollama, any local model ($0) |

## Commands

```bash
apicost calc <model> [-i INPUT] [-o OUTPUT]    # Calculate cost
apicost compare [-i INPUT] [-o OUTPUT]          # Compare all models
apicost list                                     # Show all models + pricing
```

## Why?

Every AI developer asks "how much will this cost?" before making API calls. This tool answers that instantly, from your terminal or Python code, without looking up pricing pages.

## Contributing

PRs welcome — especially for adding new models and keeping prices up to date.

## License

[MIT](LICENSE)

---

<div align="center">

**If this saves you money, give it a star.**

</div>

---

## Also By OuterSpacee

| Project | Description |
|---------|-------------|
| [Awesome AI Tools](https://github.com/OuterSpacee/awesome-ai-tools) | 200+ AI tools across 22 categories |
| [Build Your Own AI](https://github.com/OuterSpacee/build-your-own-ai) | 150+ tutorials for building AI projects from scratch |
| [AI Engineering Handbook](https://github.com/OuterSpacee/ai-engineering-handbook) | Everything you need to build production AI apps |
| [Free AI APIs](https://github.com/OuterSpacee/free-ai-apis) | 100+ free AI APIs for developers |
| [aimsg](https://github.com/OuterSpacee/aimsg) | AI-powered git commit messages — free with Ollama |
