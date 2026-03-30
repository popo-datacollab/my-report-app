import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Mapping ---
agent_map = {
    "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
    "313820": "Thae Su", "304539": "Ko Phyo", "313674": "Lai Hnin Hlaing"
}

# --- Sidebar ---
with st.sidebar:
    st.title("📂 Data Control Center")
    f1 = st.file_uploader("Pre-Order Report (R1-R3) ကို တင်ပါ", type=["csv", "xlsx"])
    f2 = st.file_uploader("IVR Call Log (R4) ကို တင်ပါ", type=["csv"])
    st.divider()
    choice = st.radio("Menu ရွေးချယ်ပါ -", ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- Main Logic ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.info("Sidebar ကနေ File အရင်တင်ပေးပါ။")

elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    if f1 is not None:
        # Data ဖတ်ခြင်း
        df1 = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
        
        # Data ကျလာကြောင်း သေချာအောင် Raw Data အရင်ပြပါမယ်
        st.success(f"File '{f1.name}' ကို ဖတ်ပြီးပါပြီ။ (Total Rows: {len(df1)})")
        with st.expander("တင်ထားသော Data အားလုံးကို ကြည့်ရန်"):
            st.dataframe(df1.head(20)) # ပထမဆုံး အကြောင်း ၂၀ ကို အစမ်းပြမည်

        st.divider()
        st.subheader("🔍 Report 3: Manual Case ID Search")
        case_input = st.text_area("Case ID များကို ထည့်ပါ (တစ်ကြောင်းချင်းစီ)")
        
        if st.button("Generate Report 3"):
            if case_input:
                search_list = [x.strip() for x in case_input.replace('\n', ',').split(',') if x.strip()]
                
                # Column နာမည် တိတိကျကျမသိရင်တောင် 'id' သို့မဟုတ် 'case' ပါတာကို လိုက်ရှာခိုင်းခြင်း
                target_col = None
                for col in df1.columns:
                    if 'case' in col.lower() or 'id' in col.lower() or 'no' in col.lower():
                        target_col = col
                        break
                
                if target_col:
                    res = df1[df1[target_col].astype(str).str.contains('|'.join(search_list), na=False)]
                    st.write(f"ရှာဖွေတွေ့ရှိမှု - {len(res)} ခု (Column: {target_col})")
                    st.dataframe(res, use_container_width=True)
                else:
                    st.error("Excel ထဲမှာ 'ID' ဒါမှမဟုတ် 'Case' ပါတဲ့ Column ရှာမတွေ့ပါ။")
            else:
                st.warning("Case ID အရင်ထည့်ပေးပါ။")
    else:
        st.warning("ဘယ်ဘက် Sidebar တွင် Pre-Order File ကို အရင်တင်ပေးပါ။")

elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    if f2 is not None:
        df2 = pd.read_csv(f2, encoding='latin-1')
        df2.columns = df2.columns.str.strip()
        
        # Pause Time တွက်ချက်ခြင်း
        if 'Agent' in df2.columns and 'Pause Time' in df2.columns:
            df2['Agent_ID'] = df2['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            df2['Pause Time'] = pd.to_numeric(df2['Pause Time'], errors='coerce').fillna(0)
            
            summary = df2.groupby('Agent_ID')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent_ID'].map(agent_map).fillna("Unknown")
            st.dataframe(summary, use_container_width=True)
        else:
            st.error("File ထဲမှာ 'Agent' နဲ့ 'Pause Time' column နာမည်တွေ မှားနေပါတယ်။")
    else:
        st.warning("Sidebar တွင် IVR Call Log (CSV) ကို အရင်တင်ပေးပါ။")
