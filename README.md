# ⚙️ Machining Advisor (RAG-based Assistant)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green?logo=langchain&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Llama3-black?logo=ollama&logoColor=white)

**Machining Advisor** is an AI-powered tool designed for Production Engineers. It uses **Retrieval-Augmented Generation (RAG)** to "read" technical PDF catalogs (like Schnittwerte/Cutting Data) and answer specific questions about cutting speeds, feeds, and material mappings.

Unlike generic AI, this tool is grounded in **your** specific technical documents, reducing hallucinations and providing page-specific citations.

---

## 🚀 Why this project?

Standard LLMs (like ChatGPT) don't know the specific cutting parameters of your workshop's tools. They hallucinate numbers.
**Machining Advisor** solves this by:
1.  **Ingesting** complex PDF tables (handling reversed text like "gnilliM" automatically).
2.  **Storing** data in a local Vector Database (ChromaDB).
3.  **Retrieving** only the relevant rows (e.g., "Steel Milling speeds") to answer your question.

---

## 🛠️ Architecture

The project consists of three main modules:

1.  **`Ingestor.py`**: A custom ETL pipeline using `pdfplumber`.
    * *Feature:* Fixes reversed text (e.g., "edibrac" -> "carbide").
    * *Feature:* Flattens complex nested table headers.
    * *Feature:* Extracts "Tips" found below tables and attaches them to the data.
2.  **`Vector_Database.py`**: Manages the Knowledge Base.
    * Embeds text using `all-MiniLM-L6-v2`.
    * Stores chunks in a persistent `ChromaDB`.
3.  **`streamlit_app.py`**: The "Face" of the application.
    * Chat interface powered by **Ollama** (Llama 3, Mistral, etc.).
    * Adjustable parameters (Temperature, K-Retrieval).

---

## 📦 Installation

### Prerequisites
1.  **Python 3.10+** installed.
2.  **Ollama** installed and running locally.
    * Pull the model: `ollama pull llama3.1:latest`

### Step 1: Clone the Repo
```bash
git clone [https://github.com/yourusername/machining-advisor.git](https://github.com/yourusername/machining-advisor.git)
cd machining-advisor
