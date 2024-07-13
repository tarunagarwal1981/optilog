import streamlit as st
import openai

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Add custom CSS to position the form on the left and chatbot on the right
st.markdown("""
    <style>
        .main .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .left-column {
            width: 58%;
            float: left;
            padding-right: 2%;
        }
        .right-column {
            width: 40%;
            float: right;
            margin-left: 60%;
        }
        .stApp {
            overflow-x: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns
left_column, right_column = st.columns([6, 4])

# Left column - Form
with left_column:
    st.header("Contact Form")
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    message = st.text_area("Message")
    submit_button = st.button("Submit")

    if submit_button:
        st.success("Form submitted successfully!")

# Right column - Chatbot
with right_column:
    st.title("💬 Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display messages in the chatbot section
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Your message"):
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
