import streamlit as st
import pandas as pd
from datetime import datetime, time
import random
import string

# Set page config
st.set_page_config(layout="wide", page_title="Maritime Reporting System")

# Custom CSS to adjust layout
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stNumberInput input {
    width: 100px;
}
</style>
""", unsafe_allow_html=True)

with st.expander("Fuel Consumption", expanded=True):
    st.subheader("Main Engines")
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

def generate_random_vessel_name():
    adjectives = ['Swift', 'Majestic', 'Brave', 'Stellar', 'Royal']
    nouns = ['Voyager', 'Explorer', 'Mariner', 'Adventurer', 'Navigator']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

def generate_random_imo():
    return ''.join(random.choices(string.digits, k=6))

# Define the main function
def main():
    st.title("AI-Enhanced Maritime Reporting System")
    
    # Create two columns: one for the form (70%) and one for the chatbot (30%)
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

        col1, col2 = st.columns(2)
        with col1:
            time_elapsed = st.number_input("Time Elapsed (hours)", min_value=0.0, step=0.1)
        with col2:
            sailing_time = st.number_input("Sailing Time (hours)", min_value=0.0, step=0.1)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            anchor_time = st.number_input("Time at Anchor (hours)", min_value=0.0, step=0.1)
        with col2:
            dp_time = st.number_input("Dynamic Positioning Time (hours)", min_value=0.0, step=0.1)
        with col3:
            ice_time = st.number_input("Operating in Ice Time (hours)", min_value=0.0, step=0.1)
        with col4:
            maneuvering_time = st.number_input("Maneuvering Time (hours)", min_value=0.0, step=0.1)

        col1, col2, col3 = st.columns(3)
        with col1:
            waiting_time = st.number_input("Waiting Time (hours)", min_value=0.0, step=0.1)
        with col2:
            loading_unloading_time = st.number_input("Loading/Unloading Time (hours)", min_value=0.0, step=0.1)
        with col3:
            drifting_time = st.number_input("Drifting Time (hours)", min_value=0.0, step=0.1)

    with st.expander("Position", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            lat_deg = st.number_input("Latitude Degrees", min_value=-90, max_value=90)
        with col2:
            lat_min = st.number_input("Latitude Minutes", min_value=0.0, max_value=60.0, step=0.1)
        with col3:
            lat_dir = st.selectbox("Latitude Direction", ["North", "South"])

        col1, col2, col3 = st.columns(3)
        with col1:
            lon_deg = st.number_input("Longitude Degrees", min_value=-180, max_value=180)
        with col2:
            lon_min = st.number_input("Longitude Minutes", min_value=0.0, max_value=60.0, step=0.1)
        with col3:
            lon_dir = st.selectbox("Longitude Direction", ["East", "West"])

    with st.expander("Cargo", expanded=True):
        cargo_weight = st.number_input("Cargo Weight (mt)", min_value=0.0, step=0.1)

    with st.expander("Fuel Consumption", expanded=True):
        fuel_types = ["LFO", "MGO", "LNG", "Other"]
        
        st.subheader("Main Engines")
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"ME {fuel} Consumption (mt)", min_value=0.0, step=0.1, key=f"me_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("ME Other Fuel Type", key="me_other_type")
        
        st.subheader("Auxiliary Engines")
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"AE {fuel} Consumption (mt)", min_value=0.0, step=0.1, key=f"ae_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("AE Other Fuel Type", key="ae_other_type")
        
        st.subheader("Boilers")
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"Boiler {fuel} Consumption (mt)", min_value=0.0, step=0.1, key=f"boiler_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("Boiler Other Fuel Type", key="boiler_other_type")
        
        st.subheader("Inert Gas Generators and GCUs")
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"Inert Gas {fuel} Consumption (mt)", min_value=0.0, step=0.1, key=f"inert_gas_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("Inert Gas Other Fuel Type", key="inert_gas_other_type")
        
        st.subheader("Incinerators")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Incinerator Other Fuels Consumption (mt)", min_value=0.0, step=0.1, key="incinerator_consumption")
        with col2:
            st.text_input("Incinerator Other Fuels Type", key="incinerator_fuel_type")

    with st.expander("Remaining on Board (ROB)", expanded=True):
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"{fuel} ROB (mt)", min_value=0.0, step=0.1, key=f"rob_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("Other Fuel Type ROB", key="rob_other_type")
        
        st.number_input("Total Fuel ROB (mt)", min_value=0.0, step=0.1, key="total_rob")

    with st.expander("Fuel Allocation", expanded=True):
        st.subheader("Cargo Heating")
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"Cargo Heating {fuel} Consumption (mt)", min_value=0.0, step=0.1, key=f"cargo_heating_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("Cargo Heating Other Fuel Type", key="cargo_heating_other_type")
        
        st.subheader("Cargo Pumps (DPP)")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("DPP Cargo Pump MDO Consumption (mt)", min_value=0.0, step=0.1, key="dpp_cargo_pump_mdo")
        with col2:
            st.number_input("DPP Cargo Pump Other Fuels Consumption (mt)", min_value=0.0, step=0.1, key="dpp_cargo_pump_other")
        st.text_input("DPP Cargo Pump Other Fuels Type", key="dpp_cargo_pump_other_type")
        
        st.subheader("Dynamic Positioning (DP)")
        for fuel in fuel_types:
            col1, col2 = st.columns(2)
            with col1:
                st.number_input(f"DP {fuel} Consumption (mt)", min_value=0.0, step=0.1, key=f"dp_{fuel.lower()}")
            if fuel == "Other":
                with col2:
                    st.text_input("DP Other Fuel Type", key="dp_other_type")

    with st.expander("Machinery", expanded=True):
        st.subheader("Reefer Container")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Reefer Work (kWh)", min_value=0.0, step=0.1, key="reefer_work")
        with col2:
            st.number_input("Reefer SFOC (g/kWh)", min_value=0.0, step=0.1, key="reefer_sfoc")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Reefer Fuel Type", fuel_types, key="reefer_fuel_type")
        with col2:
            st.text_input("Reefer Fuel BDN", key="reefer_fuel_bdn")
        
        st.subheader("Cargo Cooling")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Cargo Cooling Work (kWh)", min_value=0.0, step=0.1, key="cargo_cooling_work")
        with col2:
            st.number_input("Cargo Cooling SFOC (g/kWh)", min_value=0.0, step=0.1, key="cargo_cooling_sfoc")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Cargo Cooling Fuel Type", fuel_types, key="cargo_cooling_fuel_type")
        with col2:
            st.text_input("Cargo Cooling Fuel BDN", key="cargo_cooling_fuel_bdn")
        
        st.subheader("Heating/Discharge Pump")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Heating/Discharge Pump Work (kWh)", min_value=0.0, step=0.1, key="heating_discharge_work")
        with col2:
            st.number_input("Heating/Discharge Pump SFOC (g/kWh)", min_value=0.0, step=0.1, key="heating_discharge_sfoc")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Heating/Discharge Pump Fuel Type", fuel_types, key="heating_discharge_fuel_type")
        with col2:
            st.text_input("Heating/Discharge Pump Fuel BDN", key="heating_discharge_fuel_bdn")
        
        st.subheader("Shore-Side Electricity")
        st.number_input("Shore-Side Electricity Work (kWh)", min_value=0.0, step=0.1, key="shore_side_electricity_work")

    with st.expander("Weather", expanded=True):
        st.subheader("Wind")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Wind Direction (degrees)", min_value=0, max_value=360, step=1, key="wind_direction")
        with col2:
            st.number_input("Wind Speed (knots)", min_value=0.0, step=0.1, key="wind_speed")
        with col3:
            st.number_input("Wind Force (Beaufort)", min_value=0, max_value=12, step=1, key="wind_force")
        
        st.subheader("Sea State")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Sea State Direction (degrees)", min_value=0, max_value=360, step=1, key="sea_state_direction")
        with col2:
            st.number_input("Sea State Force (Douglas scale)", min_value=0, max_value=9, step=1, key="sea_state_force")
        with col3:
            st.number_input("Sea State Period (seconds)", min_value=0.0, step=0.1, key="sea_state_period")
        
        st.subheader("Swell")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Swell Direction (degrees)", min_value=0, max_value=360, step=1, key="swell_direction")
        with col2:
            st.number_input("Swell Height (meters)", min_value=0.0, step=0.1, key="swell_height")
        with col3:
            st.number_input("Swell Period (seconds)", min_value=0.0, step=0.1, key="swell_period")
        
        st.subheader("Current")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Current Direction (degrees)", min_value=0, max_value=360, step=1, key="current_direction")
        with col2:
            st.number_input("Current Speed (knots)", min_value=0.0, step=0.1, key="current_speed")
        
        st.subheader("Temperature")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Air Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1, key="air_temperature")
        with col2:
            st.number_input("Sea Temperature (°C)", min_value=-2.0, max_value=35.0, step=0.1, key="sea_temperature")

    with st.expander("Draft", expanded=True):
        st.subheader("Actual")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Actual Forward Draft (m)", min_value=0.0, step=0.01, key="actual_forward_draft")
        with col2:
            st.number_input("Actual Aft Draft (m)", min_value=0.0, step=0.01, key="actual_aft_draft")
        
        st.subheader("Recommended")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Recommended Forward Draft (m)", min_value=0.0, step=0.01, key="recommended_forward_draft")
        with col2:
            st.number_input("Recommended Aft Draft (m)", min_value=0.0, step=0.01, key="recommended_aft_draft")
        
        st.subheader("Ballast")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Actual Ballast (mt)", min_value=0.0, step=0.1, key="actual_ballast")
        with col2:
            st.number_input("Optimum Ballast (mt)", min_value=0.0, step=0.1, key="optimum_ballast")
        
        st.number_input("Displacement (mt)", min_value=0.0, step=0.1, key="displacement")
        st.number_input("Water Depth (m)", min_value=0.0, step=0.1, key="water_depth")

    with st.expander("Cargo Details", expanded=True):
        st.subheader("Containers")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Total Containers (TEU)", min_value=0, step=1, key="total_containers")
        with col2:
            st.number_input("Full Containers (TEU)", min_value=0, step=1, key="full_containers")
        with col3:
            st.number_input("Full Reefer Containers (TEU)", min_value=0, step=1, key="full_reefer_containers")
        
        st.subheader("People")
        st.number_input("Number of Crew", min_value=0, step=1, key="crew_count")
        
        st.subheader("Vehicles")
        st.number_input("Vehicles (CEU)", min_value=0.0, step=0.1, key="vehicles_ceu")
        
        st.subheader("Deadweight")
        st.number_input("Deadweight Carried (mt)", min_value=0.0, step=0.1, key="deadweight_carried")

    with st.expander("Miscellaneous", expanded=True):
        st.subheader("Water")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Water Bunkered (m³)", min_value=0.0, step=0.1, key="water_bunkered")
        with col2:
            st.number_input("Drinking Water Consumption (m³)", min_value=0.0, step=0.1, key="drinking_water_consumption")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Technical Water Consumption (m³)", min_value=0.0, step=0.1, key="technical_water_consumption")
        with col2:
            st.number_input("Washing Water Consumption (m³)", min_value=0.0, step=0.1, key="washing_water_consumption")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Water Production (m³)", min_value=0.0, step=0.1, key="water_production")
        with col2:
            st.number_input("Water ROB (m³)", min_value=0.0, step=0.1, key="water_rob")
        
        st.number_input("Duration of Water Operations (hours)", min_value=0.0, step=0.1, key="water_operations_duration")

        st.subheader("Speed")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("GPS Speed (knots)", min_value=0.0, step=0.1, key="gps_speed")
        with col2:
            st.number_input("Speed Through Water (knots)", min_value=0.0, step=0.1, key="speed_through_water")

        st.subheader("Machinery")
        st.subheader("Main Engines")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("ME Barometric Pressure (bar)", min_value=0.0, step=0.01, key="me_barometric_pressure")
        with col2:
            st.number_input("ME Air Intake Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1, key="me_air_intake_temp")
        with col3:
            st.number_input("ME Charge Air Coolant Inlet Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1, key="me_charge_air_coolant_inlet_temp")

        for i in range(1, 5):  # Main Engines 1-4
            st.subheader(f"Main Engine {i}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"ME{i} Load (kW)", min_value=0.0, step=0.1, key=f"me{i}_load")
            with col2:
                st.number_input(f"ME{i} Load Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, key=f"me{i}_load_percentage")
            with col3:
                st.number_input(f"ME{i} Speed (RPM)", min_value=0.0, step=0.1, key=f"me{i}_speed")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"ME{i} Propeller Pitch (m)", min_value=0.0, step=0.01, key=f"me{i}_propeller_pitch")
            with col2:
                st.number_input(f"ME{i} Propeller Pitch Ratio", min_value=0.0, step=0.01, key=f"me{i}_propeller_pitch_ratio")
            with col3:
                st.checkbox(f"ME{i} Aux Blower", key=f"me{i}_aux_blower")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"ME{i} Shaft Generator Power (kW)", min_value=0.0, step=0.1, key=f"me{i}_shaft_gen_power")
            with col2:
                st.number_input(f"ME{i} Charge Air Inlet Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1, key=f"me{i}_charge_air_inlet_temp")
            with col3:
                st.number_input(f"ME{i} Scav. Air Pressure (bar)", min_value=0.0, step=0.01, key=f"me{i}_scav_air_pressure")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"ME{i} Pressure Drop Over Scav. Air Cooler (bar)", min_value=0.0, step=0.01, key=f"me{i}_pressure_drop_scav_air_cooler")
            with col2:
                st.number_input(f"ME{i} P max (bar)", min_value=0.0, step=0.1, key=f"me{i}_p_max")
            with col3:
                st.number_input(f"ME{i} P comp (bar)", min_value=0.0, step=0.1, key=f"me{i}_p_comp")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"ME{i} T/C Speed (RPM)", min_value=0.0, step=1.0, key=f"me{i}_tc_speed")
            with col2:
                st.number_input(f"ME{i} Exh. Temp. Before T/C (°C)", min_value=0.0, max_value=1000.0, step=0.1, key=f"me{i}_exh_temp_before_tc")
            with col3:
                st.number_input(f"ME{i} Exh. Temp. After T/C (°C)", min_value=0.0, max_value=1000.0, step=0.1, key=f"me{i}_exh_temp_after_tc")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"ME{i} Current Consumption (mt/hour)", min_value=0.0, step=0.01, key=f"me{i}_current_consumption")
            with col2:
                st.number_input(f"ME{i} SFOC (g/kWh)", min_value=0.0, step=0.1, key=f"me{i}_sfoc")
            with col3:
                st.number_input(f"ME{i} SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1, key=f"me{i}_sfoc_iso_corrected")

        st.subheader("Auxiliary Engines")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("AE Barometric Pressure (bar)", min_value=0.0, step=0.01, key="ae_barometric_pressure")
        with col2:
            st.number_input("AE Air Intake Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1, key="ae_air_intake_temp")
        with col3:
            st.number_input("AE Charge Air Coolant Inlet Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1, key="ae_charge_air_coolant_inlet_temp")

        for i in range(1, 7):  # Auxiliary Engines 1-6
            st.subheader(f"Auxiliary Engine {i}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"AE{i} Load (kW)", min_value=0.0, step=0.1, key=f"ae{i}_load")
            with col2:
                st.number_input(f"AE{i} Charge Air Inlet Temperature (°C)", min_value=-50.0, max_value=100.0, step=0.1, key=f"ae{i}_charge_air_inlet_temp")
            with col3:
                st.number_input(f"AE{i} Charge Air Pressure (bar)", min_value=0.0, step=0.01, key=f"ae{i}_charge_air_pressure")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"AE{i} Pressure Drop Over Charge Air Cooler (bar)", min_value=0.0, step=0.01, key=f"ae{i}_pressure_drop_charge_air_cooler")
            with col2:
                st.number_input(f"AE{i} T/C Speed (RPM)", min_value=0.0, step=1.0, key=f"ae{i}_tc_speed")
            with col3:
                st.number_input(f"AE{i} P max (bar)", min_value=0.0, step=0.1, key=f"ae{i}_p_max")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"AE{i} P comp (bar)", min_value=0.0, step=0.1, key=f"ae{i}_p_comp")
            with col2:
                st.number_input(f"AE{i} Exh. Temp. Before T/C (°C)", min_value=0.0, max_value=1000.0, step=0.1, key=f"ae{i}_exh_temp_before_tc")
            with col3:
                st.number_input(f"AE{i} Exh. Temp. After T/C (°C)", min_value=0.0, max_value=1000.0, step=0.1, key=f"ae{i}_exh_temp_after_tc")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(f"AE{i} Current Consumption (mt/hour)", min_value=0.0, step=0.01, key=f"ae{i}_current_consumption")
            with col2:
                st.number_input(f"AE{i} SFOC (g/kWh)", min_value=0.0, step=0.1, key=f"ae{i}_sfoc")
            with col3:
                st.number_input(f"AE{i} SFOC ISO Corrected (g/kWh)", min_value=0.0, step=0.1, key=f"ae{i}_sfoc_iso_corrected")

        st.subheader("Boilers")
        for i in range(1, 3):  # Boilers 1-2
            st.subheader(f"Boiler {i}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.selectbox(f"Boiler {i} Operation Mode", ["On", "Off"], key=f"boiler{i}_operation_mode")
            with col2:
                st.number_input(f"Boiler {i} Feed Water Flow (m³/min)", min_value=0.0, step=0.01, key=f"boiler{i}_feed_water_flow")
            with col3:
                st.number_input(f"Boiler {i} Steam Pressure (bar)", min_value=0.0, step=0.1, key=f"boiler{i}_steam_pressure")

        st.subheader("Other Systems")
        st.subheader("Cooling Water System")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("SW Pumps in Service", min_value=0, step=1, key="sw_pumps_in_service")
        with col2:
            st.number_input("SW Inlet Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key="sw_inlet_temp")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("SW Outlet Temp (°C)", min_value=-2.0, max_value=35.0, step=0.1, key="sw_outlet_temp")
        with col2:
            st.number_input("Pressure Drop Over Heat Exchanger (bar)", min_value=0.0, step=0.01, key="pressure_drop_heat_exchanger")
        
        st.number_input("Pump Pressure (bar)", min_value=0.0, step=0.1, key="pump_pressure")

        st.subheader("ER Ventilation")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Fans in Service", min_value=0, step=1, key="fans_in_service")
        with col2:
            st.number_input("Waste Air Temp (°C)", min_value=0.0, max_value=100.0, step=0.1, key="waste_air_temp")

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
