import streamlit as st
from openai import OpenAI
import datetime

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

def create_noon_report_form():
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

def create_chatbot():
    st.header("AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your maritime reporting?"}]
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Type your message here..."):
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

def main():
    st.set_page_config(layout="wide")
    st.title("Maritime Reporting System")

    # Sidebar for OpenAI API Key
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        
    # Create two columns: one for the form (70%) and one for the chatbot (30%)
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        create_noon_report_form()

    with col2:
        create_chatbot()

if __name__ == "__main__":
    main()
