import streamlit as st
import http.client
import json

# RapidAPI Details
# Sample info

API_HOST = "llm17.p.rapidapi.com"
API_ENDPOINT = "/chat"
API_KEY = "d77548cc77msh6251129096604d3p15207bjsn7djfai40tbf3a03dc"

def get_chatbot_response(user_input):
    try:
        conn = http.client.HTTPSConnection(API_HOST)
        payload = json.dumps({
            "chatid": "",
            "role": "You are a Helpful Assistant.",
            "message": user_input
        })
        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': API_HOST,
            'Content-Type': "application/json"
        }

        conn.request("POST", API_ENDPOINT, body=payload, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        response_json = json.loads(data)

        return response_json.get("response", "Error: No response from API")  # Adjust key based on actual API response format

    except Exception as e:
        return f"Error: {str(e)}"

def chatbot_page():
    st.markdown("""
        <style>
            .chat-container {
                max-height: 500px;
                overflow-y: auto;
                border-radius: 15px;
                padding: 15px;
                background: #ffffff;
            }
            .user-message {
                background: #0084ff;
                color: white;
                padding: 10px;
                border-radius: 15px;
                margin: 5px 0;
                text-align: right;
            }
            .bot-message {
                background: #e5e5ea;
                color: black;
                padding: 10px;
                border-radius: 15px;
                margin: 5px 0;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("💆‍♂️ Stress Relief Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_placeholder = st.empty()
    user_input = st.text_input("Type your message:", key="user_input", value="").strip()

    if user_input:
        st.session_state.messages.append(("user", user_input))
        bot_response = get_chatbot_response(user_input)
        st.session_state.messages.append(("bot", bot_response))

    chat_html = "<div class='chat-container' id='chatbox'>"
    for role, text in st.session_state.messages:
        chat_html += f"<div class='{role}-message'>{text}</div>"
    chat_html += "</div>"
    
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)
    
    st.markdown("""
        <script>
        var chatbox = document.getElementById('chatbox');
        if (chatbox) {
            chatbox.scrollTop = chatbox.scrollHeight;
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    chatbot_page()