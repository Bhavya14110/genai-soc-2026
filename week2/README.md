# 📚 DocBuddy Pro — Q&A Over Multiple PDFs with Source Citations 🧠✨

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange?logo=gradio&logoColor=white)](https://gradio.app/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-green?logo=langchain&logoColor=white)](https://langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq-black?logo=groq&logoColor=white)](https://groq.com/)

## 🌟 Overview
**DocBuddy Pro** is an intelligent, Retrieval-Augmented Generation (RAG) application that allows you to upload multiple PDF documents and ask questions across all of them simultaneously. Say goodbye to endless scrolling—DocBuddy Pro reads, understands, and retrieves the exact information you need, complete with **source citations and page numbers**! 📖🔍

### 🤖 What is RAG?
Retrieval-Augmented Generation (RAG) gives AI models a "search engine" for your specific documents. Instead of relying solely on its pre-trained knowledge, DocBuddy retrieves the most relevant text chunks from your uploaded PDFs and feeds them to the AI, ensuring factual, grounded, and hallucination-free answers.

---

## ✨ Key Features
* **📂 Multi-Document Q&A**: Chat with lecture notes, policy documents, and research papers all at once.
* **🎯 Pinpoint Citations**: Every answer includes the exact source file and page number.
* **🔍 Transparent Retrieval**: A dedicated "Retrieved Context" panel shows you exactly which text chunks the AI used to formulate its answer.
* **💾 Smart Persistence**: Documents are indexed once and saved locally using ChromaDB, so you don't have to re-upload on every restart!
* **⚡ Blazing Fast**: Powered by Groq's lightning-fast inference engine and Llama 3.1.

---

## 🛠️ Tech Stack
* **Frontend:** [Gradio](https://gradio.app/)
* **Framework:** [LangChain](https://www.langchain.com/)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/)
* **Embeddings:** `all-MiniLM-L6-v2` (via HuggingFace)
* **LLM:** `llama-3.1-8b-instant` (via Groq)
* **Document Parsing:** `PyPDFLoader`

---

## 🚀 Installation & Setup

Follow these steps to run DocBuddy Pro locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Bhavya14110/genai-soc-2026.git](https://github.com/Bhavya14110/genai-soc-2026.git)
cd genai-soc-2026/week2
