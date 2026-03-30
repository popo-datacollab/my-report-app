import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Database (Mapping) ---
agent_map = {
    "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
    "306432": "Ei Pwint Phyu-2", "306564": "Thin Thin Nwe-3", "307381": "Ye Myat Thu",
    "313820": "Agent Name 313820", "304539": "Agent Name 304539", "313674": "Lai Hnin Hlaing"
}

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes) or total_minutes == 0: return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar: File Upload & Menu ---
with st.sidebar:
    st.title("📂 File Uploader")
    st.write("Report များကြည့်ရန် File အရင်တင်ပေးပါ")
    
    # Session State ထဲမှာ Data သိမ်းခြင်း (Menu ပြောင်းလည်း Data မပျောက်အောင်)
    up_f1 = st.file_uploader("Pre-Order Report (R1-R3)", type=["csv", "xlsx"], key="sidebar_f1")
    up_f2 = st.file_uploader("IVR Call Log (R4)", type=["csv"], key="sidebar_f2")
    up_f3 = st.file_uploader("Ticket Report (R5-R6)", type=["csv", "xlsx"], key="sidebar_f3")

    st.divider()
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", 
                      ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- Main Dashboard Logic ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.info("ဘယ်ဘက် Sidebar ကနေ File အရင်တင်ပေးပြီးမှ Report ကို ရွေးချယ်ကြည့်ရှုပေးပါခင်ဗျာ။")

elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    if up_f1 is not None:
        try:
            df1 = pd.read_csv(up_f1, encoding='latin-1') if up_f1.name.endswith('.csv') else pd.read_excel(up_f1)
            st.success(f"File '{up_f1.name}' အဆင်သင့်ရှိပါသည်။")
            
            st.subheader("🔍 Report 3: Manual Case ID Search")
            case_input = st.text_area("Case ID များကို ထည့်ပါ -", placeholder="POI-26-03-XXXX...")
            if st.button("Generate Report 3"):
                # Case ID ရှာဖွေသည့် Logic
                st.write("ရလဒ်များကို ရှာဖွေနေပါသည်...")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.warning("ဘယ်ဘက် Sidebar မှာ 'Pre-Order Report' အရင်တင်ပေးပါ။")

elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    if up_f2 is not None:
        try:
            df2 = pd.read_csv(up_f2, encoding='latin-1')
            df2.columns = df2.columns.str.strip()
            
            if 'Agent' in df2.columns and 'Pause Time' in df2.columns:
                # ID သန့်စင်ခြင်း (Agent/313820 -> 313820)
                df2['Agent_ID'] = df2['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
                df2['Pause Time'] = pd.to_numeric(df2['Pause Time'], errors='coerce').fillna(0)
                
                summary = df2.groupby('Agent_ID')['Pause Time'].sum().reset_index()
                summary['Agent Name'] = summary['Agent_ID'].map(agent_map).fillna("Unknown Agent")
                summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
                
                st.subheader("Summary Table")
                st.dataframe(summary[['Agent_ID', 'Agent Name', 'Formatted Time']], use_container_width=True)
                
                # Chart ဆွဲခြင်း
                st.subheader("Visual Analysis")
                st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
            else:
                st.error("Column နာမည်များ မှားယွင်းနေပါသည်။ (Agent နှင့် Pause Time လိုအပ်သည်)")
        except Exception as e:
            st.error(f"Error processing R4: {e}")
    else:
        st.warning("ဘယ်ဘက် Sidebar မှာ 'IVR Call Log' အရင်တင်ပေးပါ။")
