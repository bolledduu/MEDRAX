import dspy
import json
import os
import sys

# Add project root to sys.path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.signatures import MedRAXSignature

# Load the compiled model
def load_model(model_path):
    # Re-instantiate the agent class (ReAct with Signature)
    # Note: We need to know the tools it was trained with to reconstruct the class structure correctly if loading weights,
    # but dspy.load usually loads the program state.
    # For simplicity, we'll just load the program if possible, or reconstruct and load.
    # The blueprint says "compiled_medrax.save", so we load it back.
    # However, dspy.ReAct needs tools.
    from src.tools import MedRAXTools
    agent = dspy.ReAct(MedRAXSignature, tools=[MedRAXTools.chexagent_detect, MedRAXTools.medsam_segment])
    agent.load(model_path)
    return agent

def run_evaluation():
    results_path = os.path.join(os.path.dirname(__file__), '../results/medrax_compiled.json')
    if not os.path.exists(results_path):
        print("Compiled model not found. Run train_medrax.py first.")
        return

    print(f"Loading model from {results_path}...")
    agent = load_model(results_path)

    # Load test data
    data_path = os.path.join(os.path.dirname(__file__), '../data/test_samples.json')
    with open(data_path, 'r') as f:
        data = json.load(f)

    print("Running evaluation...")
    for item in data:
        print(f"\nQuestion: {item['question']}")
        pred = agent(
            clinical_context=item['context'],
            image_path=item['image_path'],
            question=item['question']
        )
        print(f"Predicted Answer: {pred.answer}")
        print(f"Reasoning: {pred.reasoning}")

if __name__ == "__main__":
    run_evaluation()
