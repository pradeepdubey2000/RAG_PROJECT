import streamlit as st
from streamlit import session_state
import time
import base64
import os 
from vector import EmbeddingManager
from chatbot import ChatbotManager

# Set the page config as the first command
st.set_page_config(
    page_title='LLAMA-LEX APP',
    layout='wide',
    initial_sidebar_state='expanded',
)


def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

if "temp_df_path" not in st.session_state:
    st.session_state['temp_pdf_path'] = None

if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Custom CSS for the app layout
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            color: black;  /* Change sidebar text color to black */
        }
        .css-18e3th9 {
            padding-top: 2rem;
            color: white;  /* Change this text color to black */
        }
        .main-header {
            background-color: #003366;
            color: white;  /* Change main header text color to black */
            padding: 1rem;
            border-radius: 10px;
        }
        .main-container {
            background-color: #f9f9f9;
            padding: 2rem;
            border-radius: 10px;
            color: black;  /* Change main container text color to black */
        }
        .col-header {
            background-color: #ff6347;
            color: black;  /* Change column header text color to black */
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }
        .pdf-preview {
            background-color: #f0f0f5;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            color: black;  /* Change PDF preview text color to black */
        }
        .success-alert {
            color: green;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("logo.png", use_column_width=True)
    st.markdown("<h3>📚 Your Personal Document Assistant</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation Menu
    menu = ["🏠 Home", "🤖 Chatbot"]
    choice = st.selectbox("Navigate", menu)

# Home Page
if choice == "🏠 Home":
    st.markdown("""
        <div class='main-header'>
            <h1>📄 Welcome to LLAMA-LEX APP!</h1>
            <p>🚀Real-Time Document Interaction System Using RAG and LLAMA 3.2</p>
        </div>
        <div class='main-container'>
            <p><strong>Built using Open Source Stack (Llama 3.2, BGE Embeddings, and Qdrant running locally within a Docker Container.)</strong></p>
            <ul>
                <li><strong>Upload Documents</strong>: Easily upload your PDF documents.</li>
                <li><strong>Summarize</strong>: Get concise summaries of your documents.</li>
                <li><strong>Chat</strong>: Interact with your documents through our intelligent chatbot.</li>
            </ul>
            <p>Enhance your document management experience with LLAMA-LEX! 😊</p>
        </div>
    """, unsafe_allow_html=True)

# Chatbot Page
elif choice == "🤖 Chatbot":
    st.markdown("<div class='main-header'><h1>🤖 Chatbot Interface (Llama 3.2 RAG 🦙)</h1></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Column 1: File Uploader and Preview
    with col1:
        st.markdown("<div class='col-header'>📂 Upload Document</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
        if uploaded_file is not None:
            st.markdown("<p class='success-alert'>📄 File Uploaded Successfully!</p>", unsafe_allow_html=True)
            st.markdown(f"**Filename:** {uploaded_file.name}")
            st.markdown(f"**File Size:** {uploaded_file.size} bytes")

            # Display PDF preview using displayPDF function
            st.markdown("<div class='pdf-preview'>### 📖 PDF Preview</div>", unsafe_allow_html=True)
            displayPDF(uploaded_file)

            # Save the uploaded file to a temporary location
            temp_pdf_path = "temp.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state['temp_pdf_path'] = temp_pdf_path

    # Column 2: Create Embeddings
    with col2:
        st.markdown("<div class='col-header'>🧠 Embeddings</div>", unsafe_allow_html=True)
        create_embeddings = st.checkbox("✅ Create Embeddings")
        if create_embeddings:
            if st.session_state['temp_pdf_path'] is None:
                st.warning("⚠️ Please upload a PDF first.")
            else:
                try:
                    embeddings_manager = EmbeddingManager(
                        model_name="BAAI/bge-small-en",
                        device="cpu",
                        encode_kwargs={"normalize_embeddings": True},
                        qdrant_url="http://localhost:6333",
                        collection_name="vector_db"
                    )

                    with st.spinner("🔄 Embeddings are in process..."):
                        result = embeddings_manager.create_embeddings(st.session_state['temp_pdf_path'])
                        time.sleep(1)  # Optional: To show spinner for a bit longer
                    st.success(result)

                    # Initialize ChatbotManager after embeddings are created
                    if st.session_state['chatbot_manager'] is None:
                        st.session_state['chatbot_manager'] = ChatbotManager(
                            model_name="BAAI/bge-small-en",
                            device="cpu",
                            encode_kwargs={"normalize_embeddings": True},
                            llm_model="llama3.2:3b",
                            llm_temperature=0.7,
                            qdrant_url="http://localhost:6333",
                            collection_name="vector_db"
                        )
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    # Column 3: Chatbot Interface
    with col3:
        st.markdown("<div class='col-header'>💬 Chat with Document</div>", unsafe_allow_html=True)

        if st.session_state['chatbot_manager'] is None:
            st.info("🤖 Please upload a PDF and create embeddings to start chatting.")
        else:
            # Display existing messages
            for msg in st.session_state['messages']:
                st.chat_message(msg['role']).markdown(msg['content'])

            # User input
            if user_input := st.chat_input("Type your message here..."):
                st.chat_message("user").markdown(user_input)
                st.session_state['messages'].append({"role": "user", "content": user_input})

                with st.spinner("🤖 Responding..."):
                    try:
                        answer = st.session_state['chatbot_manager'].get_response(user_input)
                        time.sleep(1)
                    except Exception as e:
                        answer = f"⚠️ An error occurred while processing your request: {e}"

                st.chat_message("assistant").markdown(answer)
                st.session_state['messages'].append({"role": "assistant", "content": answer})
