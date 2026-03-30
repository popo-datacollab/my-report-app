import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Config ---
st.set_page_config(page_title="Agent Dashboard", layout="wide")

# --- Sidebar Navigation Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    # Menu ရွေးချယ်စရာများ
    choice = st.radio(
        "သွားလိုသည့် Report ကို ရွေးပါ -",
        ["Home & Overview", "Pre-Order Report (R1-R3)", "Agent Pause Analysis (R4)", "Ticket Report (R5-R6)"]
    )
    st.divider()
    st.info("WPS Office မှ ထွက်လာသော CSV ဖိုင်များကို စနစ်တကျ Analysis လုပ်ပေးပါသည်။")

# --- 1. Home Page ---
if choice == "Home & Overview":
    st.title("🏠 Welcome to Agent Reporting Dashboard")
    st.write("ဘယ်ဘက် Sidebar Menu မှ မိမိကြည့်လိုသော Report ကို ရွေးချယ်နိုင်ပါသည်။")
    
    # Dashboard အကျဉ်းချုပ် ပြသရန် (နမူနာ)
    col1, col2 = st.columns(2)
    col1.metric("System Status", "Active")
    col2.metric("Project Name", "POI Analysis 2026")

# --- 2. Pre-Order Report (R1-R3) ---
elif choice == "Pre-Order Report (R1-R3)":
    st.title("📁 Pre-Order Report (R1, R2, R3)")
    file1 = st.file_uploader("Upload CSV for R1-R3", type=["csv"], key="r1_r3")
    
    st.subheader("Manual Case ID Search")
    case_ids = st.text_area("Enter Case IDs (one per line)", height=150, placeholder="POI-26-03-XXXX...")
    
    if st.button("Generate Report 3"):
        if file1 is not None:
            st.success("Data processing started...")
        else:
            st.warning("ကျေးဇူးပြု၍ File အရင်တင်ပေးပါ။")

# --- 3. Agent Pause Analysis (R4) ---
elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    st.write("Agent တစ်ဦးချင်းစီ၏ Pause Time အခြေအနေကို တွက်ချက်ခြင်း။")
    
    agent_file = st.file_uploader("Agent Data CSV ကို တင်ပါ", type=["csv"], key="agent_r4")
    
    if agent_file is not None:
        try:
            df = pd.read_csv(agent_file, encoding='latin-1')
            
            # Column Check (Agent နှင့် Pause Time)
            if 'Agent' in df.columns and 'Pause Time' in df.columns:
                # Time string ဖြစ်နေလျှင် Minutes သို့ပြောင်းရန်
                if df['Pause Time'].dtype == 'object':
                    df['Pause Time'] = pd.to_timedelta(df['Pause Time']).dt.total_seconds() / 60
                
                # Calculation
                summary = df.groupby('Agent')['Pause Time'].sum().reset_index().sort_values(by='Pause Time', ascending=False)
                
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    st.write("**Agent-wise Summary Table**")
                    st.dataframe(summary, hide_index=True, use_container_width=True)
                
                with c2:
                    st.write("**Pause Time Chart**")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    sns.barplot(data=summary, x='Agent', y='Pause Time', ax=ax, palette="viridis")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
            else:
                st.error("File ထဲတွင် 'Agent' နှင့် 'Pause Time' column များ မတွေ့ရပါ။")
        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. Ticket Report (R5-R6) ---
elif choice == "Ticket Report (R5-R6)":
    st.title("🎫 Ticket Report Analysis (R5, R6)")
    file3 = st.file_uploader("Upload Ticket CSV", type=["csv"], key="r5_r6")
    if file3 is not None:
        st.info("Ticket data received. Processing logic can be added here.")
