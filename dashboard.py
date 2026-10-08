import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Ladywood Environmental Monitor", layout="wide")
st.title("🌱 Ladywood Environmental Risk & Trend Monitor")
st.markdown("Dynamic prioritization matrices and pollutant timeline analytics.")
st.markdown("---")

# 2. Loading Your Actual Dataset Records
raw_data = {
    "Year_Month": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12"],
    "PM10_Average": [11.26, 8.57, 11.98, 7.87, 14.07, 8.82, 8.15, 10.94, 15.04, 10.63, 14.39, 6.68],
    "PM2_5_Average": [6.67, 5.15, 8.55, 4.51, 9.21, 5.18, 4.49, 6.38, 9.16, 6.35, 10.40, 4.20],
    "NO2_Average": [18.51, 15.23, 16.95, 9.93, 13.22, 7.87, 9.92, 7.99, 14.38, 18.88, 25.18, 14.62],
    "Ozone_Average": [52.10, 55.27, 59.10, 74.60, 66.82, 66.39, 52.93, 61.33, 58.65, 42.51, 26.22, 43.36]
}
df = pd.DataFrame(raw_data)

# 3. Sidebar Configuration Filter
st.sidebar.header("🎛️ Analysis Controls")
target_pollutant = st.sidebar.selectbox(
    "Select Target Indicator Tracker:",
    ["PM10_Average", "PM2_5_Average", "NO2_Average", "Ozone_Average"]
)

# 4. Core Priority Scorecard Engine (Top Row Metrics)
m1, m2, m3 = st.columns(3)
with m1:
    peak_val = df[target_pollutant].max()
    st.metric(label=f"🚨 Peak {target_pollutant} Level", value=f"{peak_val:.2f}", delta="Risk Prioritization Factor")
with m2:
    avg_val = df[target_pollutant].mean()
    st.metric(label=f"📊 Dataset Baseline Mean", value=f"{avg_val:.2f}")
with m3:
    st.metric(label="🗓️ Active Timeline Horizons", value=f"{len(df)} Months Monitored")

st.markdown("---")

# 5. Dashboard Grid: Data Spreadsheet Split with Timeline Performance Chart
left_panel, right_panel = st.columns(2)

with left_panel:
    st.subheader("📋 Core Pollutant Matrix Data")
    st.dataframe(df[["Year_Month", "PM10_Average", "PM2_5_Average", "NO2_Average", "Ozone_Average"]], use_container_width=True)

with right_panel:
    st.subheader("📈 Environmental Degradation Trend Timeline")
    # Streamlit's built-in chart engine boots instantly without any network delays!
    st.line_chart(data=df, x="Year_Month", y=target_pollutant, use_container_width=True)
