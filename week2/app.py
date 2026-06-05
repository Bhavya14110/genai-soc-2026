import os
import gradio as gr
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize Embeddings & LLM (Using the updated, supported model)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant") 

# Global vectorstore variable
VECTORSTORE_DIR = "./chroma_store"
vectorstore = None

# Step 4: Handle Persistence Check on Startup
if os.path.exists(VECTORSTORE_DIR):
    vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    initial_status = "✅ Existing document database loaded."
else:
    initial_status = "⚠️ No documents indexed yet. Please upload PDFs."

# Step 2: Build the Indexing Function
def index_documents(pdf_paths: list) -> tuple[str, str]:
    global vectorstore
    if not pdf_paths:
        return "No files uploaded.", gr.update()
    
    total_chunks = 0
    all_splits = []
    
    # Text Splitter config
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    
    for file_path in pdf_paths:
        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Clean metadata (extract just the filename)
        filename = os.path.basename(file_path)
        for doc in docs:
            doc.metadata["source"] = filename
            # PyPDFLoader usually populates "page", but let's ensure it's there
            if "page" not in doc.metadata:
                doc.metadata["page"] = "Unknown"
                
        # Split documents
        splits = text_splitter.split_documents(docs)
        all_splits.extend(splits)
    
    total_chunks = len(all_splits)
    
    # Store in Chroma DB
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    
    print(f"Indexing complete! Total chunks created: {total_chunks}")
    status_msg = f"✅ {len(pdf_paths)} documents indexed — {total_chunks} total chunks."
    
    return status_msg

# Step 3: Build the Retrieval and Answer Function
def ask(chat_history, question: str):
    global vectorstore
    
    # Safety check: Ensure chat_history is a list even on the first run
    chat_history = chat_history or [] 
    
    if vectorstore is None:
        # Fixed to use the dictionary format instead of tuples
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": "Error: No documents indexed. Please upload and index documents first."})
        return chat_history, "", "No context retrieved."

    # Setup Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    retrieved_docs = retriever.invoke(question)
    
    # Format retrieved context
    context_text = ""
    context_display = ""
    
    for i, doc in enumerate(retrieved_docs):
        source = doc.metadata.get("source", "Unknown Source")
        page = doc.metadata.get("page", "Unknown Page")
        content = doc.page_content
        preview = content[:150] + "..." if len(content) > 150 else content
        
        # For the LLM prompt
        context_text += f"\n[Source: {source}, Page: {page}]\n{content}\n"
        
        # For the Gradio UI Display
        context_display += f"**Chunk {i+1}** | `📄 {source} (Page {page})`\n> {preview}\n\n"
        
    # Grounded Prompt
    template = """You are a helpful and factual assistant. Use ONLY the provided context to answer the question. 
    If the answer is not contained in the context, explicitly say "I don't have that information." Do not hallucinate.
    Always cite your sources by mentioning the source file and page number at the end of your answer.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    response = chain.invoke({"context": context_text, "question": question})
    answer = response.content
    
    # Fixed to use the dictionary format instead of tuples
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": answer})
    
    return chat_history, "", context_display

# Step 5: Build the Gradio UI
# Fixed the theme initialization location (removed from here)
with gr.Blocks() as demo:
    gr.Markdown("# 📚 DocBuddy Pro — Q&A Over Multiple PDFs")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_upload = gr.File(file_count="multiple", file_types=[".pdf"], label="Upload PDFs")
            index_btn = gr.Button("⚙️ Index Documents", variant="primary")
            status_label = gr.Label(value=initial_status, label="System Status")
            
        with gr.Column(scale=2):
            # Fixed the Chatbot by removing the unsupported 'type' argument entirely
            chatbot = gr.Chatbot(label="Conversation")
            question_input = gr.Textbox(placeholder="Ask a question about your documents...", label="Your Question")
            ask_btn = gr.Button("Ask", variant="primary")
            
            with gr.Accordion("🔍 Retrieved Context", open=False):
                context_markdown = gr.Markdown("The chunks used for the last query will appear here.")
                
    # Event Listeners
    index_btn.click(
        fn=index_documents,
        inputs=[file_upload],
        outputs=[status_label]
    )
    
    ask_btn.click(
        fn=ask,
        inputs=[chatbot, question_input],
        outputs=[chatbot, question_input, context_markdown]
    )
    
    question_input.submit(
        fn=ask,
        inputs=[chatbot, question_input],
        outputs=[chatbot, question_input, context_markdown]
    )

if __name__ == "__main__":
    # Moved the theme parameter here to satisfy Gradio 6.0!
    demo.launch(theme=gr.themes.Soft())