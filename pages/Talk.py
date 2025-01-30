import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader
import os
import dotenv
import shutil
from groq import Groq


# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
dotenv.load_dotenv(dotenv_path)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

st.set_page_config(page_icon="assets/logo.png", page_title="TalkToDocs")

persist_directory="chromadb"
def clear_chroma_db():
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
        os.makedirs(persist_directory)



# Clear Chroma DB at the start of a new session
if "session_started" not in st.session_state:
    st.session_state.session_started = True
    clear_chroma_db()


st.title("Talk to your Documents")
st.divider()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chunks" not in st.session_state:
    st.session_state.chunks=[]
with st.sidebar:
    st.subheader("Upload Documents:", divider="red")
    
    UPLOAD_DIR = "./uploaded_files"
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    files = st.file_uploader("Upload", type=["pdf", "txt", "docx"], label_visibility="hidden", accept_multiple_files=True)

    if st.button("Upload") and files:
        for file in files:
            path = os.path.join(UPLOAD_DIR, file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            st.write(f"File saved as: {path}")

        with st.spinner("Parsing Documents..."):
            text_splitter = RecursiveCharacterTextSplitter(separators=["\n", "\t"], chunk_size=500, chunk_overlap=100)

            for file in files:
                path = os.path.join(UPLOAD_DIR, file.name)
                file_type = file.type

                try:
                    if "pdf" in file_type:
                        loaded_file = PyMuPDFLoader(path).load()
                    elif "text" in file_type:
                        loaded_file = TextLoader(path).load()
                    elif "document" in file_type:
                        loaded_file = Docx2txtLoader(path).load()  
                    else:
                        st.error(f"❌ Unsupported file type: {file_type}")
                        continue

                    # Process and append chunks
                    file_chunks = text_splitter.split_documents(loaded_file)
                    st.session_state.chunks.extend(file_chunks)
                    st.write(f"✅ Processed {file.name} | Chunks created: {len(file_chunks)}")

                except Exception as e:
                    st.error(f"Error processing file {file.name}: {e}")

        st.write(f"Total chunks generated: {len(st.session_state.chunks)}")

# Check if chunks are available before creating Chroma index
if st.session_state.chunks:
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    library = Chroma.from_documents(st.session_state.chunks, embedding_model, persist_directory=persist_directory)
    retriever = library.as_retriever()

    prompt_template = ChatPromptTemplate(messages=[
        ("system", "You are a helpful AI Assistant who will answer only from the chunks provided here.{chunks}."),
        ("user", "{user_input_text}")
    ])

    model = ChatGroq(model="llama3-8b-8192", api_key=GROQ_API_KEY)
    chain = prompt_template | model | StrOutputParser()

    # Chat history rendering
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message(name="user", avatar="👤"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message(name="assistant", avatar="assets/logo.png"):
                st.write(message["content"])

    user_input_text = st.chat_input("Your message")
    user_input_voice = st.audio_input("Record input")
    
    if user_input_text :
        st.session_state.chat_history.append({"role": "user", "content": user_input_text})

        with st.chat_message(name="user", avatar="👤"):
            st.write(user_input_text)

        with st.spinner("Retrieving..."):
            docs = retriever.invoke(user_input_text)
            ai_response = chain.invoke({"chunks": docs, "user_input_text": user_input_text})

        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

        with st.chat_message(name="assistant", avatar="assets/logo.png"):
            st.write(ai_response)
    elif user_input_voice:
        client = Groq(api_key=GROQ_API_KEY)
        transcription = client.audio.transcriptions.create(
            file=user_input_voice,
            temperature=0,
            model = "whisper-large-v3-turbo",
            response_format="text"
        )
        st.session_state.chat_history.append({"role": "user", "content": transcription})

        with st.chat_message(name="user", avatar="👤"):
            st.write(transcription)

        with st.spinner("Retrieving..."):
            docs = retriever.invoke(transcription)
            ai_response = chain.invoke({"chunks": docs, "user_input_text": transcription})

        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

        with st.chat_message(name="assistant", avatar="assets/logo.png"):
            st.write(ai_response)

else:
    st.warning("Please upload valid documents to generate chunks.")

