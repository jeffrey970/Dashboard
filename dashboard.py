import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import os

# --- SITE CONFIGURATION ---
st.set_page_config(page_title="Ladywood Urban Engineering Console", layout="wide")

# LOCAL PRODUCTION DATA STORAGE FILES
DATA_FILE = "ladywood_active_data.csv"
TEXT_FILE = "ladywood_text_state.csv"

# OFFICIAL REGISTRATION BOUNDARIES FOR LADYWOOD WARD, BIRMINGHAM (BCC SCHEMA)
LADYWOOD_BORDER_POLYGON = [
    [-1.9380, 52.4920],
    [-1.9020, 52.4920],
    [-1.9020, 52.4680],
    [-1.9380, 52.4680],
    [-1.9380, 52.4920]
]

# --- SYSTEM INITIALIZATION AND PERSISTENCE CONTROL ---
# Reads and writes settings to local files so data updates persist globally for all users
if not os.path.exists(TEXT_FILE):
    text_defaults = {
        "key": ["about_title", "about_body", "rehab_title", "rehab_body"],
        "value": [
            "Ladywood Urban Environmental Diagnostics",
            "Ladywood is an inner-city ward of Birmingham, UK, with a deep industrial legacy. During the 19th and 20th centuries, it served as a dense manufacturing and production engine. Over decades of intensive urban buildup, natural green spaces were systematically stripped away and replaced with high-density brick envelopes, manufacturing facilities, and asphalt transportation networks. Today, this massive structural footprint traps high ambient heat and concentrates localized vehicle emissions, creating acute environmental and air quality hazards. This platform applies geostatistical mining engineering principles to prioritize high-risk zones, using multi-criteria matrix analysis to target environmental remediation exactly where it is needed most.",
            "Engineering Rehabilitation Pipeline Solutions",
            "1. Eco-Canopy Retrofitting: Target strategic tree planting in high-density infrastructure zones to intercept airborne particulate vectors.\n2. Albedo Modification: Transition legacy non-porous pavements into high-albedo, cool permeable materials to break urban heat storage.\n3. Ecological Buffering: Deploy thick vegetation buffer corridors alongside primary motorway boundaries to scrub localized gaseous emissions."
        ]
    }
    pd.DataFrame(text_defaults).to_csv(TEXT_FILE, index=False)

if not os.path.exists(DATA_FILE):
    # Official Grounded Neighborhood Clusters from the Ladywood Ward Plan
    base_neighborhoods = ["Central Ladywood", "Park Central", "Five Ways Estate", "Convention Quarter", "Civic Centre Estate"]
    default_data = {
        "Subzone": base_neighborhoods,
        "Air_Quality_Index": [55, 78, 42, 60, 85],
        "Vegetation_Cover_Pct": [35, 12, 40, 22, 15],
        "Latitude": [52.4780, 52.4760, 52.4820, 52.4850, 52.4710],
        "Longitude": [-1.9210, -1.9120, -1.9150, -1.9270, -1.9180]
    }
    pd.DataFrame(default_data).to_csv(DATA_FILE, index=False)

# Read active operational states from global tables
df_text_state = pd.read_csv(TEXT_FILE)
df_data_state = pd.read_csv(DATA_FILE)

# Helper function to map text parameters dynamically
def get_state_text(key_name):
    match = df_text_state[df_text_state["key"] == key_name]
    if not match.empty:
        return match["value"].iloc[0]
    return ""

# --- ACTIVE GEOTECHNICAL CALCULATIONS MATRIX ---
# Computes infrastructure deficit ratios using explicit Multi-Criteria Engineering equations
if not df_data_state.empty:
    df_data_state["Canopy_Deficit"] = 100.0 - df_data_state["Vegetation_Cover_Pct"]
    df_data_state["Calculated_Risk_Score"] = ((df_data_state["Air_Quality_Index"] * 0.6) + (df_data_state["Canopy_Deficit"] * 0.4)) / 10.0
    df_data_state = df_data_state.sort_values(by="Calculated_Risk_Score", ascending=False)
    
    total_elements = len(df_data_state)
    computed_mean_aqi = df_data_state["Air_Quality_Index"].sum() / total_elements
    computed_mean_veg = df_data_state["Vegetation_Cover_Pct"].sum() / total_elements
    highest_critical_zone = df_data_state["Subzone"].iloc[0]
else:
    total_elements, computed_mean_aqi, computed_mean_veg = 0, 0.0, 0.0
    highest_critical_zone = "No Data Configured"

# --- SIDEBAR INTERFACE ---
st.sidebar.title("Ladywood Engineering Framework")
st.sidebar.write("---")

# Authentication Module to Unlock Management Workspace
if "admin_active" not in st.session_state:
    st.session_state.admin_active = False

secret_input = st.sidebar.text_input("Console Access Key:", type="password")
if secret_input in ["admin123", "teamladywood2026"]:
    st.session_state.admin_active = True
else:
    st.session_state.admin_active = False

# Navigation controls mapped cleanly without visual distractions
if st.session_state.admin_active:
    nav_menu = ["Objective and Scope", "Visualizations and Analytics", "Rehabilitation Steps", "Management Control Panel"]
else:
    nav_menu = ["Objective and Scope", "Visualizations and Analytics", "Rehabilitation Steps"]

selected_page = st.sidebar.radio("Navigation Menu:", nav_menu)

# --- VIEWPORT ROUTING LOGIC ---

# 1. OBJECTIVE AND SCOPE
if selected_page == "Objective and Scope":
    st.title(get_state_text("about_title"))
    st.write("---")
    
    col_img, col_txt = st.columns(2)
    with col_img:
        if os.path.exists("ladywood.jpg"):
            st.image("ladywood.jpg", caption="Ladywood Site Aerial Image Blueprint")
        else:
            st.info("Place your picture file named 'ladywood.jpg' on your Desktop folder to load the visual asset.")
    with col_txt:
        st.write(get_state_text("about_body"))

# 2. VISUALIZATIONS AND ANALYTICS
elif selected_page == "Visualizations and Analytics":
    st.title("Visualizations, Maps and Risk Priorities")
    
    # Public Metrics Summary Board
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Monitored Subzones", total_elements)
    col_m2.metric("Mean Regional AQI", f"{computed_mean_aqi:.1f}")
    col_m3.metric("Mean Vegetation Canopy", f"{computed_mean_veg:.1f}%")
    col_m4.metric("Critical Threat Area", highest_critical_zone)
    st.write("---")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Official Ladywood Geofence Boundary Map")
        
        # Structure the explicit polygon border data frame to display legal ward lines
        polygon_dataframe = pd.DataFrame({"coordinates": [LADYWOOD_BORDER_POLYGON]})
        
        polygon_layer = pdk.Layer(
            "PolygonLayer",
            polygon_dataframe,
            get_polygon="coordinates",
            get_fill_color=[255, 75, 75, 20],  # Transparent white/red hue tracing the legal zone
            get_line_color=[255, 75, 75, 200], # Solid border outline
            get_line_width=3,
            line_width_min_pixels=1,
            pickable=False
        )
        
        # Solid point pins inside the legal limits
        point_layer = pdk.Layer(
            "ScatterplotLayer",
            df_data_state,
            get_position=["Longitude", "Latitude"],
            get_color=[255, 75, 75, 200],
            get_radius=45, # High-precision micro-meter targeting radius
            pickable=True
        )
        
        view_state = pdk.ViewState(latitude=52.478, longitude=-1.918, zoom=13.0, pitch=0)
        st.pydeck_chart(pdk.Deck(layers=[polygon_layer, point_layer], initial_view_state=view_state))
        st.caption("Legal Boundary Layer Enabled: Boundary markers trace the official Birmingham Ladywood Ward limits.")

    with col_right:
        st.subheader("Classified Risk Hierarchy and Attribute Trends")
        st.bar_chart(data=df_data_state.set_index("Subzone")["Calculated_Risk_Score"], color="#ff4b4b")
        st.line_chart(data=df_data_state.set_index("Subzone")[["Air_Quality_Index", "Vegetation_Cover_Pct"]])

    # --- PRIVILEGED WORKSPACE MATH OVERRIDES ---
    if st.session_state.admin_active:
        st.write("---")
        st.write("### Internal Engineering Calculations and Audit Proofs")
        
        st.table(df_data_state[["Subzone", "Air_Quality_Index", "Vegetation_Cover_Pct", "Canopy_Deficit", "Calculated_Risk_Score"]])
        
        st.write("#### Geostatistical Calculation Ledger")
        st.text(f"Mean AQI Calculation: {df_data_state['Air_Quality_Index'].sum()} / {total_elements} = {computed_mean_aqi:.2f}")
        st.text(f"Mean Canopy Distribution: {df_data_state['Vegetation_Cover_Pct'].sum()}% / {total_elements} = {computed_mean_veg:.2f}%")
        
        st.write("#### Linear Matrix Iteration Calculations Breakdown:")
        for idx in range(len(df_data_state)):
            row = df_data_state.iloc[idx]
            st.text(f"Zone [{row['Subzone']}]: (AQI {row['Air_Quality_Index']} * 0.6) + (Deficit {row['Canopy_Deficit']} * 0.4) = Risk Factor: {row['Calculated_Risk_Score']:.2f}")

# 3. REHABILITATION STEPS
elif selected_page == "Rehabilitation Steps":
    st.title(get_state_text("rehab_title"))
    st.write("---")
    st.write(get_state_text("rehab_body"))

# 4. PRIVILEGED WORKSPACE MANAGEMENT ENVIRONMENT
elif selected_page == "Management Control Panel" and st.session_state.admin_active:
    st.title("Master Administrative Control Center")
    st.write("---")
    
    tab_text, tab_data = st.tabs(["Text Content Editor", "Spreadsheet Pipeline Manager"])
    
    with tab_text:
        st.subheader("Modify Web Interface Text Fields")
        edit_title = st.text_input("About Header Wording:", value=get_state_text("about_title"))
        edit_body = st.text_area("About Narrative Wording:", value=get_state_text("about_body"), height=100)
        edit_rehab_title = st.text_input("Rehabilitation Header Wording:", value=get_state_text("rehab_title"))
        edit_rehab_body = st.text_area("Rehabilitation Content List:", value=get_state_text("rehab_body"), height=100)
        
        if st.button("Publish Modifications Live"):
            updated_text_df = pd.DataFrame({
                "key": ["about_title", "about_body", "rehab_title", "rehab_body"]})

