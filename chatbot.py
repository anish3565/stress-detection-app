import streamlit as st

def chatbot_ui():
    # Initialize session state variables if they do not exist
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chatbot toggle button
    if st.button("💬 Chat with AI"):
        st.session_state.chat_open = not st.session_state.chat_open  # Toggle chat window

    # Chatbot UI
    if st.session_state.chat_open:
        with st.container():
            st.markdown(
                """
                <style>
                .chat-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 350px;
                    background-color: white;
                    padding: 10px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                }
                .chat-messages {
                    max-height: 250px;
                    overflow-y: auto;
                    padding: 5px;
                    border-bottom: 1px solid #ddd;
                }
                .chat-input {
                    width: 100%;
                    padding: 5px;
                }
                </style>
                <div class="chat-container">
                    <div class="chat-messages">
                """,
                unsafe_allow_html=True,
            )

            # Display previous chat messages
            for msg in st.session_state.messages:
                st.markdown(f"**{msg['role']}:** {msg['content']}")

            st.markdown("</div>", unsafe_allow_html=True)

            # User input for chatbot
            user_input = st.text_input("Type your message here...", key="chat_input")

            # Process input when the user clicks "Send"
            if st.button("Send") and user_input:
                st.session_state.messages.append({"role": "You", "content": user_input})

                # Simulate bot response (Replace with API call)
                bot_response = "I'm here to help! How are you feeling?"  # Replace this with actual API response
                st.session_state.messages.append({"role": "Bot", "content": bot_response})

                # Refresh UI
                st.rerun()

            # Close button
            if st.button("Close Chat"):
                st.session_state.chat_open = False
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# Ensure this script runs only when executed directly (not when imported)
if __name__ == "__main__":
    chatbot_ui()