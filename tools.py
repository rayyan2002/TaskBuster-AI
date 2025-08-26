import requests
import json

# If you setup your FAISS/doc QA here also add:
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
# If your tools need dataset loading/random:
from datasets import load_dataset

from config import OPENAI_API_KEY, SERPER_API_KEY

def get_openai_response(prompt, model_name="gpt-3.5-turbo"):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

def web_search(query: str):
    """
    Web search via Serper API, falls back to OpenAI GPT if Serper fails or gives no results.
    """
    print(f"Searching the web for: '{query}'...")

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            # Extract the best organic snippet
            if "organic" in data and len(data["organic"]) > 0:
                top_result = data["organic"][0]
                title = top_result.get("title", "")
                snippet = top_result.get("snippet", "")
                answer = f"{title}: {snippet}".strip()
                if answer.strip():
                    return answer
            print("Serper returned no useful result, using LLM fallback.")
        else:
            print(f"Serper error: status code {response.status_code}, using LLM fallback.")
    except Exception as e:
        print(f"Serper exception: {e}, using LLM fallback.")

    # Fallback to OpenAI if Serper fails or is empty
    answer = get_openai_response(f"Answer the following question using your general world knowledge: {query}")
    return answer

def calculator(query):
    """
    Solves arithmetic expressions (e.g., '12*7+3/2'). Uses OpenAI for natural language or complex expressions.
    """
    import re

    # Try to safely compute if it's a pure arithmetic expression
    if re.fullmatch(r'[\d\s\+\-\*\/\(\)\.]+', query):
        try:
            result = eval(query)
            return str(result)
        except Exception as e:
            print(f"Eval failed, using OpenAI for calculation. Reason: {e}")

    # Otherwise, use OpenAI as a calculator
    answer = get_openai_response(f"Calculate: {query}")
    return answer


embeddings = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY,
    model="text-embedding-ada-002"
)

# Load and split your document
loader = TextLoader("agent_info.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(documents)

# Create FAISS vector store (index)
vector_store = FAISS.from_documents(docs, embeddings)


def document_qa(query):
    
    """
    Answers a user's question using your loaded document(s) as context, via LangChain retriever + OpenAI.
    """
    # Retrieve relevant docs for the query
    retriever = vector_store.as_retriever()
    if "retriever" in globals():
        relevant_docs = retriever.get_relevant_documents(query)
    elif "vector_store" in globals():
        relevant_docs = vector_store.similarity_search(query)
    else:
        return "(No retriever/vector store available. Please set one up in advance.)"

    # Combine top docs into a context string
    context = "\n\n".join([doc.page_content for doc in relevant_docs[:3]])
    prompt = (
        f"Based only on the provided context below, answer the user's question. "
        f"If the answer is not in the context, say so.\n\n"
        f"Context:\n{context}\n\nUser Question:\n{query}"
    )
    answer = get_openai_response(prompt)
    return answer

def math_solver(query):
    """
    Solves word problems and conversions (like '30 USD in euros'), uses OpenAI for broad capability.
    """
    # Will instruct OpenAI to do the solving or conversion.
    prompt = f"Solve or convert this as accurately as possible, answer with only the number or result:\n\n{query}"
    answer = get_openai_response(prompt)
    return answer
