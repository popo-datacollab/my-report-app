import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Custom CSS for Styling (ပုံထဲကအတိုင်း Box လှလှလေးများဖြစ်အောင်) ---
st.markdown("""
    <style>
    .upload-box {
        border: 2px dashed #1a73e8;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        background-color: #f8f9fa;
        margin-bottom: 10px;
    }
    .ticket-box {
        border: 2px dashed #28a745;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        background-color: #f8f9fa;
        margin-bottom: 10px;
    }
    .report-title {
        color: #1a73e8;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        margin-top: 20px;
        border-bottom: 2px solid #1a73e8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Agent Database (Mapping) ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        "306432": "Ei Pwint Phyu-2", "306564": "Thin Thin Nwe-3", "313820": "Agent Name 313820", # ပုံထဲပါသော ID အသစ်များ
        "304539": "Agent Name 304539", "313674": "Lai Hnin Hlaing"
    }

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", ["Home", "Data Analysis Dashboard"])

if choice == "Home":
    st.title("🏠 Welcome to Po Po Dashboard")
    st.info("ညာဘက် Menu မှ 'Data Analysis Dashboard' ကို နှိပ်၍ အလုပ်စတင်နိုင်ပါသည်။")

else:
    # --- UI Layout: Upload Boxes (၃ ခု) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="upload-box"><b>File 1: Pre-Order Report (R1, R2, R3)</b></div>', unsafe_allow_html=True)
        file1 = st.file_uploader("Upload R1-R3", type=["csv", "xlsx"], label_visibility="collapsed")
        
    with col2:
        st.markdown('<div class="upload-box"><b>File 2: IVR Call Log (Report 4)</b></div>', unsafe_allow_html=True)
        file2 = st.file_uploader("Upload R4", type=["csv"], label_visibility="collapsed")
        
    with col3:
        st.markdown('<div class="ticket-box"><b style="color:#28a745;">File 3: Ticket Report (R5, R6)</b></div>', unsafe_allow_html=True)
        file3 = st.file_uploader("Upload R5-R6", type=["csv", "xlsx"], label_visibility="collapsed")

    st.divider()

    # --- Logic for Pre-Order (R1, R2, R3) ---
    if file1:
        st.markdown('<p class="report-title">Report 3: Manual Case ID Search</p>', unsafe_allow_html=True)
        df1 = pd.read_csv(file1, encoding='latin-1') if file1.name.endswith('.csv') else pd.read_excel(file1)
        
        case_input = st.text_area("Case ID များကို ထည့်ပါ (POI-26-03-XXXX...)", height=100)
        if st.button("Generate Report 3"):
            search_list = [x.strip() for x in case_input.replace('\n', ',').split(',') if x.strip()]
            case_col = [c for c in df1.columns if 'case' in c.lower() or 'id' in c.lower()]
            if case_col:
                res = df1[df1[case_col[0]].astype(str).isin(search_list)]
                st.dataframe(res, use_container_width=True)
            else: st.error("Case ID Column ရှာမတွေ့ပါ။")

    # --- Logic for Agent Pause (Report 4) ---
    if file2:
        st.markdown('<p class="report-title">Report 4: Agent Pause Analysis</p>', unsafe_allow_html=True)
        df2 = pd.read_csv(file2, encoding='latin-1')
        df2.columns = df2.columns.str.strip()
        
        if 'Agent' in df2.columns:
            # ID သန့်စင်ခြင်း
            df2['Agent'] = df2['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            df2['Pause Time'] = pd.to_numeric(df2['Pause Time'], errors='coerce').fillna(0)
            
            summary = df2.groupby('Agent')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent'].map(st.session_state.agent_map).fillna("Unknown Agent")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.dataframe(summary[['Agent', 'Agent Name', 'Formatted Time']].sort_values(by='Agent'), use_container_width=True)

    # --- Report 4: Green Light Issue (Placeholder) ---
    st.markdown('<p class="report-title">Report 4: Green Light Issue (Plan Upgrade FRSLA)</p>', unsafe_allow_html=True)
    st.info("ဤ Report အတွက် Data ကို File 1 သို့မဟုတ် File 3 မှ အလိုအလျောက် တွက်ချက်ပေးမည်ဖြစ်သည်။")
