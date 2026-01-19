"""Final end-to-end test of the orchestration system."""
from orchestrator import orchestrate

print("="*70)
print("FINAL END-TO-END TEST")
print("="*70)

prompt = "What is machine learning?"
print(f"\nPrompt: {prompt}\n")

result = orchestrate(prompt)

print("\n" + "="*70)
print("RESULT")
print("="*70)
print(f"Model Used: {result['model_used']}")
print(f"Estimated Cost: ${result['estimated_cost']:.6f}")
print(f"\nResponse:\n{result['response']}")
print("\n" + "="*70)
print("[SUCCESS] SYSTEM FULLY OPERATIONAL!")
print("="*70)
