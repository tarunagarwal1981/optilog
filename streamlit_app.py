import streamlit as st
import openai

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Add links and information to the left 70% space
st.markdown("""
<div style="width: 70%; float: left;">
    <p><a href="https://platform.openai.com/account/api-keys">Get an OpenAI API key</a></p>
    <p><a href="https://github.com/streamlit/llm-examples/blob/main/Chatbot.py">View the source code</a></p>
    <p><a href="https://codespaces.new/streamlit/llm-examples?quickstart=1"><img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces"></a></p>
</div>
""", unsafe_allow_html=True)

# Add the chatbot to the right 30% space
st.markdown("""
<div style="width: 30%; float: right;">
    <h1>💬 Chatbot</h1>
</div>
""", unsafe_allow_html=True)

# Clear floating elements
st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display messages in the chatbot section
st.markdown('<div style="width: 30%; float: right;">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API key not found. Please add your API key to the Streamlit secrets.")
        st.stop()

    # Set the API key for the openai module
    openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown('<div style="width: 30%; float: right;">', unsafe_allow_html=True)
    st.chat_message("user").write(prompt)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message['content']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.markdown('</div>', unsafe_allow_html=True)

