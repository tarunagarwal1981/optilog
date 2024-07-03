import streamlit as st
import pandas as pd
from datetime import datetime

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
    # Initialize session state for dynamic title
    if 'report_type' not in st.session_state:
        st.session_state.report_type = "New Report"

    st.header(st.session_state.report_type)
    
    # Vessel Data
    st.subheader("Vessel Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        vessel_name = st.text_input("Vessel Name")
    with col2:
        vessel_imo = st.text_input("Vessel IMO Number")
    with col3:
        vessel_type = st.selectbox("Vessel Type", ["Oil Tanker", "Bulk Carrier", "Container Ship", "Gas Carrier", "Other"])

    # Voyage Data
    st.subheader("Voyage Data")
    col1, col2 = st.columns(2)
    with col1:
        utc_datetime = st.datetime_input("UTC Date and Time")
        local_datetime = st.datetime_input("Local Date and Time")
    with col2:
        voyage_from = st.text_input("From - port code (Departure port)")
        voyage_to = st.text_input("To - port code (Arrival port)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        voyage_type = st.selectbox("Voyage type", ["STS", "One way", "Round trip", "Idle"])
    with col2:
        voyage_number = st.text_input("Voyage Number")
    with col3:
        offhire_reasons = st.text_input("Offhire reasons")

    # Event Type
    st.subheader("Event Type")
    event_types = ["Arrival", "Departure", "Beginofoffhire", "Endofoffhire", "ArrivalSTS", "DepartureSTS", "STS",
                   "Begin canal passage", "End canal passage", "Begin of sea passage", "End of sea passage",
                   "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - Sea passage",
                   "Noon (Position) - Port", "Noon (Position) - River", "Noon (Position) - Stoppage",
                   "ETA update", "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
                   "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"]
    event_type = st.selectbox("Select Event Type", event_types, on_change=update_report_title)

    # Event Data
    st.subheader("Event Data")
    col1, col2 = st.columns(2)
    with col1:
        time_elapsed = st.number_input("Time elapsed since previous event report (hours)", min_value=0.0, step=0.1)
        sailing_time = st.number_input("Sailing time (hours)", min_value=0.0, step=0.1)
        anchor_time = st.number_input("Time at anchor (hours)", min_value=0.0, step=0.1)
        dp_time = st.number_input("Dynamic positioning time (hours)", min_value=0.0, step=0.1)
    with col2:
        ice_time = st.number_input("Operating in ice time (hours)", min_value=0.0, step=0.1)
        maneuvering_time = st.number_input("Maneuvering time (hours)", min_value=0.0, step=0.1)
        waiting_time = st.number_input("Waiting time (hours)", min_value=0.0, step=0.1)
        loading_unloading_time = st.number_input("Loading/Unloading time (hours)", min_value=0.0, step=0.1)
        drifting_time = st.number_input("Drifting time (hours)", min_value=0.0, step=0.1)

    col1, col2 = st.columns(2)
    with col1:
        distance = st.number_input("Distance over Ground (NM)", min_value=0.0, step=0.1)
    
    # Position
    st.subheader("Position")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lat_deg = st.number_input("Latitude Degrees", min_value=-90, max_value=90, step=1)
    with col2:
        lat_min = st.number_input("Latitude Minutes", min_value=0.0, max_value=60.0, step=0.1)
    with col3:
        lat_dir = st.selectbox("Latitude Direction", ["North", "South"])
    with col4:
        lon_deg = st.number_input("Longitude Degrees", min_value=-180, max_value=180, step=1)
    col1, col2, col3 = st.columns(3)
    with col1:
        lon_min = st.number_input("Longitude Minutes", min_value=0.0, max_value=60.0, step=0.1)
    with col2:
        lon_dir = st.selectbox("Longitude Direction", ["East", "West"])

    # Cargo
    st.subheader("Cargo")
    col1, col2, col3 = st.columns(3)
    with col1:
        cargo_weight = st.number_input("Weight of cargo (mt)", min_value=0.0, step=0.1)
        cargo_volume = st.number_input("Volume of cargo (m³)", min_value=0.0, step=0.1)
    with col2:
        passengers = st.number_input("Number of passengers", min_value=0, step=1)
    with col3:
        reefer_20_chilled = st.number_input("Reefer 20 ft. Chilled", min_value=0, step=1)
        reefer_40_chilled = st.number_input("Reefer 40 ft. chilled", min_value=0, step=1)
        reefer_20_frozen = st.number_input("Reefer 20 ft. Frozen", min_value=0, step=1)
        reefer_40_frozen = st.number_input("Reefer 40 ft. Frozen", min_value=0, step=1)

    # Consumption
    st.subheader("Consumption")
    fuel_types = ["HFO", "LFO", "MGO", "MDO", "LPG Propane", "LPG Butane", "LNG", "Methanol", "Ethanol", "Other"]
    
    def create_consumption_section(engine_type):
        st.write(f"{engine_type} Engines")
        cols = st.columns(5)
        for i, fuel in enumerate(fuel_types):
            with cols[i % 5]:
                st.number_input(f"{engine_type} {fuel} consumption (mt)", min_value=0.0, step=0.1, key=f"{engine_type}_{fuel}")
        if engine_type in ["ME", "AE"]:
            with cols[0]:
                st.text_input(f"{engine_type} other fuels type", key=f"{engine_type}_other_type")

    create_consumption_section("ME")
    create_consumption_section("AE")
    create_consumption_section("Boiler")
    create_consumption_section("Inert_gas")
    
    st.write("Incinerators")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Incinerator other fuels consumption (mt)", min_value=0.0, step=0.1)
    with col2:
        st.text_input("Incinerator other fuels type")

    # ROB (Remaining on Board)
    st.subheader("ROB (Remaining on Board)")
    cols = st.columns(5)
    for i, fuel in enumerate(fuel_types):
        with cols[i % 5]:
            st.number_input(f"{fuel} ROB (mt)", min_value=0.0, step=0.1, key=f"ROB_{fuel}")
    with cols[0]:
        st.text_input("Other fuel type (ROB)", key="ROB_other_type")
    with cols[1]:
        st.number_input("Total fuel ROB (mt)", min_value=0.0, step=0.1)

    # Fuel Allocation
    st.subheader("Fuel Allocation")
    allocation_types = ["Cargo heating", "DPP cargo pump", "DP"]
    for alloc_type in allocation_types:
        st.write(f"{alloc_type}")
        cols = st.columns(5)
        for i, fuel in enumerate(fuel_types):
            with cols[i % 5]:
                st.number_input(f"{alloc_type} {fuel} consumption (mt)", min_value=0.0, step=0.1, key=f"{alloc_type}_{fuel}")
        with cols[0]:
            st.text_input(f"{alloc_type} other fuels type", key=f"{alloc_type}_other_type")

    # Machinery
    st.subheader("Machinery")
    machinery_types = ["Reefer container", "Cargo cooling", "Heating/Discharge pump"]
    for mach_type in machinery_types:
        st.write(f"{mach_type}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input(f"{mach_type} Work (kWh)", min_value=0.0, step=0.1, key=f"{mach_type}_work")
        with col2:
            st.number_input(f"{mach_type} SFOC (g/kWh)", min_value=0.0, step=0.1, key=f"{mach_type}_sfoc")
        with col3:
            st.selectbox(f"{mach_type} Fuel type", fuel_types, key=f"{mach_type}_fuel_type")
        with col4:
            st.text_input(f"{mach_type} Fuel BDN", key=f"{mach_type}_fuel_bdn")

    # Shore-Side Electricity
    st.subheader("Shore-Side Electricity")
    st.number_input("Shore-Side Electricity Work (kWh)", min_value=0.0, step=0.1)

    if st.button("Submit"):
        st.success("Report submitted successfully!")

def update_report_title():
    st.session_state.report_type = f"{st.session_state['Select Event Type']} Report"

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
