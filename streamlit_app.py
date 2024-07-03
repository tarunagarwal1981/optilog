import streamlit as st
import pandas as pd
from datetime import datetime, time

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS to make the chatbot sidebar full height
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        width: 30% !important;
        min-width: 30% !important;
    }
    section[data-testid="stSidebar"] > div {
        height: 100vh;
        overflow-y: auto;
    }
    .main > div {
        padding-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Define the main function
def main():
    st.title("AI-Enhanced Maritime Reporting System")

    # Create a sidebar for the chatbot
    with st.sidebar:
        create_chatbot()

    # Main content area for the form
    create_form()

def create_form():
    st.header("New Noon Report")
    
    # Create form fields
    col1, col2 = st.columns(2)
    
    with col1:
        imo_number = st.text_input("IMO Number", key="imo")
    with col2:
        event_name = st.selectbox("Event Name", ["Departure", "Arrival", "ArrivalSTS", "DepartureSTS", "Noon", "SOSP", "EOSP"], key="event")
    
    st.subheader("Voyage Data")
    col1, col2 = st.columns(2)
    with col1:
        utc_date = st.date_input("UTC Date", key="utc_date")
        utc_time = st.time_input("UTC Time", key="utc_time")
        utc_datetime = datetime.combine(utc_date, utc_time)
        st.write(f"UTC Date and Time: {utc_datetime}")
    with col2:
        local_date = st.date_input("Local Date", key="local_date")
        local_time = st.time_input("Local Time", key="local_time")
        local_datetime = datetime.combine(local_date, local_time)
        st.write(f"Local Date and Time: {local_datetime}")
    
    col1, col2 = st.columns(2)
    with col1:
        voyage_from = st.text_input("From (Departure Port)", key="from")
    with col2:
        voyage_to = st.text_input("To (Arrival Port)", key="to")
    
    col1, col2 = st.columns(2)
    with col1:
        time_since_last_report = st.number_input("Time Since Previous Report (hours)", min_value=0.0, step=0.1, key="time_since")
    with col2:
        distance = st.number_input("Distance over Ground (NM)", min_value=0.0, step=0.1, key="distance")
    
    st.subheader("Position")
    col1, col2, col3 = st.columns(3)
    with col1:
        latitude_degree = st.number_input("Latitude (Degrees)", min_value=-90, max_value=90, step=1, key="lat_deg")
    with col2:
        latitude_minutes = st.number_input("Latitude (Minutes)", min_value=0.0, max_value=60.0, step=0.1, key="lat_min")
    with col3:
        latitude_direction = st.selectbox("Latitude (Direction)", ["North", "South"], key="lat_dir")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        longitude_degree = st.number_input("Longitude (Degrees)", min_value=-180, max_value=180, step=1, key="lon_deg")
    with col2:
        longitude_minutes = st.number_input("Longitude (Minutes)", min_value=0.0, max_value=60.0, step=0.1, key="lon_min")
    with col3:
        longitude_direction = st.selectbox("Longitude (Direction)", ["East", "West"], key="lon_dir")
    
    cargo_mt = st.number_input("Cargo Weight (mt)", min_value=0.0, step=0.1, key="cargo")
    
    # Fuel consumption fields
    st.subheader("Fuel Consumption")
    col1, col2, col3 = st.columns(3)
    with col1:
        me_consumption_hfo = st.number_input("ME HFO (mt)", min_value=0.0, step=0.1, key="me_hfo")
    with col2:
        me_consumption_lfo = st.number_input("ME LFO (mt)", min_value=0.0, step=0.1, key="me_lfo")
    with col3:
        me_consumption_mgo = st.number_input("ME MGO (mt)", min_value=0.0, step=0.1, key="me_mgo")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ae_consumption_hfo = st.number_input("AE HFO (mt)", min_value=0.0, step=0.1, key="ae_hfo")
    with col2:
        ae_consumption_lfo = st.number_input("AE LFO (mt)", min_value=0.0, step=0.1, key="ae_lfo")
    with col3:
        ae_consumption_mgo = st.number_input("AE MGO (mt)", min_value=0.0, step=0.1, key="ae_mgo")
    
    # ROB fields
    st.subheader("Remaining on Board (ROB)")
    col1, col2, col3 = st.columns(3)
    with col1:
        hfo_rob = st.number_input("HFO ROB (mt)", min_value=0.0, step=0.1, key="hfo_rob")
    with col2:
        lfo_rob = st.number_input("LFO ROB (mt)", min_value=0.0, step=0.1, key="lfo_rob")
    with col3:
        mgo_rob = st.number_input("MGO ROB (mt)", min_value=0.0, step=0.1, key="mgo_rob")
    
    if st.button("Submit"):
        st.success("Report submitted successfully!")

def create_chatbot():
    st.header("AI Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How can I help you with your report?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate AI response (placeholder)
        response = f"Thank you for your question. Here's a placeholder response to: {prompt}"
        
        # Display AI response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
