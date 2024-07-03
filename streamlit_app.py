import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Define the main function
def main():
    st.title("AI-Enhanced Maritime Reporting System")

    # Create two columns: one for the form (70%) and one for the chatbot (30%)
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        create_form()

    with col2:
        create_chatbot()

def create_form():
    st.header("New Noon Report")
    
    # Create form fields
    imo_number = st.text_input("IMO Number")
    utc_date = st.date_input("UTC Date")
    utc_time = st.time_input("UTC Time")
    voyage_from = st.text_input("From (Departure Port)")
    voyage_to = st.text_input("To (Arrival Port)")
    event_name = st.selectbox("Event Name", ["Departure", "Arrival", "ArrivalSTS", "DepartureSTS", "Noon", "SOSP", "EOSP"])
    
    time_since_last_report = st.number_input("Time Since Previous Report (hours)", min_value=0.0, step=0.1)
    distance = st.number_input("Distance over Ground (NM)", min_value=0.0, step=0.1)
    
    latitude_degree = st.number_input("Latitude (Degrees)", min_value=-90, max_value=90, step=1)
    latitude_minutes = st.number_input("Latitude (Minutes)", min_value=0.0, max_value=60.0, step=0.1)
    latitude_direction = st.selectbox("Latitude (Direction)", ["North", "South"])
    
    longitude_degree = st.number_input("Longitude (Degrees)", min_value=-180, max_value=180, step=1)
    longitude_minutes = st.number_input("Longitude (Minutes)", min_value=0.0, max_value=60.0, step=0.1)
    longitude_direction = st.selectbox("Longitude (Direction)", ["East", "West"])
    
    cargo_mt = st.number_input("Cargo Weight (mt)", min_value=0.0, step=0.1)
    
    # Fuel consumption fields
    st.subheader("Fuel Consumption")
    me_consumption_hfo = st.number_input("ME HFO Consumption (mt)", min_value=0.0, step=0.1)
    me_consumption_lfo = st.number_input("ME LFO Consumption (mt)", min_value=0.0, step=0.1)
    me_consumption_mgo = st.number_input("ME MGO Consumption (mt)", min_value=0.0, step=0.1)
    
    ae_consumption_hfo = st.number_input("AE HFO Consumption (mt)", min_value=0.0, step=0.1)
    ae_consumption_lfo = st.number_input("AE LFO Consumption (mt)", min_value=0.0, step=0.1)
    ae_consumption_mgo = st.number_input("AE MGO Consumption (mt)", min_value=0.0, step=0.1)
    
    # ROB fields
    st.subheader("Remaining on Board (ROB)")
    hfo_rob = st.number_input("HFO ROB (mt)", min_value=0.0, step=0.1)
    lfo_rob = st.number_input("LFO ROB (mt)", min_value=0.0, step=0.1)
    mgo_rob = st.number_input("MGO ROB (mt)", min_value=0.0, step=0.1)
    
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
