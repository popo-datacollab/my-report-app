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
    st.title("📌 Main Menu")
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- Main Logic ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.info("ဘယ်ဘက် Menu မှ 'Pre-Order (R1-R3)' ကို ရွေးချယ်ပြီး File တင်ပေးပါ။")

elif choice == "Pre-Order (R1-R3)":
    # ထိပ်ဆုံးတွင် File Box ၃ ခု (ပုံထဲကအတိုင်း)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("File 1: Pre-Order (R1-R3)")
        f1 = st.file_uploader("Upload R1-R3", type=["csv", "xlsx"], key="u1", label_visibility="collapsed")
    with c2:
        st.info("File 2: IVR Call Log (R4)")
        f2 = st.file_uploader("Upload IVR", type=["csv"], key="u2", label_visibility="collapsed")
    with c3:
        st.success("File 3: Ticket Report (R5-R6)")
        f3 = st.file_uploader("Upload Tickets", type=["csv", "xlsx"], key="u3", label_visibility="collapsed")

    if f1:
        df = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
        
        # --- REPORT 1: SERVICE CITY & BILLING GROUP ---
        st.markdown("<h3 style='text-align: center; color: #1a73e8;'>Report 1: Service City & Billing Group</h3>", unsafe_allow_html=True)
        
        # Column အမည်များကို အလိုအလျောက်ရှာခြင်း
        city_col = next((c for c in df.columns if 'city' in c.lower() or 'address' in c.lower()), None)
        
        # Sample Calculation (Yangon, Mandalay စသဖြင့် အုပ်စုခွဲခြင်း)
        total_count = len(df)
        # ဤနေရာတွင် လူကြီးမင်း၏ Data ပေါ်မူတည်၍ Filter များပြုလုပ်နိုင်ပါသည်
        
        # ပုံထဲကအတိုင်း ဇယားကွက် ဖန်တီးခြင်း
        r1_data = {
            "Category": ["Count"],
            "Grand Total": [total_count],
            "Yangon <30k": [len(df[df[city_col].str.contains('Yangon', case=False, na=False)]) if city_col else 0],
            "Mandalay": [len(df[df[city_col].str.contains('Mandalay', case=False, na=False)]) if city_col else 0],
            "Other": [0],
            "List 1": [0],
            "List 2/PAN": [0]
        }
        st.table(pd.DataFrame(r1_data))

        # --- REPORT 2: SERVICE TYPE GROUPING ---
        st.markdown("<h3 style='text-align: center; color: #1a73e8;'>Report 2: Service Type Grouping</h3>", unsafe_allow_html=True)
        # Service Type အလိုက် အုပ်စုခွဲသည့် ဇယား
        r2_data = {
            "Category": ["Count"],
            "Grand Total": [total_count],
            "FR-SLA": [0],
            "Biz Group": [0],
            "Plus Group": [0],
            "Net Group": [0]
        }
        st.table(pd.DataFrame(r2_data))

        st.divider()

        # --- REPORT 3: MANUAL SEARCH ---
        st.subheader("🔍 Report 3: Manual Case ID Search")
        case_input = st.text_area("Case ID များကို ထည့်ပါ -", placeholder="POI-26-03-XXXX...")
        if st.button("Generate Report 3"):
            if case_input:
                search_list = [x.strip() for x in case_input.replace('\n', ',').split(',') if x.strip()]
                id_col = next((c for c in df.columns if 'case' in c.lower() or 'id' in c.lower()), None)
                if id_col:
                    res = df[df[id_col].astype(str).isin(search_list)]
                    st.dataframe(res, use_container_width=True)

elif choice == "Agent Pause Analysis (R4)":
    # Pause Time Logic များကို ဤနေရာတွင် ထားပါသည်
    st.title("⏱️ Agent Pause Time Analysis")
