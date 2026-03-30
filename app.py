import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Helper Functions ---
def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Pre-Order Logic Constants ---
GROUP1_LIST = ["AEY", "BGY", "BNY", "INY", "KGY", "KTY", "LAY", "LWY", "MEY", "MTY", "SGY", "SRY", "TEY", "TNY"]
GROUP2_LIST = ["ANM", "CIM", "MYM", "NPW", "DIN", "PIN"]
ALLOWED_TYPES = ["Installation", "TVie (New)"]
ALLOWED_CHANNELS = ["CS", "Website (Kobo)", "Social Media", "Facebook", "Loan Sale", "TikTok"]

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    MENU_HOME = "Home"
    MENU_R1 = "Pre-Order (R1-R3)"
    MENU_R4 = "Agent Pause Analysis (R4)"
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", [MENU_HOME, MENU_R1, MENU_R4])
    st.divider()
    st.write("Logged in as: User")

# --- 1. Home Page ---
if choice == MENU_HOME:
    st.title("🏠 Po Po Data Dashboard")
    st.write("Welcome! အလိုအလျောက် Data Analysis ပြုလုပ်ပေးသော Dashboard ဖြစ်ပါသည်။")
    col1, col2 = st.columns(2)
    col1.metric("System Status", "Online")
    col2.metric("Report Version", "2.0 (Integrated)")

# --- 2. Pre-Order Report (R1-R3) Integrated ---
elif choice == MENU_R1:
    st.title("📁 Pre-Order Report (R1, R2, R3)")
    file1 = st.file_uploader("Pre-Order CSV ကို တင်ပါ", type=["csv"], key="preorder_upload")
    
    if file1 is not None:
        df = pd.read_csv(file1, encoding='latin-1')
        # Data Cleaning
        df['Preorder type'] = df['Preorder type'].fillna('').str.strip()
        df['Channel'] = df['Channel'].fillna('').str.strip()
        df['Service Type'] = df['Service Type'].fillna('').str.strip()
        df['Service City'] = df['Service City'].fillna('').str.strip()
        df['Billing Group'] = df['Billing Group'].fillna('').str.strip()
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)

        # Filtering logic based on your JS code
        mask = (df['Preorder type'].isin(ALLOWED_TYPES)) & \
               (df['Channel'].isin(ALLOWED_CHANNELS)) & \
               (df['Service Type'] != "Bridge Fiber")
        filtered_df = df[mask].copy()

        # --- Report 1: Service City & Billing Group ---
        st.subheader("Report 1: Service City & Billing Group")
        
        def get_city_cat(city):
            if city in ["Yangon", "Mandalay"]: return city
            return "Other"
        
        filtered_df['City Cat'] = filtered_df['Service City'].apply(get_city_cat)
        filtered_df['Price Cat'] = filtered_df['Price'].apply(lambda x: "<30k" if x < 30000 else ">=30k")
        
        # Matrix Calculation
        report1 = filtered_df.groupby(['City Cat', 'Price Cat']).size().unstack(fill_value=0)
        
        # Billing Group Lists
        b1_count = filtered_df[filtered_df['Billing Group'].isin(GROUP1_LIST)].shape[0]
        b2_count = filtered_df[filtered_df['Billing Group'].isin(GROUP2_LIST) | filtered_df['Billing Group'].str.contains("PAN")].shape[0]

        st.write(f"**Grand Total: {filtered_df.shape[0]}**")
        st.table(report1)
        st.info(f"List 1 Count: {b1_count} | List 2/PAN Count: {b2_count}")

        # --- Report 2: Service Type Grouping ---
        st.subheader("Report 2: Service Type Grouping")
        
        def get_service_group(stype):
            if stype == "FR-SLA": return "FR-SLA"
            if stype in ["MNet Biz", "G2 Biz"]: return "Biz Group"
            if stype in ["G2 Plus", "MNet Plus"]: return "Plus Group"
            if stype in ["MNet", "G2 Net"]: return "Net Group"
            return "Other"

        filtered_df['Service Group'] = filtered_df['Service Type'].apply(get_service_group)
        report2 = filtered_df['Service Group'].value_counts().reset_index()
        st.dataframe(report2, hide_index=True, use_container_width=True)

        # --- Report 3: Manual Search ---
        st.divider()
        st.subheader("Report 3: Manual Case ID Search")
        case_input = st.text_area("Case IDs များကို ဒီနေရာတွင် ထည့်ပါ (one per line)")
        
        if st.button("Generate Report 3"):
            search_ids = [id.strip() for id in case_input.split() if id.strip()]
            r3_df = df[df['Case ID'].isin(search_ids)].copy()
            
            if not r3_df.empty:
                r3_df['Service Group'] = r3_df['Service Type'].apply(get_service_group)
                res = {
                    "Biz Group": r3_df[r3_df['Service Group'] == "Biz Group"].shape[0],
                    "Plus Group": r3_df[r3_df['Service Group'] == "Plus Group"].shape[0],
                    "FR-SLA": r3_df[r3_df['Service Group'] == "FR-SLA"].shape[0],
                    "Billing Group Match": r3_df[r3_df['Billing Group'].isin(GROUP1_LIST + GROUP2_LIST) | r3_df['Billing Group'].str.contains("PAN")].shape[0],
                    "TVie (Exchange)Only": r3_df[r3_df['Preorder type'] == "TVie (Exchange)Only"].shape[0]
                }
                st.write(res)
            else:
                st.warning("Matching Case IDs မတွေ့ပါ။")

# --- 3. Agent Analysis (R4) ---
elif choice == MENU_R4:
    st.title("⏱️ Agent Pause Time Analysis (R4)")
    agent_file = st.file_uploader("Agent CSV တင်ပါ", type=["csv"], key="agent_upload")
    
    if agent_file:
        df_agent = pd.read_csv(agent_file, encoding='latin-1')
        if 'Agent' in df_agent.columns and 'Pause Time' in df_agent.columns:
            if df_agent['Pause Time'].dtype == 'object':
                df_agent['Pause Time'] = pd.to_timedelta(df_agent['Pause Time']).dt.total_seconds() / 60
            
            summary = df_agent.groupby('Agent')['Pause Time'].sum().reset_index()
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            col_a, col_b = st.columns([1, 1.5])
            with col_a:
                st.dataframe(summary[['Agent', 'Formatted Time']].sort_values(by='Formatted Time', ascending=False), hide_index=True)
            with col_b:
                st.bar_chart(data=summary, x='Agent', y='Pause Time')
