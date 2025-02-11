import streamlit as st
import pandas as pd
import plotly.express as px

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("pathogen_data.csv")
    return df

df = load_data()

# Ensure Data is Clean
df = df.dropna(subset=["Hospital", "Number_of_Cases", "Date"])
df["Number_of_Cases"] = pd.to_numeric(df["Number_of_Cases"], errors='coerce')
df["Date"] = pd.to_datetime(df["Date"])

# Streamlit Page Config
st.set_page_config(page_title="Pathogen Sim", layout="wide")

# Sidebar Navigation
st.sidebar.title("🔬 Pathogen Sim Dashboard")
page = st.sidebar.radio("Go to", ["📈 Infection Trends", "🏥 Hospital Comparisons", "💊 Antibiotic Resistance", "☠️ Mortality & Recovery"])

# Header
st.title("🦠 Pathogen Sim - Infection Analysis Dashboard")

# Infection Trends Page
if page == "📈 Infection Trends":
    st.subheader("📊 Infection Spread Over Time (Animated)")

    fig = px.line(
        df, 
        x="Date", 
        y="Number_of_Cases", 
        color="Hospital",
        markers=True,
        title="Infection Cases Over Time",
    )
    fig.update_traces(line=dict(width=2))  # Adjust line width
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Cases",
        font=dict(size=14),  # Fix small fonts
        template="plotly_white",
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Hospital Comparisons Page
elif page == "🏥 Hospital Comparisons":
    st.subheader("🏥 Infection Rate by Hospital")
    
    hospital_cases = df.groupby("Hospital")["Number_of_Cases"].sum().reset_index()
    
    fig = px.bar(
        hospital_cases, 
        x="Hospital", 
        y="Number_of_Cases",
        color="Hospital",
        title="Total Infection Cases Per Hospital",
    )
    fig.update_layout(
        xaxis_title="Hospital",
        yaxis_title="Total Cases",
        font=dict(size=14),
        template="plotly_white",
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Antibiotic Resistance Page
elif page == "💊 Antibiotic Resistance":
    st.subheader("💊 Antibiotic Resistance Trends")

    # Assuming "Antibiotic" column exists
    if "Antibiotic" in df.columns:
        antibiotic_resistance = df.groupby("Antibiotic")["Number_of_Cases"].sum().reset_index()
        
        fig = px.bar(
            antibiotic_resistance, 
            x="Antibiotic", 
            y="Number_of_Cases",
            color="Antibiotic",
            title="Antibiotic Resistance Overview",
        )
        fig.update_layout(
            xaxis_title="Antibiotic",
            yaxis_title="Resistant Cases",
            font=dict(size=14),
            template="plotly_white",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No Antibiotic Resistance Data Available.")

# Mortality & Recovery Page
elif page == "☠️ Mortality & Recovery":
    st.subheader("☠️ Mortality vs. Recovery Rates")

    # Assuming "Outcome" column exists
    if "Outcome" in df.columns:
        outcome_counts = df["Outcome"].value_counts().reset_index()
        outcome_counts.columns = ["Outcome", "Count"]
        
        fig = px.pie(
            outcome_counts, 
            names="Outcome", 
            values="Count",
            title="Mortality & Recovery Distribution",
            color="Outcome",
        )
        fig.update_layout(
            font=dict(size=14),
            template="plotly_white",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No Mortality/Recovery Data Available.")
