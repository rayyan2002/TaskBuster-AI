
***

# Tool Calling AI Agent

A multi-functional AI agent that can answer factual questions, perform calculations, retrieve information from custom documents, and solve math word problems—powered by LLMs and tool integration.

***

## Features

- **Web Search:** Real-time web answers using Serper API.
- **Calculator:** Accurate arithmetic/evaluable math expressions.
- **Document Q&A (RAG):** Answers based on your private documents.
- **Math Solver:** Handles math and word problems with step-by-step reasoning.
- **Modular & Extensible:** Clean code with agent, tool, and configuration modules.
- **Streamlit UI:** User-friendly web app for interaction.

***

## Installation

### 1. **Clone the Repository**

```bash
git clone <your-repository-url>
cd final_buster_project
```

### 2. **Set Up Virtual Environment** (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Requirements**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. **API Keys Setup**

Create a `.env` file in your project root, and add:

```
OPENAI_API_KEY=sk-xxxx...       # Your OpenAI API key
SERPER_API_KEY=xxxx-yyy...      # Your Serper API key (for web search)
```

**Note:**  
- Obtain [OpenAI API key](https://platform.openai.com/account/api-keys).  
- Get a [Serper API key](https://serper.dev/).

### 5. **Document Q&A Setup**

If you want to use document Q&A, include `agent_info.txt` (or your custom text file) in the project root. This enables the agent to answer document-grounded questions.

***

## Running the Streamlit App

In the project directory, run:

```bash
streamlit run app.py
```

The app will open automatically in your default browser at [http://localhost:8501](http://localhost:8501).

***

## Benchmarking (Optional)

To run automated performance tests (e.g., GSM8K, TriviaQA):

```bash
# From the project root
python benchmarks/gsm8k.py
python benchmarks/llama_benchmark.py
```

These scripts will output evaluation results to the console.

***

## Project Structure

```
final_buster_project/
│
├── app.py                  # Streamlit UI (entry point)
├── agent.py                # Agent controller logic
├── tools.py                # Tool function implementations
├── config.py               # API keys, prompts, and constants
├── .env                    # API secrets (not in public repos)
├── agent_info.txt          # (Optional) Document for RAG
├── benchmarks/
│   ├── gsm8k.py            # GSM8K math benchmark script
│   └── llama_benchmark.py  # TriviaQA/Llama benchmark
├── requirements.txt        # All Python dependencies
└── README.md               # This file
```

***

## Troubleshooting

- **ModuleNotFoundError:**  
  Always run `app.py` and benchmark scripts from the project root.
- **API Errors:**  
  Double-check your `.env` keys are valid and not expired.
- **Benchmark Import Errors:**  
  If you see import errors in benchmark scripts, ensure your working directory is the project root—not inside the `/benchmarks` folder.

***

## Contact

For questions or feedback, contact:  
- Muhammad Rayyan Ayub  
- Muhammad Umair Ali

***

**Enjoy exploring our Tool Calling AI Agent!**
