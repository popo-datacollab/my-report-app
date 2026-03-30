import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Pre-Order Analysis", layout="wide")

# --- Agent Map (Data Consistency အတွက်) ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        # ... (လူကြီးမင်း၏ Agent List အပြည့်အစုံကို ဤနေရာတွင် ဆက်လက်ထားရှိပါ)
    }

# --- Formatting Helper ---
def clean_id(val):
    return str(val).replace('.0', '').strip()

# --- Main Menu Sidebar ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("Reports", ["Pre-Order (R1-R3)", "Pause Time Analysis"])

# --- Pre-Order Analysis Section ---
if choice == "Pre-Order (R1-R3)":
    st.title("Pre-Order Report Analysis")
    
    f1 = st.file_uploader("Upload File 1: Pre-Order Report", type=["csv", "xlsx"])

    if f1:
        # Load Data
        df = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
        df.columns = df.columns.str.strip()
        
        # 1. Report 1 & 2 Tables (image_7ad681 အတိုင်း)
        st.markdown("### Report 1: Service City & Billing Group")
        # ဤနေရာတွင် လူကြီးမင်း၏ တွက်ချက်မှု Logic များကို ထည့်သွင်းပါ
        
        # ဥပမာ Table ပုံစံပြသခြင်း
        st.image("https://raw.githubusercontent.com/dataprofessor/streamlit-share/master/streamlit-logo.png", width=100) # Placeholder
        
        # 2. Data Summary (image_795f41 အတိုင်း)
        st.markdown("### Data Summary:")
        
        # ID များကို ရှင်းလင်းခြင်း
        id_col = next((c for c in df.columns if 'Agent' in c or 'ID' in c), None)
        if id_col:
            df[id_col] = df[id_col].apply(clean_id)
            # နာမည်များ ချိတ်ဆက်ခြင်း
            if 'Customer Name' not in df.columns:
                df['Customer Name'] = df[id_col].map(st.session_state.agent_map).fillna("Unknown")

        st.dataframe(df.head(10), use_container_width=True)

# --- Pause Time Analysis Section ---
elif choice == "Pause Time Analysis":
    st.title("Agent Pause Time Report")
    # ယခင်ပေးထားသော Pause Time Code ကို ဤနေရာတွင် ထည့်သွင်းနိုင်သည်
