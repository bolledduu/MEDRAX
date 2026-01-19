# LLMRouter System Understanding

## Summary (5 bullets):

1. **What LLMRouter does**: LLMRouter is a routing system that intelligently selects the most appropriate LLM from a pool of available models based on query characteristics (embeddings, cost, quality requirements). It uses machine learning techniques (KNN, SVM, etc.) to match queries to optimal models.

2. **What routing means**: Routing is the process of analyzing an input prompt/query and selecting which LLM model should handle it. The router considers factors like query similarity (via embeddings), cost constraints, quality requirements, and model capabilities to make the selection.

3. **What inputs the router consumes**: The router takes a text prompt/query as input, along with configuration specifying available models, their embeddings, costs, and capabilities. It may also use a trained model (like a KNN classifier) that has learned optimal routing patterns.

4. **What outputs the router produces**: The router outputs a selected model identifier (e.g., "openai/gpt-4o-mini") that should be used to process the query. It may also provide routing metadata like confidence scores or cost estimates.

5. **Where OpenRouter fits**: OpenRouter is the API gateway/service that provides access to multiple LLM models through a unified interface. After the router selects a model, the system calls OpenRouter's API with the selected model identifier to actually execute the LLM inference and get the response.
