from datasets import load_dataset
import time
from agent import run_concluder_agent

# Load TriviaQA validation subset
trivia_dataset = load_dataset("trivia_qa", "rc.nocontext", split="validation[:100]")
questions_to_test = 30
subset_to_test = trivia_dataset.select(range(questions_to_test))
correct_predictions = 0

print(f"--- Starting TriviaQA Benchmark on {questions_to_test} questions ---")
for item in subset_to_test:
    question = item['question']
    correct_aliases = item['answer']['aliases']

    print(f"\n--- Testing Question: {question} ---")
    print(f"Correct Answers Can Include: {correct_aliases}")
    agent_response = run_concluder_agent(question)

    is_correct = any(alias.lower() in str(agent_response).lower() for alias in correct_aliases)

    if is_correct:
        print("✅ Correct")
        correct_predictions += 1
    else:
        print(f"❌ Incorrect. Agent response: {agent_response}")

    time.sleep(5)  # To respect API rate limits

accuracy = (correct_predictions / len(subset_to_test)) * 100
print(f"\n--- TriviaQA Evaluation Complete ---")
print(f"Final Factual Accuracy: {accuracy:.2f}% ({correct_predictions} out of {len(subset_to_test)} correct)")
