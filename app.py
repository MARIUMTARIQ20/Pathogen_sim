import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load Data
patients = pd.read_csv('patients_data.csv')
hospitals = pd.read_csv('hospital_data.csv')
antibiotic_resistance = pd.read_csv('antibiotic_resistance.csv')
infection_spread = pd.read_csv('infection_spread.csv')
mortality_recovery = pd.read_csv('mortality_recovery.csv')

# Fix Dates
infection_spread["Date"] = pd.date_range(start="2024-06-01", periods=len(infection_spread), freq="D")
infection_spread["Date"] = np.random.choice(infection_spread["Date"], size=len(infection_spread), replace=False)

# Streamlit App
st.set_page_config(page_title="Pathogen Sim Dashboard", layout="wide")

# Custom Theme
custom_colors = ["#FFB6C1", "#87CEEB", "#FFD700", "#98FB98"]
st.markdown("<style>body { font-size: 16px; }</style>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Infection Trends", "🏥 Hospital Comparisons", "💊 Antibiotic Resistance", "🌡️ Mortality & Recovery"])

with tab1:
    st.subheader("📈 Infection Spread Over Time")
    fig = px.line(infection_spread, x="Date", y="Number_of_Cases", color="Hospital", 
                  markers=True, title="Infection Cases Over Time",
                  color_discrete_sequence=custom_colors)
    fig.update_traces(mode="lines+markers", line_shape="spline")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🏥 Infection Rates by Hospital")
    fig = px.bar(hospitals, x="Name", y="Infection_Rate", color="Name",
                 title="Hospital Infection Rates",
                 color_discrete_sequence=custom_colors)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("💊 Antibiotic Resistance Breakdown")
    fig = px.pie(antibiotic_resistance, names="Antibiotic", values="Resistance_Percentage",
                 title="Antibiotic Resistance Distribution",
                 color_discrete_sequence=custom_colors)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("🌡️ Mortality vs Recovery Heatmap")
    fig = px.imshow(mortality_recovery.pivot(index="Date", columns="Hospital", values="Mortality_Rate"),
                    color_continuous_scale=custom_colors[:3], title="Mortality Rate Heatmap")
    st.plotly_chart(fig, use_container_width=True)
