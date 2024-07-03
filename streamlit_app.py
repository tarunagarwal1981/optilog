import streamlit as st
import pandas as pd
from datetime import datetime, time
import random
import string

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS to adjust layout and make input boxes smaller
st.markdown("""
<style>
    .reportSection {
        padding-right: 1rem;
    }
    .chatSection {
        padding-left: 1rem;
        border-left: 1px solid #e0e0e0;
    }
    .stButton > button {
        width: 100%;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    h1, h2, h3 {
        margin-top: 0;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .stNumberInput input {
        width: 100px;
    }
</style>
""", unsafe_allow_html=True)

def generate_random_vessel_name():
    adjectives = ['Swift', 'Majestic', 'Brave', 'Stellar', 'Royal']
    nouns = ['Voyager', 'Explorer', 'Mariner', 'Adventurer', 'Navigator']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=6))

def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown('<div class="reportSection">', unsafe_allow_html=True)
        create_form()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chatSection">', unsafe_allow_html=True)
        create_chatbot()
        st.markdown('</div>', unsafe_allow_html=True)

def create_form():
    st.header("New Noon Report")
    
    with st.expander("Vessel Data", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            vessel_name = st.text_input("Vessel Name", value=generate_random_vessel_name())
        with col2:
            vessel_imo = st.text_input("Vessel IMO", value=generate_random_imo())

    with st.expander("Voyage Data", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            local_date = st.date_input("Local Date")
        with col2:
            local_time = st.time_input("Local Time")
        with col3:
            utc_offset = st.selectbox("UTC Offset", [f"{i:+d}" for i in range(-12, 13)])
        
        col1, col2 = st.columns(2)
        with col1:
            voyage_id = st.text_input("Voyage ID")
        with col2:
            segment_id = st.text_input("Segment ID")
        
        col1, col2 = st.columns(2)
        with col1:
            from_port = st.text_input("From Port")
        with col2:
            to_port = st.text_input("To Port")

    with st.expander("Event Data", expanded=True):
        event_types = [
            "Arrival *", "Departure *", "Beginofoffhire *", "Endofoffhire *", "ArrivalSTS *", "DepartureSTS *",
            "STS *", "Begin canal passage", "End canal passage", "Begin of sea passage", "End of sea passage",
            "Begin Anchoring/Drifting", "End Anchoring/Drifting", "Noon (Position) - Sea passage",
            "Noon (Position) - Port", "Noon (Position) - River", "Noon (Position) - Stoppage", "ETA update",
            "Begin fuel change over", "End fuel change over", "Change destination (Deviation)",
            "Begin of deviation", "End of deviation", "Entering special area", "Leaving special area"
        ]
        event_type = st.selectbox("Event Type", event_types)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            time_elapsed = st.number_input("Time Elapsed (hours)", min_value=0.0, step=0.1, format="%.1f")
        with col2:
            sailing_time = st.number_input("Sailing Time (hours)", min_value=0.0, step=0.1, format="%.1f")
        with col3:
            anchor_time = st.number_input("Anchor Time (hours)", min_value=0.0, step=0.1, format="%.1f")
        with col4:
            dp_time = st.number_input("DP Time (hours)", min_value=0.0, step=0.1, format="%.1f")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ice_time = st.number_input("Ice Time (hours)", min_value=0.0, step=0.1, format="%.1f")
        with col2:
            maneuvering_time = st.number_input("Maneuvering (hours)", min_value=0.0, step=0.1, format="%.1f")
        with col3:
            loading_unloading_time = st.number_input("Loading/Unloading (hours)", min_value=0.0, step=0.1, format="%.1f")
        with col4:
            drifting_time = st.number_input("Drifting (hours)", min_value=0.0, step=0.1, format="%.1f")

    with st.expander("Position", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            lat_deg = st.number_input("Latitude Degrees", min_value=-90, max_value=90, step=1)
        with col2:
            lat_min = st.number_input("Latitude Minutes", min_value=0.0, max_value=60.0, step=0.1, format="%.1f")
        with col3:
            lat_dir = st.selectbox("Latitude Direction", ["North", "South"])

        col1, col2, col3 = st.columns(3)
        with col1:
            lon_deg = st.number_input("Longitude Degrees", min_value=-180, max_value=180, step=1)
        with col2:
            lon_min = st.number_input("Longitude Minutes", min_value=0.0, max_value=60.0, step=0.1, format="%.1f")
        with col3:
            lon_dir = st.selectbox("Longitude Direction", ["East", "West"])

    with st.expander("Cargo", expanded=True):
        cargo_weight = st.number_input("Cargo Weight (mt)", min_value=0.0, step=0.1, format="%.1f")

    with st.expander("Fuel Consumption", expanded=True):
        st.subheader("Main Engine")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME LFO (mt)", min_value=0.0, step=0.1, key="me_lfo", format="%.1f")
        with col2:
            st.number_input("ME MGO (mt)", min_value=0.0, step=0.1, key="me_mgo", format="%.1f")
        with col3:
            st.number_input("ME LNG (mt)", min_value=0.0, step=0.1, key="me_lng", format="%.1f")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.number_input("ME Other (mt)", min_value=0.0, step=0.1, key="me_other", format="%.1f")
        with col2:
            st.text_input("ME Other Fuel Type", key="me_other_type")
        
        st.subheader("Auxiliary Engines")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("AE LFO (mt)", min_value=0.0, step=0.1, key="ae_lfo", format="%.1f")
        with col2:
            st.number_input("AE MGO (mt)", min_value=0.0, step=0.1, key="ae_mgo", format="%.1f")
        with col3:
            st.number_input("AE LNG (mt)", min_value=0.0, step=0.1, key="ae_lng", format="%.1f")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.number_input("AE Other (mt)", min_value=0.0, step=0.1, key="ae_other", format="%.1f")
        with col2:
            st.text_input("AE Other Fuel Type", key="ae_other_type")
        
        st.subheader("Boilers")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Boiler LFO (mt)", min_value=0.0, step=0.1, key="boiler_lfo", format="%.1f")
        with col2:
            st.number_input("Boiler MGO (mt)", min_value=0.0, step=0.1, key="boiler_mgo", format="%.1f")
        with col3:
            st.number_input("Boiler LNG (mt)", min_value=0.0, step=0.1, key="boiler_lng", format="%.1f")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.number_input("Boiler Other (mt)", min_value=0.0, step=0.1, key="boiler_other", format="%.1f")
        with col2:
            st.text_input("Boiler Other Fuel Type", key="boiler_other_type")

    with st.expander("Remaining on Board (ROB)", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("LFO ROB (mt)", min_value=0.0, step=0.1, key="rob_lfo", format="%.1f")
        with col2:
            st.number_input("MGO ROB (mt)", min_value=0.0, step=0.1, key="rob_mgo", format="%.1f")
        with col3:
            st.number_input("LNG ROB (mt)", min_value=0.0, step=0.1, key="rob_lng", format="%.1f")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.number_input("Other ROB (mt)", min_value=0.0, step=0.1, key="rob_other", format="%.1f")
        with col2:
            st.text_input("Other Fuel Type ROB", key="rob_other_type")
        
        st.number_input("Total Fuel ROB (mt)", min_value=0.0, step=0.1, key="total_rob", format="%.1f")

    with st.expander("Fuel Allocation", expanded=True):
        st.subheader("Cargo Heating")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Cargo Heating LFO (mt)", min_value=0.0, step=0.1, key="cargo_heating_lfo", format="%.1f")
        with col2:
            st.number_input("Cargo Heating MGO (mt)", min_value=0.0, step=0.1, key="cargo_heating_mgo", format="%.1f")
        with col3:
            st.number_input("Cargo Heating LNG (mt)", min_value=0.0, step=0.1, key="cargo_heating_lng", format="%.1f")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.number_input("Cargo Heating Other (mt)", min_value=0.0, step=0.1, key="cargo_heating_other", format="%.1f")
        with col2:
            st.text_input("Cargo Heating Other Fuel Type", key="cargo_heating_other_type")
        
        st.subheader("Dynamic Positioning (DP)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("DP LFO (mt)", min_value=0.0, step=0.1, key="dp_lfo", format="%.1f")
        with col2:
            st.number_input("DP MGO (mt)", min_value=0.0, step=0.1, key="dp_mgo", format="%.1f")
        with col3:
            st.number_input("DP LNG (mt)", min_value=0.0, step=0.1, key="dp_lng", format="%.1f")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.number_input("DP Other (mt)", min_value=0.0, step=0.1, key="dp_other", format="%.1f")
        with col2:
            st.text_input("DP Other Fuel Type", key="dp_other_type")

    with st.expander("Machinery", expanded=True):
        st.subheader("Main Engine")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Load (kW)", min_value=0.0, step=0.1, key="me_load", format="%.1f")
        with col2:
            st.number_input("ME Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, key="me_load_percentage", format="%.1f")
        with col3:
            st.number_input("ME Speed (RPM)", min_value=0.0, step=0.1, key="me_speed", format="%.1f")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Propeller Pitch (m)", min_value=0.0, step=0.01, key="me_propeller_pitch", format="%.2f")
        with col2:
            st.number_input("ME Propeller Pitch Ratio", min_value=0.0, step=0.01, key="me_propeller_pitch_ratio", format="%.2f")
        with col3:
            st.checkbox("ME Aux Blower", key="me_aux_blower")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Shaft Generator Power (kW)", min_value=0.0, step=0.1, key="me_shaft_gen_power", format="%.1f")
        with col2:
            st.number_input("ME Charge Air Inlet Temp (°C)", min_value=-50.0, max_value=100.0, step=0.1, key="me_charge_air_inlet_temp", format="%.1f")
        with col3:
            st.number_input("ME Scav. Air Pressure (bar)", min_value=0.0, step=0.01, key="me_scav_air_pressure", format="%.2f")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("ME SFOC (g/kWh)", min_value=0.0, step=0.1, key="me_sfoc", format="%.1f")
        with col2:
            st.number_input("ME SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1, key="me_sfoc_iso_corrected", format="%.1f")

        st.subheader("Auxiliary Engines")
        for i in range(1, 4):  # Three Auxiliary Engines
            st.subheader(f"Auxiliary Engine {i}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"AE{i} Load (kW)", min_value=0.0, step=0.1, key=f"ae{i}_load", format="%.1f")
            with col2:
                st.number_input(f"AE{i} Charge Air Inlet Temp (°C)", min_value=-50.0, max_value=100.0, step=0.1, key=f"ae{i}_charge_air_inlet_temp", format="%.1f")
            with col3:
                st.number_input(f"AE{i} Charge Air Pressure (bar)", min_value=0.0, step=0.01, key=f"ae{i}_charge_air_pressure", format="%.2f")
            
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"AE{i} SFOC (g/kWh)", min_value=0.0, step=0.1, key=f"ae{i}_sfoc", format="%.1f")
            with col2:
                st.number_input(f"AE{i} SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1, key=f"ae{i}_sfoc_iso_corrected", format="%.1f")

    with st.expander("Weather", expanded=True):
        st.subheader("Wind")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Wind Direction (degrees)", min_value=0, max_value=360, step=1, key="wind_direction")
        with col2:
            st.number_input("Wind Speed (knots)", min_value=0.0, step=0.1, key="wind_speed", format="%.1f")
        with col3:
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, step=1, key="wind_force")
        
        st.subheader("Sea State")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Sea State Direction (degrees)", min_value=0, max_value=360, step=1, key="sea_state_direction")
        with col2:
            st.number_input("Sea State Force (Douglas scale)", min_value=0, max_value=9, step=1, key="sea_state_force")
        with col3:
            st.number_input("Sea State Period (seconds)", min_value=0.0, step=0.1, key="sea_state_period", format="%.1f")
        
        st.subheader("Swell")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Swell Direction (degrees)", min_value=0, max_value=360, step=1, key="swell_direction")
        with col2:
            st.number_input("Swell Height (meters)", min_value=0.0, step=0.1, key="swell_height", format="%.1f")
        with col3:
            st.number_input("Swell Period (seconds)", min_value=0.0, step=0.1, key="swell_period", format="%.1f")
        
        st.subheader("Current")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Current Direction (degrees)", min_value=0, max_value=360, step=1, key="current_direction")
        with col2:
            st.number_input("Current Speed (knots)", min_value=0.0, step=0.1, key="current_speed", format="%.1f")
        
        st.subheader("Temperature")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Air Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temperature", format="%.1f")
        with col2:
            st.number_input("Sea Temperature (°C)", min_value=-2.0, max_value=35.0, step=0.1, key="sea_temperature", format="%.1f")

    with st.expander("Draft", expanded=True):
        st.subheader("Actual")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Actual Forward Draft (m)", min_value=0.0, step=0.01, key="actual_forward_draft", format="%.2f")
        with col2:
            st.number_input("Actual Aft Draft (m)", min_value=0.0, step=0.01, key="actual_aft_draft", format="%.2f")
        
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement", format="%.1f")
        st.number_input("Water Depth (m)", min_value=0.0, step=0.1, key="water_depth", format="%.1f")

    if st.button("Submit Report"):
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
