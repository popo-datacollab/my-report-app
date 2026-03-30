import streamlit as st
import pandas as pd

# 1. Page Configuration (Browser Tab မှာ ပြမယ့် အမည်)
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio(
        "သွားလိုသည့် Report ကို ရွေးပါ -",
        ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)", "Ticket Report (R5-R6)"]
    )
    st.divider()
    st.write("Logged in as: User")

# --- 1. Home Page ---
if choice == "Home":
    st.title("🏠 Po Po Data Dashboard")
    st.write("Welcome to the automated reporting system. ဘယ်ဘက် Sidebar မှ မိမိကြည့်လိုသော Report ကို ရွေးချယ်ပါ။")
    
    # Dashboard ကိန်းဂဏန်း အကျဉ်းချုပ်
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Online")
    col2.metric("Project", "POI 2026")
    col3.metric("Platform", "Streamlit Cloud")

# --- 2. Pre-Order Report (R1-R3) ---
elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report (R1, R2, R3)")
    file1 = st.file_uploader("Upload CSV 1", type=["csv"], key="u1")
    
    st.subheader("Manual Case ID Search")
    case_ids = st.text_area("Enter Case IDs (one per line)", height=150, placeholder="POI-26-03-XXXX...")
    
    if st.button("Generate Report 3", type="primary"):
        if file1 is not None:
            st.success("Report 3 Generated!")
        else:
            st.warning("ကျေးဇူးပြု၍ File 1 ကို အရင်တင်ပေးပါ။")

# --- 3. Agent Analysis (R4) ---
elif choice == "Agent Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis (Report 4)")
    agent_file = st.file_uploader("Agent Data CSV ကို တင်ပါ", type=["csv"], key="u2")
    
    if agent_file is not None:
        try:
            df = pd.read_csv(agent_file, encoding='latin-1')
            
            if 'Agent' in df.columns and 'Pause Time' in df.columns:
                # Time string ဖြစ်နေလျှင် Minutes သို့ပြောင်းရန်
                if df['Pause Time'].dtype == 'object':
                    df['Pause Time'] = pd.to_timedelta(df['Pause Time']).dt.total_seconds() / 60
                
                summary = df.groupby('Agent')['Pause Time'].sum().reset_index().sort_values(by='Pause Time', ascending=False)
                
                # Layout ခွဲပြခြင်း
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    st.write("**Summary Table**")
                    st.dataframe(summary, hide_index=True, use_container_width=True)
                
                with c2:
                    st.write("**Pause Time Chart**")
                    # Streamlit Built-in Chart (matplotlib မလိုဘဲ error ကင်းကင်း သုံးနိုင်သည်)
                    st.bar_chart(data=summary, x='Agent', y='Pause Time')
            else:
                st.error("CSV ထဲတွင် 'Agent' နှင့် 'Pause Time' Column အမည်များ မတွေ့ရပါ။")
        except Exception as e:
            st.error(f"Error occurred: {e}")

# --- 4. Ticket Report (R5-R6) ---
elif choice == "Ticket Report (R5-R6)":
    st.title("🎫 Ticket Report (R5, R6)")
    file3 = st.file_uploader("Upload Ticket CSV", type=["csv"], key="u3")
    if file3 is not None:
        st.info("Ticket data processing area...")
