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
        }
        .contact-form-container {
            width: 30%;
            margin-left: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Create a container for the chatbot
st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
st.title("💬 Chatbot")

# ... (rest of the chatbot code remains the same)

# Create a container for the contact form
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
