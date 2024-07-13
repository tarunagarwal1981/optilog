import streamlit as st
import openai

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Add the chatbot to the right 30% space
st.markdown("""
<div style="width: 30%; float: right;">
    <h1>💬 Chatbot</h1>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display messages in the chatbot section
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API key not found. Please add your API key to the Streamlit secrets.")
        st.stop()

    # Set the API key for the openai module
    openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message['content']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
st.markdown('</div>', unsafe_allow_html=True)
