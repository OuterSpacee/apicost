"""Model pricing data and cost calculation functions."""

# Prices per 1M tokens (USD) — March 2026
# Format: "model_name": {"input": price, "output": price, "provider": "name"}
MODEL_PRICES: dict[str, dict] = {
    # Anthropic
    "claude-opus-4-6": {"input": 5.00, "output": 25.00, "provider": "Anthropic"},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "provider": "Anthropic"},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00, "provider": "Anthropic"},

    # OpenAI
    "gpt-5.2": {"input": 1.75, "output": 14.00, "provider": "OpenAI"},
    "gpt-5.2-mini": {"input": 0.40, "output": 1.60, "provider": "OpenAI"},
    "gpt-4o": {"input": 2.50, "output": 10.00, "provider": "OpenAI"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "provider": "OpenAI"},
    "o3": {"input": 10.00, "output": 40.00, "provider": "OpenAI"},
    "o3-mini": {"input": 1.10, "output": 4.40, "provider": "OpenAI"},

    # Google
    "gemini-3.1-pro": {"input": 2.00, "output": 12.00, "provider": "Google"},
    "gemini-3-flash": {"input": 0.50, "output": 3.00, "provider": "Google"},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00, "provider": "Google"},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40, "provider": "Google"},
    "gemini-2.0-flash-lite": {"input": 0.075, "output": 0.30, "provider": "Google"},

    # DeepSeek
    "deepseek-v3": {"input": 0.28, "output": 0.42, "provider": "DeepSeek"},
    "deepseek-r1": {"input": 0.55, "output": 2.19, "provider": "DeepSeek"},

    # Mistral
    "mistral-large": {"input": 2.00, "output": 6.00, "provider": "Mistral"},
    "mistral-small": {"input": 0.20, "output": 0.60, "provider": "Mistral"},
    "mistral-nemo": {"input": 0.02, "output": 0.02, "provider": "Mistral"},

    # Meta (via Groq/Together)
    "llama-4-maverick": {"input": 0.10, "output": 0.10, "provider": "Meta (Groq)"},
    "llama-4-scout": {"input": 0.10, "output": 0.10, "provider": "Meta (Groq)"},
    "llama-3.3-70b": {"input": 0.06, "output": 0.06, "provider": "Meta (Groq)"},

    # Cohere
    "command-r-plus": {"input": 2.50, "output": 10.00, "provider": "Cohere"},
    "command-r": {"input": 0.15, "output": 0.60, "provider": "Cohere"},

    # Local (free)
    "ollama": {"input": 0.00, "output": 0.00, "provider": "Local (Ollama)"},
    "local": {"input": 0.00, "output": 0.00, "provider": "Local"},
}


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> dict:
    """Calculate the cost of an API call."""
    model_lower = model.lower()

    # Try exact match first, then partial match
    pricing = MODEL_PRICES.get(model_lower)
    if not pricing:
        for key, value in MODEL_PRICES.items():
            if key in model_lower or model_lower in key:
                pricing = value
                model_lower = key
                break

    if not pricing:
        return {
            "model": model,
            "error": f"Unknown model: {model}. Use 'tokencost list' to see available models.",
        }

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "model": model_lower,
        "provider": pricing["provider"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "input_price_per_1m": pricing["input"],
        "output_price_per_1m": pricing["output"],
    }


def estimate_cost(
    model: str,
    input_text: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int = 500,
) -> dict:
    """Estimate cost from text or token count."""
    if input_text:
        # Rough estimation: ~4 chars per token for English
        input_tokens = len(input_text) // 4
    elif input_tokens is None:
        input_tokens = 1000  # default

    return calculate_cost(model, input_tokens, output_tokens)


def list_models() -> list[dict]:
    """List all available models with pricing."""
    models = []
    for name, pricing in sorted(MODEL_PRICES.items()):
        models.append({
            "model": name,
            "provider": pricing["provider"],
            "input_per_1m": pricing["input"],
            "output_per_1m": pricing["output"],
        })
    return models


def get_model_info(model: str) -> dict | None:
    """Get pricing info for a specific model."""
    pricing = MODEL_PRICES.get(model.lower())
    if not pricing:
        return None
    return {
        "model": model.lower(),
        "provider": pricing["provider"],
        "input_per_1m": pricing["input"],
        "output_per_1m": pricing["output"],
    }
