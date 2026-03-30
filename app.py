import streamlit as st
import pandas as pd
from io import BytesIO

# --- Page Setup ---
st.set_page_config(page_title="Pause Time Dashboard", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
    .report-header { color: #1a73e8; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- Agent Map Data ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        # ... (လူကြီးမင်း၏ Agent List များအားလုံး ဤနေရာတွင် ဆက်လက်ရှိပါမည်)
    }

# --- Sidebar ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("Reports", ["Pre-Order (R1-R3)", "Pause Time Analysis"])

# --- Pause Time Analysis ---
if choice == "Pause Time Analysis":
    st.markdown('<div class="report-header">Agent Pause Time Report</div>', unsafe_allow_html=True)
    
    # Excel Error ကို ကာကွယ်ရန် csv ကို ဦးစားပေးခိုင်းခြင်း
    f_pause = st.file_uploader("Upload Agent CSV (Excel ဖတ်မရပါက CSV ပြောင်းတင်ပေးပါ)", type=["csv", "xlsx"])

    if f_pause:
        try:
            # File Loading Logic
            if f_pause.name.endswith('.csv'):
                df = pd.read_csv(f_pause, encoding='latin-1')
            else:
                # openpyxl library မရှိပါက error တက်နိုင်သောကြောင့် try-except သုံးခြင်း
                try:
                    df = pd.read_excel(f_pause, engine='openpyxl')
                except ImportError:
                    st.error("Excel ဖတ်ရန် 'openpyxl' library လိုအပ်နေပါသည်။ ကျေးဇူးပြု၍ ဖိုင်ကို CSV ပြောင်းပြီး ပြန်တင်ပေးပါ။")
                    st.stop()

            # Clean column names
            df.columns = df.columns.str.strip()
            
            # image_7890ab မှာဖြစ်ခဲ့တဲ့ KeyError ကို ကာကွယ်ရန် column စစ်ဆေးခြင်း
            id_col = next((c for c in df.columns if 'Agent' in c), None)
            pause_col = 'Pause Time'

            if id_col and pause_col in df.columns:
                # Mapping Names
                df['Agent Name'] = df[id_col].astype(str).str.strip().map(st.session_state.agent_map).fillna("Unknown Agent")
                df[pause_col] = df[pause_col].fillna("00:00:00")
                
                has_pause = df[df[pause_col] != "00:00:00"].sort_values(by=pause_col, ascending=False)
                no_pause = df[df[pause_col] == "00:00:00"]

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Pause Time ရှိသူများ")
                    st.dataframe(has_pause[['Agent Name', pause_col]].style.applymap(lambda x: "color: #d93025; font-weight: bold;", subset=[pause_col]), use_container_width=True, hide_index=True)

                with col2:
                    st.markdown("### Pause Time မရှိသူများ")
                    st.dataframe(no_pause[['Agent Name', pause_col]].style.applymap(lambda x: "color: #d93025;", subset=[pause_col]), use_container_width=True, hide_index=True)
            else:
                st.warning(f"ဖိုင်ထဲတွင် '{pause_col}' column မတွေ့ပါ။ Column နာမည် မှန်မမှန် စစ်ဆေးပေးပါ။")

        except Exception as e:
            st.error(f"Error ဖြစ်ပွားပါသည်: {e}")
