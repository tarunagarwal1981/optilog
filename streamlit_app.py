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
        .stApp {
            display: flex;
            flex-direction: row;
        }
        .chatbot-container {
            width: 50%;
            margin-left: 20px;
            overflow-y: scroll;
            height: 600px;
        }
        .contact-form-container {
            width: 30%;
            margin-left: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2)

# Create a container for the chatbot in the first column
with col1:
    st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)

    # Create a container for the chat history
    chat_history = st.container()

    # Create a text input box for user input
    user_input = st.text_input("Type your message...")

    # Create a button to submit the user input
    submit_button = st.button("Send")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # When the user submits their input, update the chat history
    if submit_button:
        if not openai_api_key:
            st.info("OpenAI API key not found. Please add your API key to the Streamlit secrets.")
            st.stop()

        # Set the API key for the openai module
        openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        
        msg = response.choices[0].message['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    # Display the chat history
    with chat_history:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    # Display the text input box and button
    st.write(user_input)
    st.write(submit_button)

    st.markdown('</div>', unsafe_allow_html=True)

# Create a container for the contact form in the second column
with col2:
    st.markdown('<div class="contact-form-container">', unsafe_allow_html=True)
    st.title("📧 Contact Form")

    contact_form = st.form(key="contact_form")
    name = contact_form.text_input("Name")
    email = contact_form.text_input("Email")
    message = contact_form.text_area("Message")
    submit_button = contact_form.form_submit_button("Submit")

    if submit_button:
        st.success("Form submitted successfully!")
        # Add your form submission logic here

    st.markdown('</div>', unsafe_allow_html=True)
