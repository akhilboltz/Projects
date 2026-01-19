# ⚙️ Machining Advisor

![Status](https://img.shields.io/badge/Status-Prototype-orange)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![RAG](https://img.shields.io/badge/AI-RAG_Architecture-green)
![Local](https://img.shields.io/badge/Privacy-100%25_Local-lightgrey)

> **Precision Engineering meets Generative AI.** A local RAG system that ingests complex technical machining catalogs to answer parameters, feeds, and speeds queries with page-level citations.

---

## 🛑 The Problem
Production Engineers face a critical challenge: **General-purpose AI (ChatGPT, Claude) cannot be trusted with CNC parameters.**

| Standard LLMs | Machining Advisor |
| :--- | :--- |
| ❌ **Hallucinates:** invents cutting speeds that could break tools. | ✅ **Grounded:** Answers *only* using your uploaded catalogs. |
| ❌ **Generic:** Assumes standard steel properties. | ✅ **Specific:** Understands specific grades (e.g., ISO P, 42CrMo4). |
| ❌ **Black Box:** No idea where the number came from. | ✅ **Traceable:** Cites the exact page number and table index. |

---

## ✨ Key Features

### 1. Advanced Data Ingestion (`Ingestor.py`)
This isn't just a text reader. It's a custom ETL pipeline built for messy PDF tables.
* **Reversed Text Fixer:** Automatically detects and corrects corrupted PDF text (e.g., converts `gnilliM` → `Milling`, `edibrac` → `carbide`).
* **Nested Header Flattening:** Converts complex, multi-row table headers into clean, machine-readable column names.
* **Context Awareness:** intelligently scrapes "Note" and "Tip" sections below tables and attaches them to the relevant data rows to prevent context loss.

### 2. Reliable Knowledge Base (`vector_database.py`)
* **Decoupled Architecture:** Loading, chunking, and storing are separated for modularity.
* **Semantic Search:** Uses `all-MiniLM-L6-v2` embeddings to understand that "Inox" and "Stainless Steel" are related.
* **Persistent Storage:** Uses ChromaDB to save the processed knowledge, so you only ingest once.

### 3. Engineer-Centric UI (`streamlit_app.py`)
* **Adjustable "Strictness":** Control the Temperature to switch between "Creative Brainstorming" and "Strict Fact Retrieval."
* **Source Transparency:** Every answer includes a "Sources" dropdown showing the raw table data used to generate the response.

---

## 📂 Project Structure

```text
machining-advisor/
├── 📄 Ingestor.py            # The "Miner": Extracts & Cleans data from PDFs
├── 📄 vector_database.py     # The "Librarian": Organizes data into ChromaDB
├── 📄 streamlit_app.py       # The "Interface": Chat UI for the Engineer
├── 📄 test_inventory.json    # Intermediate clean data (Auto-generated)
└── 📂 chroma_db/             # Vector Store (Auto-generated)

