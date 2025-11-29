import dspy
import json
import os
import sys

# Add project root to sys.path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.signatures import MedRAXSignature
from src.tools import MedRAXTools

# 1. Load Data
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    examples = []
    for item in data:
        # Create dspy.Example
        # Inputs: clinical_context, image_path, question
        # Labels: reasoning (gold_reasoning), answer
        example = dspy.Example(
            clinical_context=item['context'],
            image_path=item['image_path'],
            question=item['question'],
            reasoning=item['gold_reasoning'],
            answer=item['answer']
        ).with_inputs('clinical_context', 'image_path', 'question')
        examples.append(example)
    return examples

data_path = os.path.join(os.path.dirname(__file__), '../data/train_samples.json')
print(f"Loading data from {data_path}...")
train_data = load_data(data_path)
print(f"Loaded {len(train_data)} examples.")

# 2. Define the Agent
# We use ReAct, which allows the model to "Think" and "Act" (use tools)
print("Initializing MedRAX Agent...")
medrax_agent = dspy.ReAct(MedRAXSignature, tools=[MedRAXTools.chexagent_detect, MedRAXTools.medsam_segment])

# 3. Define Success Metric
# If the agent's answer matches the gold standard, it gets a point.
def medical_accuracy_metric(example, prediction, trace=None):
    # Simple containment check as per blueprint
    return example.answer.lower() in prediction.answer.lower()

# 4. Optimize (The "Training" Step)
# MIPROv2 will generate new instructions and few-shot examples to maximize the metric
from dspy.teleprompt import MIPROv2

print("Initializing Optimizer (MIPROv2)...")
# Note: This expects OPENAI_API_KEY to be set in the environment
optimizer = MIPROv2(metric=medical_accuracy_metric, prompt_model=dspy.OpenAI(model='gpt-4o'))

print("Starting Optimization...")
# This step takes time: It runs the agent many times to find the best prompt
compiled_medrax = optimizer.compile(medrax_agent, trainset=train_data)

# 5. Save the Result
results_dir = os.path.join(os.path.dirname(__file__), '../results')
os.makedirs(results_dir, exist_ok=True)
output_path = os.path.join(results_dir, "medrax_compiled.json")
compiled_medrax.save(output_path)

print(f"Optimization Complete. Compiled program saved to {output_path}")
