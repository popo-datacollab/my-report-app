import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Database ---
agent_map = {
    "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
    "306432": "Ei Pwint Phyu-2", "306564": "Thin Thin Nwe-3", "307381": "Ye Myat Thu",
    "313820": "Thae Su", "304539": "Ko Phyo", "313674": "Lai Hnin Hlaing"
}

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes) or total_minutes == 0: return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar: File Upload ---
with st.sidebar:
    st.title("📂 File Uploader")
    f1 = st.file_uploader("Pre-Order Report (R1-R3)", type=["csv", "xlsx"])
    f2 = st.file_uploader("IVR Call Log (R4)", type=["csv"])
    
    st.divider()
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- Main Dashboard ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.info("ဘယ်ဘက် Sidebar မှာ File အရင်တင်ပေးပါ။")

elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    if f1 is not None:
        # File ကို ဖတ်ပြီး Data ပြခြင်း
        df1 = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
        st.success(f"File '{f1.name}' ကို ဖတ်လို့ရပါပြီ။")
        
        # Report 3 Search UI
        st.subheader("🔍 Report 3: Manual Case ID Search")
        case_input = st.text_area("Case ID များကို ထည့်ပါ (POI-26-03-XXXX...)")
        if st.button("Generate Report 3"):
            search_list = [x.strip() for x in case_input.replace('\n', ',').split(',') if x.strip()]
            # Case Column ရှာဖွေခြင်း
            case_col = [c for c in df1.columns if 'case' in c.lower() or 'id' in c.lower()]
            if case_col:
                res = df1[df1[case_col[0]].astype(str).isin(search_list)]
                st.write(f"ရှာဖွေတွေ့ရှိမှု - {len(res)} ခု")
                st.dataframe(res, use_container_width=True)
            else:
                st.error("Case ID Column ရှာမတွေ့ပါ။")
    else:
        st.warning("Sidebar တွင် Pre-Order File ကို အရင်တင်ပေးပါ။")

elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    if f2 is not None:
        df2 = pd.read_csv(f2, encoding='latin-1')
        df2.columns = df2.columns.str.strip()
        
        if 'Agent' in df2.columns and 'Pause Time' in df2.columns:
            df2['Agent_ID'] = df2['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            df2['Pause Time'] = pd.to_numeric(df2['Pause Time'], errors='coerce').fillna(0)
            
            summary = df2.groupby('Agent_ID')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent_ID'].map(agent_map).fillna("Unknown")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.dataframe(summary[['Agent_ID', 'Agent Name', 'Formatted Time']].sort_values(by='Agent_ID'), use_container_width=True)
        else:
            st.error("Column 'Agent' သို့မဟုတ် 'Pause Time' ရှာမတွေ့ပါ။")
    else:
        st.warning("Sidebar တွင် IVR Call Log File ကို အရင်တင်ပေးပါ။")
