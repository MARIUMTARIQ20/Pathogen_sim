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

# 🔹 Fix Hospital Names in Data (Permanent Update)
hospital_names = ["AKUH", "LNH", "South City Hospital", "Parklane Hospital", "Hill Park Hospital"]
hospitals["Name"] = np.random.choice(hospital_names, size=len(hospitals), replace=True)
mortality_recovery["Hospital"] = np.random.choice(hospital_names, size=len(mortality_recovery), replace=True)

# 🔹 Streamlit App Config
st.set_page_config(page_title="Pathogen Sim Dashboard", layout="wide")

# 🎨 CSS for Styling Fonts & Headings
st.markdown("""
    <style>
    h1 {
        text-align: center; 
        font-size: 45px; 
        font-weight: bold; 
        color: #ff4b4b;
    }
    h2 {
        font-size: 30px; 
        font-weight: bold; 
        color: #4b72ff;
    }
    h3 {
        font-size: 24px; 
        font-weight: bold;
    }
    .sidebar-text {
        font-size: 18px; 
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🔹 Title
st.markdown("<h1>🦠 Pathogen Sim - Staphylococcus aureus Infection Dashboard</h1>", unsafe_allow_html=True)

# 🎨 Custom Theme Colors
custom_colors = ["#FFB6C1", "#87CEEB", "#FFD700", "#98FB98"]

# 🔹 Sidebar for Disease Info
st.sidebar.markdown("<h2>📝 Disease Information</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h3>🦠 Staphylococcus aureus</h3>", unsafe_allow_html=True)

# 🔹 Symptoms
st.sidebar.markdown("<h3>🤒 Symptoms</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<ul class='sidebar-text'>
<li>Fever</li>
<li>Skin Infections (boils, abscesses)</li>
<li>Pneumonia</li>
<li>Food Poisoning</li>
<li>Toxic Shock Syndrome (TSS)</li>
</ul>
""", unsafe_allow_html=True)

# 🔹 Tests
st.sidebar.markdown("<h3>🩺 Diagnostic Tests</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<ul class='sidebar-text'>
<li>Blood Culture</li>
<li>Nasal Swab Test</li>
<li>PCR Test</li>
<li>Antibiotic Sensitivity Test</li>
</ul>
""", unsafe_allow_html=True)

# 🔹 Treatments
st.sidebar.markdown("<h3>💊 Treatments</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<ul class='sidebar-text'>
<li>Antibiotics (Methicillin, Vancomycin)</li>
<li>Drainage of Abscesses</li>
<li>Supportive Therapy (IV Fluids, Oxygen)</li>
</ul>
""", unsafe_allow_html=True)

# 🔹 Prevention
st.sidebar.markdown("<h3>🛡️ Prevention</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<ul class='sidebar-text'>
<li>Proper Hand Hygiene 👐</li>
<li>Sanitization of Medical Equipment 🏥</li>
<li>Avoid Sharing Personal Items 🚫</li>
<li>Vaccination Development 💉 (In Progress)</li>
</ul>
""", unsafe_allow_html=True)

# 🔹 Infection Trends Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Infection Trends", "🏥 Hospital Comparisons", "💊 Antibiotic Resistance", "🌡️ Mortality & Recovery"])

with tab1:
    st.markdown("<h2>📈 Infection Spread Over Time (Animated)</h2>", unsafe_allow_html=True)
    fig = px.line(infection_spread, x="Date", y="Number_of_Cases", color="Source", 
                  markers=True, title="Infection Cases Over Time",
                  color_discrete_sequence=custom_colors)
    fig.update_traces(mode="lines+markers", line_shape="spline")  # Smooth animation
    fig.update_layout(transition_duration=500)  # Smooth transition
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("<h2>🏥 Infection Rates by Hospital</h2>", unsafe_allow_html=True)
    
    fig = px.bar(hospitals, x="Name", y="Infection_Rate", color="Name",
                 title="Hospital Infection Rates",
                 color_discrete_sequence=custom_colors)
    fig.update_layout(bargap=0.2, transition_duration=500)  # Adjust bar spacing & smooth effect
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("<h2>💊 Antibiotic Resistance Breakdown</h2>", unsafe_allow_html=True)
    fig = px.pie(antibiotic_resistance, names="Antibiotic", values="Resistance_Percentage",
                 title="Antibiotic Resistance Distribution",
                 color_discrete_sequence=custom_colors)
    fig.update_traces(textinfo="percent+label")  # Show percentage
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("<h2>🌡️ Mortality vs Recovery Heatmap</h2>", unsafe_allow_html=True)
    
    # Fix Heatmap Data Formatting
    heatmap_data = mortality_recovery.pivot_table(index="Date", columns="Hospital", values="Mortality", aggfunc='sum')

    fig = px.imshow(heatmap_data,
                    color_continuous_scale=px.colors.sequential.Plasma, title="Mortality Rate Heatmap")
    st.plotly_chart(fig, use_container_width=True)
