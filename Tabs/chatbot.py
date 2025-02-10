import streamlit as st
import http.client
import json

# RapidAPI Details
API_HOST = "llm17.p.rapidapi.com"
API_ENDPOINT = "/chat"
API_KEY = ""

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

        return response_json.get("response", "Sorry, I couldn't understand that.")

    except Exception as e:
        return f"Error: {str(e)}"

def chatbot_page():
    st.markdown("""
        <style>
        /* Floating Chat UI */
        .floating-chat-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            padding: 15px;
            # background: white;
            font-family: Arial, sans-serif;
        }

        /* Chat Header */
        .chat-header {
            background: Gray;
            color: white;
            padding: 10px;
            border-radius: 15px 15px 0 0;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        }

        /* Chat Body */
        .chat-body {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }

        /* Message container */
        .message-container {
            display: flex;
            margin-bottom: 5px;
        }

        /* Messages - Dynamic Width */
        .bot-message, .user-message {
            padding: 10px 15px;
            border-radius: 15px;
            font-size: 14px;
            max-width: 75%; /* Maximum width for readability */
            word-wrap: break-word;
            width: fit-content; /* Dynamic width */
        }

        /* Bot messages (left) */
        .bot-message {
            background: #D1E8FF;
            color: black;
            text-align: left;
            align-self: flex-start;
        }

        /* User messages (right) */
        .user-message {
            background: #4A90E2;
            color: white;
            text-align: right;
            align-self: flex-end;
            margin-left: auto;
        }

        /* Chat Input */
        .chat-input {
            padding: 10px;
            background: white;
            border-top: 1px solid #ddd;
            border-radius: 0 0 15px 15px;
            text-align: center;
        }

        .chat-input input {
            width: 90%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 14px;
            outline: none;
        }
        </style>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">A safe space to talk!😄</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-body">', unsafe_allow_html=True)

    for role, text in st.session_state.messages:
        message_class = "user-message" if role == "user" else "bot-message"
        align_class = "align-self-end" if role == "user" else "align-self-start"

        st.markdown(
            f'<div class="message-container {align_class}">'
            f'<div class="{message_class}">{text}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.text_input("How are you feeling today?", key="user_input")

    if user_input:
        st.session_state.messages.append(("user", user_input))
        bot_response = get_chatbot_response(user_input)
        st.session_state.messages.append(("bot", bot_response))
        del st.session_state["user_input"]
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    chatbot_page()
