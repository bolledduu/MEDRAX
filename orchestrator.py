"""Step 9: Core orchestrator - Route prompts and call OpenRouter."""
from sentence_transformers import SentenceTransformer
import json
import yaml
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import requests
from typing import Dict

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

def route_prompt(prompt: str) -> tuple:
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
    
    return selected_model, similarities[selected_model]

def call_openrouter(prompt: str, model: str) -> str:
    """Call OpenRouter API with the selected model."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set. Please set it before running.")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "LLM Router Demo"
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

def orchestrate(prompt: str) -> Dict:
    """
    Main orchestration function that routes a prompt and calls OpenRouter.
    
    Args:
        prompt: The input prompt to route and process
        
    Returns:
        Dictionary with model_used, response, and estimated_cost
    """
    # Step 1: Route the prompt
    selected_model, routing_info = route_prompt(prompt)
    
    # Step 2: Log routing decision
    print(f"[ROUTING] Prompt: {prompt[:50]}...")
    print(f"[ROUTING] Selected Model: {selected_model}")
    print(f"[ROUTING] Similarity: {routing_info['similarity']:.4f}, Cost: {routing_info['cost']:.2f}")
    
    # Step 3: Call OpenRouter
    try:
        response_text = call_openrouter(prompt, selected_model)
        
        # Step 4: Estimate cost (simplified: cost per token approximation)
        # This is a rough estimate - actual cost depends on input/output tokens
        estimated_cost = routing_info['cost'] * 0.001  # Rough estimate
        
        return {
            "model_used": selected_model,
            "response": response_text,
            "estimated_cost": estimated_cost,
            "routing_metadata": {
                "similarity": routing_info['similarity'],
                "model_cost": routing_info['cost']
            }
        }
    except Exception as e:
        print(f"[ERROR] Failed to call OpenRouter: {e}")
        raise

if __name__ == "__main__":
    # Test the orchestrator
    test_prompt = "Explain transformers to a 10 year old"
    result = orchestrate(test_prompt)
    print(f"\n{'='*60}")
    print("Orchestration Result:")
    print(f"Model Used: {result['model_used']}")
    print(f"Estimated Cost: ${result['estimated_cost']:.6f}")
    print(f"Response: {result['response'][:200]}...")
