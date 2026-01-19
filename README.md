# LLM Orchestration System with OpenRouter

End-to-end LLM orchestration system using llmrouter-lib that routes prompts to different LLMs via OpenRouter.

## System Overview

This system intelligently routes prompts to the most appropriate LLM model based on:
- **Semantic similarity** (using embeddings)
- **Cost optimization** (prioritizing lower-cost models)
- **Model capabilities** (based on model characteristics)

## Architecture

1. **LLMRouter**: Routes prompts to optimal models using KNN-based similarity matching
2. **OpenRouter**: API gateway that provides access to multiple LLM models
3. **Orchestrator**: Main function that coordinates routing and API calls

## Files Created

- `model_candidates.json` - Configuration of available models
- `knn_router.yaml` - Router configuration with embeddings
- `orchestrator.py` - Core orchestration function
- `test_routing.py` - Routing-only test (no API calls)
- `test_routing_with_api.py` - Routing with OpenRouter API calls
- `test_multi_prompt.py` - Multi-prompt testing
- `verification.py` - System verification script

## Setup

1. **Install dependencies**:
   ```bash
   pip install llmrouter-lib sentence-transformers scikit-learn requests pyyaml
   ```

2. **Set OpenRouter API key**:
   ```bash
   # Windows
   set OPENROUTER_API_KEY=your-key-here
   
   # Linux/Mac
   export OPENROUTER_API_KEY=your-key-here
   ```
   
   **Note**: You need an OpenRouter API key (not OpenAI). Get it from: https://openrouter.ai/keys

## Usage

### Basic Orchestration

```python
from orchestrator import orchestrate

result = orchestrate("Explain transformers to a 10 year old")
print(f"Model used: {result['model_used']}")
print(f"Response: {result['response']}")
print(f"Estimated cost: ${result['estimated_cost']:.6f}")
```

### Test Routing Only

```bash
python test_routing.py
```

### Test with API Calls

```bash
python test_routing_with_api.py
```

### Multi-Prompt Test

```bash
python test_multi_prompt.py
```

### Verification

```bash
python verification.py
```

## Model Candidates

The system is configured with 3 models:

1. **openai/gpt-4o-mini** - Fast, efficient, general purpose (cost: 0.15)
2. **meta-llama/llama-3-70b-instruct** - Large, powerful, instruction-tuned (cost: 0.59)
3. **mistralai/mistral-7b-instruct** - Small, efficient, instruction-tuned (cost: 0.07)

## Routing Logic

The router uses:
- **70% weight** on semantic similarity (embedding-based)
- **30% weight** on cost optimization

## Next Steps

1. Set your OpenRouter API key
2. Run `python test_multi_prompt.py` to test with real API calls
3. Customize model candidates in `model_candidates.json`
4. Adjust routing weights in `orchestrator.py` if needed
