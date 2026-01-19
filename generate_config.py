"""Generate router configuration with embeddings."""
from sentence_transformers import SentenceTransformer
import json
import yaml

# Load model candidates
with open('model_candidates.json', 'r') as f:
    models = json.load(f)

# Generate embeddings for each model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
descriptions = [
    'GPT-4o-mini: Fast, efficient, general purpose, low cost',
    'Llama-3-70B: Large, powerful, instruction-tuned, medium cost',
    'Mistral-7B: Small, efficient, instruction-tuned, very low cost'
]
embeddings = embedding_model.encode(descriptions)

# Create YAML structure
llm_data = {}
for i, model in enumerate(models):
    model_name = model['model'].replace('/', '_').replace('-', '_')
    llm_data[model_name] = {
        'model': model['model'],
        'size': f"{model['relative_cost']*100:.0f}B",  # Use cost as proxy for size
        'cost': model['relative_cost'],
        'max_tokens': model['max_tokens'],
        'embedding': embeddings[i].tolist()
    }

# Create router config
config = {
    'router_type': 'KNNRouter',
    'llm_data': llm_data,
    'optional': {
        'n_neighbors': 1,
        'metric': 'cosine',
        'optimize_for': 'cost',  # Cost first, quality second
        'embedding_model': 'all-MiniLM-L6-v2'
    }
}

# Save YAML config
with open('knn_router.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print("Configuration generated successfully!")
print(f"Models configured: {list(llm_data.keys())}")
