import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Database (Mapping) ---
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
                      ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)", "Ticket Report (R5-R6)"])

# --- 1. Home Page ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.write("App is running successfully!")
    st.info("ဘယ်ဘက် Menu ကနေ စစ်ဆေးလိုတဲ့ Report ကို ရွေးချယ်ပါ။")

# --- 2. Pre-Order (R1-R3) Menu (ဒီနေရာမှာ လူကြီးမင်းလိုချင်တဲ့ Box ၃ ခု ပုံစံထည့်ထားပါတယ်) ---
elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    
    # ပုံထဲကအတိုင်း File တင်ရမယ့် Box ၃ ခု
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.help("📂 File 1: Pre-Order Report (R1-R3)")
        f1 = st.file_uploader("Upload R1-R3", type=["csv", "xlsx"], key="pre_f1", label_visibility="collapsed")
        
    with col2:
        st.help("⏱️ File 2: IVR Call Log (R4)")
        f2 = st.file_uploader("Upload IVR", type=["csv"], key="pre_f2", label_visibility="collapsed")
        
    with col3:
        st.help("🎫 File 3: Ticket Report (R5-R6)")
        f3 = st.file_uploader("Upload Tickets", type=["csv", "xlsx"], key="pre_f3", label_visibility="collapsed")

    st.divider()
    
    # Report 4: Green Light Issue UI
    st.subheader("🔵 Report 4: Green Light Issue (Plan Upgrade FRSLA)")
    st.info("ဤ Report အတွက် Data ကို File 1 သို့မဟုတ် File 3 မှ အလိုအလျောက် တွက်ချက်ပေးမည်ဖြစ်သည်။")
    
    # Report 3: Manual Search (အောက်နားမှာ ဆက်ထားပေးပါတယ်)
    if f1:
        st.subheader("🔍 Report 3: Manual Case ID Search")
        df1 = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
        case_ids = st.text_area("Case ID များကို ထည့်ပါ -", placeholder="POI-26-03-XXXX...")
        if st.button("Generate Report 3"):
            st.write("ရလဒ်များကို ပြသနေသည်...")

# --- 3. Agent Pause Analysis (R4) Menu (သီးသန့်ခွဲထုတ်ပေးထားပါတယ်) ---
elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    agent_file = st.file_uploader("Agent CSV File ကို တင်ပါ", type=["csv"], key="pause_main")
    
    if agent_file:
        df = pd.read_csv(agent_file, encoding='latin-1')
        df.columns = df.columns.str.strip()
        
        if 'Agent' in df.columns and 'Pause Time' in df.columns:
            # Unknown ပျောက်အောင် ID သန့်စင်ခြင်း
            df['Agent'] = df['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            df['Pause Time'] = pd.to_numeric(df['Pause Time'], errors='coerce').fillna(0)
            
            summary = df.groupby('Agent')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent'].map(st.session_state.agent_map).fillna("Unknown Agent")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.subheader("Summary Table")
            st.dataframe(summary[['Agent', 'Agent Name', 'Formatted Time']].sort_values(by='Agent'), use_container_width=True, hide_index=True)
            st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
        else:
            st.error("Column နာမည်များ မှားယွင်းနေပါသည်။")

# --- 4. Ticket Report (R5-R6
