import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Agent Report", layout="wide")

# Sidebar Menu
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("Go to:", ["Home", "Agent Analysis (R4)"])

# Home Page
if choice == "Home":
    st.title("🏠 Welcome")
    st.write("App is running successfully!")

# Agent Analysis Page
elif choice == "Agent Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    agent_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if agent_file is not None:
        df = pd.read_csv(agent_file, encoding='latin-1')
        
        if 'Agent' in df.columns and 'Pause Time' in df.columns:
            # Time conversion
            if df['Pause Time'].dtype == 'object':
                df['Pause Time'] = pd.to_timedelta(df['Pause Time']).dt.total_seconds() / 60
            
            summary = df.groupby('Agent')['Pause Time'].sum().reset_index()
            
            # Chart ဆွဲရန် Built-in Bar Chart ကိုသုံးခြင်း (matplotlib မလိုပါ)
            st.subheader("Pause Time Summary")
            st.bar_chart(data=summary, x='Agent', y='Pause Time')
            st.dataframe(summary)
        else:
            st.error("Column names 'Agent' or 'Pause Time' not found!")
