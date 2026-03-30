import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Database (Mapping) ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        "306432": "Ei Pwint Phyu-2", "306564": "Thin Thin Nwe-3", "307381": "Ye Myat Thu",
        "307832": "Hnin Aye Soe", "308059": "Nyo Nyo Tun Lwin", "313820": "Agent Name 313820",
        "304539": "Agent Name 304539", "313674": "Lai Hnin Hlaing"
    }

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar Menu (Menu များ ပြန်ခွဲထားသည်) ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", 
                      ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)", "Ticket Report (R5-R6)"])

# --- Home Page ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.write("App is running successfully!")

# --- Pre-Order (R1-R3) ---
elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    file1 = st.file_uploader("Upload Pre-Order File", type=["csv", "xlsx"])
    if file1:
        st.success("File တင်ပြီးပါပြီ။")
        # R1-R3 Logic များ ဤနေရာတွင် ရှိသည်

# --- Agent Pause Analysis (R4) --- (ဒီ Menu ပြန်ပေါ်လာပါပြီ)
elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    agent_file = st.file_uploader("Agent CSV File ကို တင်ပါ", type=["csv"])
    
    if agent_file:
        df = pd.read_csv(agent_file, encoding='latin-1')
        df.columns = df.columns.str.strip() # Column space သန့်စင်ခြင်း
        
        if 'Agent' in df.columns and 'Pause Time' in df.columns:
            # Agent ID သန့်စင်ခြင်း (Unknown မဖြစ်အောင်)
            df['Agent'] = df['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            
            # Pause Time ကို Number ပြောင်းခြင်း
            df['Pause Time'] = pd.to_numeric(df['Pause Time'], errors='coerce').fillna(0)
            
            summary = df.groupby('Agent')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent'].map(st.session_state.agent_map).fillna("Unknown Agent")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.subheader("Summary Table")
            st.dataframe(summary[['Agent', 'Agent Name', 'Formatted Time']].sort_values(by='Agent'), use_container_width=True)
            st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
        else:
            st.error("Column 'Agent' သို့မဟုတ် 'Pause Time' ကို ရှာမတွေ့ပါ။")

# --- Ticket Report (R5-R6) ---
elif choice == "Ticket Report (R5-R6)":
    st.title("🎫 Ticket Report Analysis")
    file3 = st.file_uploader("Upload Ticket File", type=["csv", "xlsx"])
