"""Step 8: OpenRouter inference - Route prompt and call OpenRouter API."""
from sentence_transformers import SentenceTransformer
import json
import yaml
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import requests

# Load configuration
with open('knn_router.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Load model candidates
with open('model_candidates.json', 'r') as f:
    models = json.load(f)

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract model embeddings from config
llm_data = config['llm_data']
model_embeddings = {}
model_info = {}

for model_name, data in llm_data.items():
    model_embeddings[data['model']] = np.array(data['embedding'])
    model_info[data['model']] = {
        'cost': data['cost'],
        'max_tokens': data['max_tokens']
    }

def route_prompt(prompt: str) -> str:
    """Route a prompt to the best model based on embeddings and cost."""
    # Generate embedding for the prompt
    prompt_embedding = embedding_model.encode([prompt])[0]
    
    # Calculate cosine similarity with each model
    similarities = {}
    for model, model_emb in model_embeddings.items():
        similarity = cosine_similarity([prompt_embedding], [model_emb])[0][0]
        # Combine similarity with cost (lower cost = higher score)
        cost_score = 1.0 - model_info[model]['cost']  # Invert cost
        # Weight: 70% similarity, 30% cost preference
        combined_score = 0.7 * similarity + 0.3 * cost_score
        similarities[model] = {
            'similarity': similarity,
            'cost': model_info[model]['cost'],
            'combined_score': combined_score
        }
    
    # Select model with highest combined score
    selected_model = max(similarities.items(), key=lambda x: x[1]['combined_score'])[0]
    
    return selected_model, similarities

def call_openrouter(prompt: str, model: str) -> str:
    """Call OpenRouter API with the selected model."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set. Please set it before running.")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",  # Optional
        "X-Title": "LLM Router Demo"  # Optional
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    result = response.json()
    return result['choices'][0]['message']['content']

# Test routing and API call
prompt = "Explain transformers to a 10 year old"
selected_model, all_scores = route_prompt(prompt)

print(f"Prompt: {prompt}")
print(f"\nSelected Model: {selected_model}")
print(f"\nAll Model Scores:")
for model, scores in all_scores.items():
    print(f"  {model}: similarity={scores['similarity']:.4f}, cost={scores['cost']:.2f}, combined={scores['combined_score']:.4f}")

print(f"\n{'='*60}")
print("Calling OpenRouter API...")
try:
    response_text = call_openrouter(prompt, selected_model)
    print(f"\nLLM Response:\n{response_text}")
except Exception as e:
    print(f"\nError calling OpenRouter: {e}")
    print("\nNote: Make sure OPENROUTER_API_KEY is set in your environment.")
