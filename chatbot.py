import streamlit as st
import requests
import json

class OllamaAPI:
    def __init__(self, base_url: str = "http://127.0.0.1:11434"):
        self.base_url = base_url

    def generate_response(self, prompt: str, model: str = "mistral:7b"):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if chunk := json_response.get('response', ''):
                        yield chunk
                        
        except Exception as e:
            yield f"Error: {str(e)}"

def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ollama_api" not in st.session_state:
        st.session_state.ollama_api = OllamaAPI()
    if "chat_visible" not in st.session_state:
        st.session_state.chat_visible = False

def chatbot_ui():
    # Add custom CSS for the chat interface
    st.markdown("""
        <style>
        .floating-chat-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 400px;
            z-index: 1000;
        }
        .chat-header {
            background-color: #2D2D2D;
            color: white;
            padding: 10px;
            border-radius: 10px 10px 0 0;
            cursor: pointer;
        }
        .chat-body {
            background-color: white;
            border-radius: 0 0 10px 10px;
            max-height: 500px;
            overflow-y: auto;
            padding: 15px;
        }
        .user-message {
            background-color: #e3f2fd;
            border-radius: 15px;
            padding: 10px 15px;
            margin: 5px 20% 5px 0;
            color: black;
        }
        .bot-message {
            background-color: #f5f5f5;
            border-radius: 15px;
            padding: 10px 15px;
            margin: 5px 0 5px 20%;
            color: black;
        }
        .chat-input {
            padding: 10px;
            background-color: white;
            border-top: 1px solid #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

    initialize_chat()

    # Create a container for the floating chat
    chat_container = st.container()

    # Chat toggle button
    if st.button("💬 Chat Support", key="chat_toggle"):
        st.session_state.chat_visible = not st.session_state.chat_visible

    if st.session_state.chat_visible:
        with chat_container:
            st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
            
            # Chat header
            st.markdown('<div class="chat-header">Chat Support</div>', unsafe_allow_html=True)
            
            # Chat messages
            st.markdown('<div class="chat-body">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                message_class = "user-message" if message["role"] == "user" else "bot-message"
                st.markdown(
                    f'<div class="{message_class}">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat input
            with st.markdown('<div class="chat-input">', unsafe_allow_html=True):
                user_input = st.text_input("Type your message...", key="user_input")

                if user_input:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Get bot response
                    full_response = ""
                    for chunk in st.session_state.ollama_api.generate_response(user_input):
                        full_response += chunk
                    
                    # Add bot response
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    # Clear input properly
                    del st.session_state["user_input"]
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    chatbot_ui()