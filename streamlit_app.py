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
            padding-bottom: 5rem;
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
            position: relative;
            height: calc(100vh - 80px);
        }
        .chat-container {
            height: calc(100% - 70px);
            overflow-y: auto;
            padding-bottom: 70px;
        }
        .input-container {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #0E1117;
            padding: 1rem 0;
        }
        #root > div:nth-child(1) > div > div > div > div > section.main.css-uf99v8.ea3mdgi5 {
            overflow-y: hidden;
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
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Input container
    input_container = st.container()

    with input_container:
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        prompt = st.chat_input("Your message")
        st.markdown('</div>', unsafe_allow_html=True)

        if prompt:
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

# Ensure the page doesn't reload on form submission
st.markdown("""
    <script>
        var form = window.parent.document.querySelector("form");
        function handleSubmit(event) {
            event.preventDefault();
        }
        form.addEventListener('submit', handleSubmit);
    </script>
""", unsafe_allow_html=True)
