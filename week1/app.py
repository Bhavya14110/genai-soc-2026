import os
import json
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# --- 1. SETUP & AUTH ---
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- 2. PERSONAS DICTIONARY ---
personas = {
    "Technical Explainer": {
        "system_prompt": "Explain complex topics simply, without jargon. Use analogies.",
        "few_shot_examples": [
            {"role": "user", "content": "What is an API?"},
            {"role": "assistant", "content": "Think of an API like a waiter in a restaurant. You tell the waiter (API) what you want, they take the request to the kitchen (server), and bring your food (data) back to you!"}
        ],
        "output_format": "text"
    },
    "Code Reviewer": {
        "system_prompt": "Review the given code and output ONLY valid JSON with keys: 'issues', 'suggestions', and 'severity'. Do not include any other text.",
        "few_shot_examples": [
            {"role": "user", "content": "def add(a, b): return a - b"},
            {"role": "assistant", "content": '{"issues": ["Function subtracts instead of adds."], "suggestions": ["Change a - b to a + b."], "severity": "High"}'}
        ],
        "output_format": "json"
    },
    "Debate Coach": {
        "system_prompt": "Argue aggressively but logically for BOTH sides of the user's prompt. Play devil's advocate.",
        "few_shot_examples": [],
        "output_format": "text"
    },
    "Creative Writer": {
        "system_prompt": "Respond with vivid, descriptive, and highly imaginative narrative prose.",
        "few_shot_examples": [],
        "output_format": "text"
    }
}

# --- 3. HELPER FUNCTIONS ---
def build_messages(user_prompt, selected_mode):
    mode_data = personas[selected_mode]
    messages = [{"role": "system", "content": mode_data["system_prompt"]}]
    
    for example in mode_data["few_shot_examples"]:
        messages.append(example)
        
    messages.append({"role": "user", "content": user_prompt})
    return messages

def format_code_reviewer_output(raw_text):
    # Bug Fix: Strip markdown backticks if the model adds them!
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
    cleaned_text = cleaned_text.strip()
    
    try:
        data = json.loads(cleaned_text)
        md_output = f"### 🕵️‍♂️ Code Review Results\n\n"
        severity = data.get('severity', 'Unknown')
        md_output += f"**Severity:** `{severity}`\n\n"
        
        md_output += "**🚨 Issues Found:**\n"
        for issue in data.get('issues', ["No issues reported."]):
            md_output += f"* {issue}\n"
            
        md_output += "\n**💡 Suggestions:**\n"
        for suggestion in data.get('suggestions', ["No suggestions provided."]):
            md_output += f"* {suggestion}\n"
            
        return md_output
    except json.JSONDecodeError:
        return f"⚠️ **Warning: The model did not output valid JSON.**\n\n{raw_text}"

# --- 4. GENERATOR / STREAMING FUNCTION ---
def chat_logic(user_input, chat_history, mode, temperature):
    """Handles the chat history update and the streaming generation."""
    
    # NEW FORMAT: Gradio 5+ strict dictionary format! 📦
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": ""})
    
    messages = build_messages(user_input, mode)
    
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Your updated model string!
        messages=messages,
        temperature=temperature,
        stream=True
    )
    
    accumulated_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            accumulated_text += chunk.choices[0].delta.content
            # Update the 'content' key of the last assistant dictionary
            chat_history[-1]["content"] = accumulated_text
            yield "", chat_history # Yield empty string to clear the textbox, and updated history
            
    # Apply JSON formatting if Code Reviewer is finished
    if mode == "Code Reviewer":
        formatted_final_text = format_code_reviewer_output(accumulated_text)
        chat_history[-1]["content"] = formatted_final_text
        yield "", chat_history

# --- 5. UI UPDATER ---
def update_system_prompt_ui(selected_mode):
    return personas[selected_mode]["system_prompt"]

# --- 6. GRADIO INTERFACE ---
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 PromptForge Multi-Mode AI")
    
    with gr.Row():
        mode_dropdown = gr.Dropdown(choices=list(personas.keys()), value="Technical Explainer", label="AI Persona")
        temp_slider = gr.Slider(minimum=0.0, maximum=1.5, value=0.7, label="Temperature")
        
    with gr.Accordion("Active System Prompt", open=False):
        sys_prompt_display = gr.Markdown(personas["Technical Explainer"]["system_prompt"])
        
    # Standard Chatbot with NO type parameter! 🛠️
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(label="Type your message here...", placeholder="Press Enter to send...")
    
    # --- THE WIRING ---
    mode_dropdown.change(
        fn=update_system_prompt_ui, 
        inputs=[mode_dropdown], 
        outputs=[sys_prompt_display]
    )
    
    msg.submit(
        fn=chat_logic, 
        inputs=[msg, chatbot, mode_dropdown, temp_slider], 
        outputs=[msg, chatbot]
    )

if __name__ == "__main__":
    # Theme safely placed in the launch method! 🎨
    demo.launch(theme=gr.themes.Soft())