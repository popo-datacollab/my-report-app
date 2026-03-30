import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Global File Upload (Sidebar မှာ ထားပေးထားပါတယ်) ---
with st.sidebar:
    st.title("📂 File Uploader")
    st.markdown("Report များကြည့်ရန် File အရင်တင်ပေးပါ")
    
    # Session State ထဲမှာ Data သိမ်းထားဖို့ (Menu ပြောင်းလည်း Data မပျောက်အောင်)
    if 'pre_data' not in st.session_state: st.session_state.pre_data = None
    if 'ivr_data' not in st.session_state: st.session_state.ivr_data = None
    if 'ticket_data' not in st.session_state: st.session_state.ticket_data = None

    # File Uploaders
    f1 = st.file_uploader("Pre-Order Report (R1-R3)", type=["csv", "xlsx"])
    f2 = st.file_uploader("IVR Call Log (R4)", type=["csv"])
    f3 = st.file_uploader("Ticket Report (R5-R6)", type=["csv", "xlsx"])

    # File တင်လိုက်ရင် Data ထဲထည့်မယ်
    if f1: st.session_state.pre_data = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
    if f2: 
        ivr_df = pd.read_csv(f2, encoding='latin-1')
        ivr_df.columns = ivr_df.columns.str.strip()
        st.session_state.ivr_data = ivr_df
    if f3: st.session_state.ticket_data = pd.read_csv(f3, encoding='latin-1') if f3.name.endswith('.csv') else pd.read_excel(f3)

    st.divider()
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", 
                      ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- Agent Database (Mapping) ---
agent_map = {
    "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
    "313820": "Agent Name 313820", "304539": "Agent Name 304539", "313674": "Lai Hnin Hlaing"
}

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Main Dashboard Logic ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.info("ဘယ်ဘက် Sidebar ကနေ File အရင်တင်ပေးပြီးမှ Report ကို ရွေးချယ်ကြည့်ရှုပေးပါခင်ဗျာ။")

elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    if st.session_state.pre_data is not None:
        st.success("Pre-Order Data အဆင်သင့်ရှိပါသည်။")
        # Report 3 Search Logic 
        st.subheader("🔍 Report 3: Manual Case ID Search")
        # (Case ID Search code များကို ဤနေရာတွင် ဆက်ရေးပါ)
    else:
        st.warning("ဘယ်ဘက် Sidebar မှာ 'Pre-Order Report' အရင်တင်ပေးပါ။")

elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    if st.session_state.ivr_data is not None:
        df = st.session_state.ivr_data
        if 'Agent' in df.columns:
            # ID သန့်စင်ခြင်း
            df['Agent_ID'] = df['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            df['Pause Time'] = pd.to_numeric(df['Pause Time'], errors='coerce').fillna(0)
            
            summary = df.groupby('Agent_ID')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent_ID'].map(agent_map).fillna("Unknown Agent")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.dataframe(summary[['Agent_ID', 'Agent Name', 'Formatted Time']], use_container_width=True)
            st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
        else:
            st.error("Column 'Agent' ရှာမတွေ့ပါ။ CSV column name ကို စစ်ဆေးပေးပါ။")
    else:
        st.warning("ဘယ်ဘက် Sidebar မှာ 'IVR Call Log' အရင်တင်ပေးပါ။")
