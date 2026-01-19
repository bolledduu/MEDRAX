"""Step 10: Multi-prompt test - Test orchestrate() with 3 different prompts."""
from orchestrator import orchestrate
import json

# Test prompts
prompts = [
    "Summarize gravity",
    "Prove convergence of gradient descent",
    "Write a haiku about stars"
]

print("="*70)
print("MULTI-PROMPT ROUTING TEST")
print("="*70)

results = []

for i, prompt in enumerate(prompts, 1):
    print(f"\n{'='*70}")
    print(f"TEST {i}/3")
    print(f"{'='*70}")
    
    try:
        result = orchestrate(prompt)
        results.append({
            "prompt": prompt,
            "model_used": result["model_used"],
            "response_preview": result["response"][:150] + "..." if len(result["response"]) > 150 else result["response"],
            "estimated_cost": result["estimated_cost"],
            "routing_metadata": result["routing_metadata"]
        })
        
        print(f"\n[RESULT] Model: {result['model_used']}")
        print(f"[RESULT] Estimated Cost: ${result['estimated_cost']:.6f}")
        print(f"[RESULT] Response Preview: {result['response'][:200]}...")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to process prompt: {e}")
        results.append({
            "prompt": prompt,
            "error": str(e)
        })

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")

print("\nRouting Decisions:")
for i, result in enumerate(results, 1):
    if "error" not in result:
        print(f"  {i}. Prompt: {result['prompt']}")
        print(f"     Model: {result['model_used']}")
        print(f"     Cost: ${result['estimated_cost']:.6f}")
        print(f"     Similarity: {result['routing_metadata']['similarity']:.4f}")
    else:
        print(f"  {i}. Prompt: {result['prompt']}")
        print(f"     ERROR: {result['error']}")

# Check if routing decisions differ
if len(results) > 1 and all("error" not in r for r in results):
    models_used = [r["model_used"] for r in results if "error" not in r]
    unique_models = set(models_used)
    print(f"\n[VERIFICATION] Unique models selected: {len(unique_models)}")
    if len(unique_models) > 1:
        print("  [PASS] Routing decisions differ across prompts (GOOD)")
    else:
        print("  [WARN] All prompts routed to same model")

# Save results
with open('multi_prompt_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to multi_prompt_results.json")
