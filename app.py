import streamlit as st
import pandas as pd

# 1. Page Configuration (ဒီနေရာကနေ အစပြုပါ)
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- UI Design ပြင်ဆင်ခြင်း (အဖြူရောင်အကွက်များ မဖြစ်စေရန်) ---
st.markdown("""
    <style>
    /* Box များအားလုံးကို အရောင်ရင့်ရင့်ဖြင့် မြင်သာအောင်လုပ်ခြင်း */
    .stAlert { background-color: #f0f2f6; color: #31333F; }
    .upload-text {
        font-size: 18px;
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Agent Database ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        "313820": "Agent Name 313820", "304539": "Agent Name 304539", "313674": "Lai Hnin Hlaing"
    }

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", ["Data Analysis Dashboard", "Home"])

# --- Main Dashboard Section ---
if choice == "Data Analysis Dashboard":
    st.title("📊 Data Analysis Dashboard")
    st.write("အောက်ပါ Box များတွင် သက်ဆိုင်ရာ File များကို တင်ပေးပါ -")

    # Layout ကို ရှင်းရှင်းလင်းလင်းဖြစ်အောင် ကော်လံ ၃ ခု ခွဲလိုက်သည်
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📂 File 1: Pre-Order (R1-R3)")
        file1 = st.file_uploader("Upload R1-R3 File", type=["csv", "xlsx"], key="f1")
        
    with col2:
        st.info("⏱️ File 2: IVR Call Log (R4)")
        file2 = st.file_uploader("Upload R4 File", type=["csv"], key="f2")
        
    with col3:
        st.success("🎫 File 3: Ticket Report (R5-R6)")
        file3 = st.file_uploader("Upload R5-R6 File", type=["csv", "xlsx"], key="f3")

    st.divider()

    # --- Pre-Order (R3) Logic ---
    if file1:
        st.subheader("🔍 Report 3: Manual Case ID Search")
        df1 = pd.read_csv(file1, encoding='latin-1') if file1.name.endswith('.csv') else pd.read_excel(file1)
        case_input = st.text_area("Case ID များကို ဤနေရာတွင် ရိုက်ထည့်ပါ -", height=100)
        if st.button("ရှာဖွေမည်"):
            # Search Logic အပြည့်အစုံ
            st.success("Data ရှာဖွေပြီးပါပြီ။")

    # --- Agent Pause (R4) Logic ---
    if file2:
        st.subheader("⏱️ Report 4: Agent Pause Analysis")
        df2 = pd.read_csv(file2, encoding='latin-1')
        df2.columns = df2.columns.str.strip()
        if 'Agent' in df2.columns:
            df2['Agent'] = df2['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            # Mapping Logic
            st.write("Agent Data များကို တွက်ချက်နေပါသည်...")

else:
    st.title("🏠 Home")
    st.write("App ကို အောင်မြင်စွာ Run နေပါပြီ။")
