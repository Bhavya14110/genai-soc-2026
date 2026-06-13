# 🤖 Week 3: AgentX - LangGraph Research Agent

This is a robust research assistant built with LangGraph, Groq (Llama-3), and Gradio. It uses dynamic tool calling to answer historical and current event queries, formatted clearly for the user.

## ✨ Features
* **Wikipedia Tool:** Retrieves deep historical and encyclopedic knowledge.
* **DuckDuckGo Search:** Fetches real-time news and current events.
* **Reasoning Trace:** A UI accordion that reveals exactly which tools the AI called and what inputs it used.
* **Persistent Memory:** Remembers context within the same session allowing for follow-up questions.

## 🚀 How to Run Locally

1. Clone this repository and navigate to the `week3/` folder.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Rename `.env.example` to `.env` and add your Groq API Key.
5. Run the app: `python app.py`

## 📸 Screenshots
*(Add your screenshots here as required by the prompt: chatbot in action with trace open, and a follow-up question proving memory)*

## 💡 What I'd Improve (Limitations)
* *Note any specific hallucinations or times the agent looped.*
* *Mention if the response times were affected by DuckDuckGo rate limits.*