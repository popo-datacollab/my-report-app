import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Database ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        "306432": "Ei Pwint Phyu-2", "306564": "Thin Thin Nwe-3", "307381": "Ye Myat Thu",
        "313820": "Thae Su", "304539": "Ko Phyo", "313674": "Lai Hnin Hlaing"
    }

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", 
                      ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- 1. Home Page ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.info("ဘယ်ဘက် Menu မှ Report အမျိုးအစားကို ရွေးချယ်ပါ။")

# --- 2. Pre-Order (R1-R3) ---
elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    
    # ရှင်းလင်းသော Box ၃ ခု ပုံစံ
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("📂 File 1")
        st.caption("Pre-Order Report (R1-R3)")
        f1 = st.file_uploader("Upload R1-R3", type=["csv", "xlsx"], key="u1")
    with c2:
        st.subheader("⏱️ File 2")
        st.caption("IVR Call Log (R4)")
        f2 = st.file_uploader("Upload IVR", type=["csv"], key="u2")
    with c3:
        st.subheader("🎫 File 3")
        st.caption("Ticket Report (R5-R6)")
        f3 = st.file_uploader("Upload Tickets", type=["csv", "xlsx"], key="u3")

    st.divider()
    st.markdown("### 🔵 Report 4: Green Light Issue (Plan Upgrade FRSLA)")
    st.info("ဤ Report အတွက် Data ကို File 1 သို့မဟုတ် File 3 မှ အလိုအလျောက် တွက်ချက်ပေးမည်ဖြစ်သည်။")

# --- 3. Agent Pause Analysis (R4) ---
elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    agent_file = st.file_uploader("Agent CSV File ကို တင်ပါ", type=["csv"])
    
    if agent_file:
        df = pd.read_csv(agent_file, encoding='latin-1')
        df.columns = df.columns.str.strip()
        
        if 'Agent' in df.columns and 'Pause Time' in df.columns:
            df['Agent'] = df['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            df['Pause Time'] = pd.to_numeric(df['Pause Time'], errors='coerce').fillna(0)
            
            summary = df.groupby('Agent')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent'].map(st.session_state.agent_map).fillna("Unknown Agent")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.dataframe(summary[['Agent', 'Agent Name', 'Formatted Time']], use_container_width=True, hide_index=True)
            st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
