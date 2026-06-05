# 🤖 PromptForge — Multi-Mode AI Assistant

Welcome to **PromptForge**, a versatile Gradio-based web application that demonstrates the power of multi-persona AI interactions using the Groq API (LLaMA3). 🌟

This project allows users to seamlessly switch between four distinct AI personalities, complete with real-time text streaming and dynamic UI updates based on the active system prompt. 🎭

## ✨ Key Features

* **4 Unique AI Personas:** 
 
  * 👨‍🏫 **Technical Explainer:** Breaks down complex concepts simply using analogies.
  * 🕵️‍♂️ **Code Reviewer:** Analyzes code and outputs structured JSON (dynamically rendered into clean Markdown).
  * ⚖️ **Debate Coach:** Plays devil's advocate and argues both sides of any prompt.
  * ✍️ **Creative Writer:** Generates vivid, descriptive narrative prose.
  * **🌊 Streaming Responses:** Implements a token-by-token typewriter effect for a highly responsive user experience.
  * **🧩 Dynamic JSON Rendering:** Automatically catches and parses JSON outputs in Code Reviewer mode, formatting them into beautiful Markdown while handling potential LLM formatting errors.
  * **🎛️ Adjustable Temperature:** Gives the user control over the model's creativity and randomness.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.8 or higher 🐍
* A valid [Groq API Key](https://console.groq.com/) 🔑

## 🚀 Setup & Installation

1. **Clone the repository:**
   Navigate to the project folder (`week1-promptforge/`).

2. **Install the dependencies:**
   Run the following command in your terminal to install Gradio, Groq, and python-dotenv:
   ```bash
   pip install -r requirements.txt