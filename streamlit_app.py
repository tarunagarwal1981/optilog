import streamlit as st
import openai

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Add custom CSS to position the chatbot on the right 40-50% of the page
st.markdown("""
    <style>
        .main .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .container {
            display: flex;
            justify-content: flex-end;
        }
        .chatbot {
            width: 40%;
            margin-right: 5%;
        }
    </style>
    <div class="container">
        <div class="chatbot">
            <h1>💬 Chatbot</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Create a container for the chat messages
chat_container = st.container()

# Display messages in the chatbot section
with chat_container:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

# Move the chat input to the bottom of the page
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API key not found. Please add your API key to the Streamlit secrets.")
        st.stop()

    # Set the API key for the openai module
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with chat_container:
        st.chat_message("user").write(prompt)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message['content']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    with chat_container:
        st.chat_message("assistant").write(msg)
