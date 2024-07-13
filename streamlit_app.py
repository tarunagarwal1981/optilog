import streamlit as st
import openai

# Set page config at the very beginning
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Get the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Define the structure for the noon report form
NOON_REPORT_FIELDS = [
    ("IMO Number", "text"),
    ("Date (UTC)", "date"),
    ("Time (UTC)", "time"),
    ("Latitude", "number"),
    ("Longitude", "number"),
    ("Distance Over Ground", "number"),
    ("Average Speed", "number"),
    ("Fuel Consumption (MT)", "number"),
    ("Cargo Weight (MT)", "number"),
    ("Weather Conditions", "text"),
]

# Add custom CSS to position the form and chatbot side by side
st.markdown("""
    <style>
        .reportform-container {
            float: left;
            width: 68%;
            padding-right: 2%;
        }
        .chatbot-container {
            float: right;
            width: 30%;
        }
        .stButton > button {
            width: 100%;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.egzxvld5 > div.block-container.css-z5fcl4.egzxvld4 {
            padding-top: 0;
        }
    </style>
""", unsafe_allow_html=True)

def create_noon_report_form():
    with st.container():
        st.markdown('<div class="reportform-container">', unsafe_allow_html=True)
        st.header("Noon Report")
        with st.form("noon_report_form"):
            form_data = {}
            for field, field_type in NOON_REPORT_FIELDS:
                if field_type == "text":
                    form_data[field] = st.text_input(field)
                elif field_type == "number":
                    form_data[field] = st.number_input(field, step=0.1)
                elif field_type == "date":
                    form_data[field] = st.date_input(field)
                elif field_type == "time":
                    form_data[field] = st.time_input(field)
            
            submit_button = st.form_submit_button("Submit Noon Report")
            if submit_button:
                st.success("Noon Report submitted successfully!")
                st.write(form_data)
        st.markdown('</div>', unsafe_allow_html=True)

def create_chatbot():
    with st.container():
        st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
        st.title("💬 Chatbot")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        
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

def main():
    st.title("Maritime Reporting System")
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
        create_noon_report_form()
    
    with col2:
        create_chatbot()

if __name__ == "__main__":
    main()
