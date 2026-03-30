import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    # Menu စာသားများကို Variable နဲ့ သတ်မှတ်လိုက်ပါမယ် (လွဲချော်မှုမရှိအောင်)
    MENU_HOME = "Home"
    MENU_R1 = "Pre-Order (R1-R3)"
    MENU_R4 = "Agent Pause Analysis (R4)"
    MENU_R5 = "Ticket Report (R5-R6)"

    choice = st.radio(
        "သွားလိုသည့် Report ကို ရွေးပါ -",
        [MENU_HOME, MENU_R1, MENU_R4, MENU_R5]
    )
    st.divider()
    st.write("Logged in as: User")

# --- 1. Home Page ---
if choice == MENU_HOME:
    st.title("🏠 Po Po Data Dashboard")
    st.write("Welcome! ဘယ်ဘက် Sidebar မှ မိမိကြည့်လိုသော Report ကို ရွေးချယ်ပါ။")
    
    col1, col2 = st.columns(2)
    col1.metric("Status", "Online")
    col2.metric("Project", "POI 2026")

# --- 2. Pre-Order Report (R1-R3) ---
elif choice == MENU_R1:
    st.title("📁 Pre-Order Report (R1, R2, R3)")
    file1 = st.file_uploader("Upload CSV 1", type=["csv"], key="u1")
    
    st.subheader("Manual Case ID Search")
    case_ids = st.text_area("Enter Case IDs (one per line)", height=150)
    
    if st.button("Generate Report 3"):
        if file1 is not None:
            st.success("File Received!")
        else:
            st.warning("Please upload file 1 first.")

# --- 3. Agent Analysis (R4) ---
elif choice == MENU_R4:
    st.title("⏱️ Agent Pause Time Analysis (Report 4)")
    st.write("Agent တစ်ဦးချင်းစီ၏ Pause Time အခြေအနေကို စစ်ဆေးရန် CSV File တင်ပေးပါ။")
    
    # File Uploader ကို အမြဲပေါ်နေအောင် လုပ်ထားပါတယ်
    agent_file = st.file_uploader("Agent Data CSV ကို တင်ရန်", type=["csv"], key="u2")
    
    if agent_file is not None:
        try:
            # File ဖတ်ခြင်း
            df = pd.read_csv(agent_file, encoding='latin-1')
            
            # Column နာမည်ကို Agent (သို့မဟုတ်) Agent Name ဖြစ်ဖြစ် ဖတ်လို့ရအောင် လုပ်ပေးထားပါတယ်
            # Pause Time ကိုလည်း အလားတူ စစ်ဆေးပါတယ်
            if 'Agent' in df.columns and 'Pause Time' in df.columns:
                
                # Time string ဖြစ်နေလျှင် Minutes သို့ပြောင်းရန်
                if df['Pause Time'].dtype == 'object':
                    df['Pause Time'] = pd.to_timedelta(df['Pause Time']).dt.total_seconds() / 60
                
                summary = df.groupby('Agent')['Pause Time'].sum().reset_index().sort_values(by='Pause Time', ascending=False)
                
                # UI Layout ခွဲခြင်း
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    st.write("**Summary Table**")
                    st.dataframe(summary, hide_index=True, use_container_width=True)
                
                with c2:
                    st.write("**Pause Time Chart**")
                    st.bar_chart(data=summary, x='Agent', y='Pause Time')
            else:
                st.error("CSV ထဲတွင် 'Agent' နှင့် 'Pause Time' Column အမည်များ မတွေ့ရပါ။ ကျေးဇူးပြု၍ စစ်ဆေးပေးပါ။")
                st.write("သင့် File ထဲရှိ Column များမှာ -", list(df.columns))
        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. Ticket Report (R5-R6) ---
elif choice == MENU_R5:
    st.title("🎫 Ticket Report (R5, R6)")
    file3 = st.file_uploader("Upload Ticket CSV", type=["csv"], key="u3")
