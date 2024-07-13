import streamlit as st
import openai

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Add custom CSS to position the chatbot on the right 40% of the page, add form on the left, and fix chatbot input at bottom
st.markdown("""
    <style>
        .main .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .row-widget.stButton {
            text-align: center;
        }
        .left-column {
            width: 58%;
            float: left;
            padding-right: 2%;
        }
        .right-column {
            width: 40%;
            float: right;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        .chat-container {
            flex-grow: 1;
            overflow-y: auto;
            padding-bottom: 5rem;
        }
        .input-container {
            position: fixed;
            bottom: 3rem;
            right: 1rem;
            width: 38%;
            background-color: #0E1117;
            padding: 1rem 0;
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

    # Chat container
    chat_container = st.container()

    # Display messages in the chatbot section
    with chat_container:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    # Input container
    input_container = st.container()

    with input_container:
        if prompt := st.chat_input("Your message"):
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

# Apply custom CSS to fix input at bottom
st.markdown("""
    <style>
        .input-container {
            position: fixed;
            bottom: 3rem;
            right: 1rem;
            width: 38%;
            background-color: #0E1117;
            padding: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)
