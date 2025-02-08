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

# 🔹 Fix Dates for Realistic Spread
infection_spread["Date"] = pd.date_range(start="2024-06-01", periods=len(infection_spread), freq="D")
infection_spread["Date"] = np.random.choice(infection_spread["Date"], size=len(infection_spread), replace=False)

# 🔹 Fix Hospital Names in Mortality & Recovery
hospital_names = ["AKUH", "LNH", "South City Hospital", "Parklane Hospital", "Hill Park Hospital"]
mortality_recovery["Hospital"] = np.random.choice(hospital_names, size=len(mortality_recovery))

# 🔹 Streamlit App Config
st.set_page_config(page_title="Pathogen Sim Dashboard", layout="wide")
st.title("🦠 Pathogen Sim - Staphylococcus aureus Infection Dashboard")

# 🎨 Custom Pastel Theme Colors
custom_colors = ["#FFB6C1", "#87CEEB", "#FFD700", "#98FB98"]

# 🔹 Sidebar for Disease Info
st.sidebar.title("📝 Disease Information")
st.sidebar.markdown("## 🦠 **Staphylococcus aureus**")

# 🔹 Symptoms Section
st.sidebar.subheader("🤒 Symptoms")
st.sidebar.write("""
- Fever
- Skin Infections (boils, abscesses)
- Pneumonia
- Food Poisoning
- Toxic Shock Syndrome (TSS)
""")

# 🔹 Tests Section
st.sidebar.subheader("🩺 Diagnostic Tests")
st.sidebar.write("""
- Blood Culture
- Nasal Swab Test
- PCR Test
- Antibiotic Sensitivity Test
""")

# 🔹 Treatments Section
st.sidebar.subheader("💊 Treatments")
st.sidebar.write("""
- Antibiotics (Methicillin, Vancomycin)
- Drainage of Abscesses
- Supportive Therapy (IV Fluids, Oxygen)
""")

# 🔹 Prevention Section
st.sidebar.subheader("🛡️ Prevention")
st.sidebar.write("""
- Proper Hand Hygiene 👐
- Sanitization of Medical Equipment 🏥
- Avoid Sharing Personal Items 🚫
- Vaccination Development 💉 (In Progress)
""")

# 🔹 Infection Trends Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Infection Trends", "🏥 Hospital Comparisons", "💊 Antibiotic Resistance", "🌡️ Mortality & Recovery"])

with tab1:
    st.subheader("📈 Infection Spread Over Time (Animated)")
    fig = px.line(infection_spread, x="Date", y="Number_of_Cases", color="Source", 
                  markers=True, title="Infection Cases Over Time",
                  color_discrete_sequence=custom_colors)
    fig.update_traces(mode="lines+markers", line_shape="spline")  # Smooth animation
    fig.update_layout(transition_duration=500)  # Smooth transition
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🏥 Infection Rates by Hospital")
    fig = px.bar(hospitals, x="Name", y="Infection_Rate", color="Name",
                 title="Hospital Infection Rates",
                 color_discrete_sequence=custom_colors)
    fig.update_layout(bargap=0.2, transition_duration=500)  # Adjust bar spacing & smooth effect
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("💊 Antibiotic Resistance Breakdown")
    fig = px.pie(antibiotic_resistance, names="Antibiotic", values="Resistance_Percentage",
                 title="Antibiotic Resistance Distribution",
                 color_discrete_sequence=custom_colors)
    fig.update_traces(textinfo="percent+label")  # Show percentage
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("🌡️ Mortality vs Recovery Heatmap")
    fig = px.imshow(mortality_recovery.pivot(index="Date", columns="Hospital", values="Mortality"),
                    color_continuous_scale=px.colors.sequential.Plasma, title="Mortality Rate Heatmap")
    st.plotly_chart(fig, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully with Fixed Hospital Names!")  
