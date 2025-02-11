import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pathogen Sim Dashboard",
    page_icon="🦠",
    layout="wide"
)

# --- LOADING DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("pathogen_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("🔍 Filters")
selected_hospital = st.sidebar.multiselect("Select Hospital", df["Hospital"].unique(), default=df["Hospital"].unique())

# --- MAIN TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Infection Trends", "🏥 Hospital Comparisons", "💊 Antibiotic Resistance", "☠️ Mortality & Recovery"])

# --- INFECTION TRENDS ---
with tab1:
    st.markdown("## 🦠 Infection Spread Over Time")
    filtered_df = df[df["Hospital"].isin(selected_hospital)]
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for selected hospital(s).")
    else:
        fig = px.line(filtered_df, x="Date", y="Number_of_Cases", color="Hospital", title="Infection Cases Over Time")
        fig.update_layout(legend_title_text="Source")
        st.plotly_chart(fig, use_container_width=True)

# --- HOSPITAL COMPARISON ---
with tab2:
    st.markdown("## 🏥 Hospital Comparisons")
    comparison_fig = px.bar(df, x="Hospital", y="Number_of_Cases", color="Hospital", title="Hospital-wise Infection Cases")
    st.plotly_chart(comparison_fig, use_container_width=True)

# --- ANTIBIOTIC RESISTANCE ---
with tab3:
    st.markdown("## 💊 Antibiotic Resistance Overview")
    resistance_fig = px.scatter(df, x="Antibiotic", y="Resistance_Level", color="Hospital", size="Number_of_Cases")
    st.plotly_chart(resistance_fig, use_container_width=True)

# --- MORTALITY & RECOVERY ---
with tab4:
    st.markdown("
