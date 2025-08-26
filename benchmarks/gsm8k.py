from datasets import load_dataset
import random
from agent import run_concluder_agent   # Import your main agent function

# Load GSM8K test set
gsm8k = load_dataset("gsm8k", "main", split="test")
sample_questions = random.sample(list(gsm8k), 5)
results = []

for i, example in enumerate(sample_questions, 1):
    question = example['question']
    print(f"\n======= GSM8K Q{i}: {question} =======")
    agent_answer = run_concluder_agent(question)
    print(f"Agent Answer: {agent_answer}\nExpected: {example['answer']}\n")
    results.append({
        "question": question,
        "agent_answer": agent_answer,
        "expected": example['answer']
    })
