import streamlit as st # type: ignore
import requests

# --- Configuration ---
st.set_page_config(
    page_title="Codebase Assistant",
    page_icon="💻",
    layout="wide"
)

BACKEND = "http://localhost:8000"

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Upload & Settings ---
with st.sidebar:
    st.header("🗂️ Project Context")
    st.write("Upload your codebase to begin.")
    
    zip_file = st.file_uploader("Upload Codebase (.zip)", type="zip")
    
    if zip_file and st.button("🚀 Process Codebase", use_container_width=True):
        with st.spinner("Uploading and indexing codebase..."):
            try:
                files = {"file": ("codebase.zip", zip_file, "application/zip")}
                res = requests.post(f"{BACKEND}/upload", files=files)
                
                if res.status_code == 200:
                    st.success("Codebase processed successfully!")

                    repo_id = res.session_id
                    
                    with st.expander("View Details"):
                        st.json(res.json())
                else:
                    st.error(f"Error {res.status_code}: {res.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Is it running?")

    st.divider()
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# --- Main Interface ---
st.title("💻 Codebase Assistant")
st.caption("Ask questions about your uploaded project structure, logic, or implementation.")

# 1. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Chat Input Handler
if prompt := st.chat_input("Ask a question about your code..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing codebase..."):
            try:
                response = requests.post(f"{BACKEND}/ask", json={"question": prompt,"repo_id": repo_id})
                
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer provided.")
                    st.markdown(answer)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.status_code}"
                    st.error(error_msg)
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Is the backend server running?")