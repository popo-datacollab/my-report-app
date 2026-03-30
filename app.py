import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- အချိန်ပြောင်းလဲပေးသည့် Function ---
def convert_to_hms(total_minutes):
    if pd.isna(total_minutes):
        return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    MENU_HOME = "Home"
    MENU_R1 = "Pre-Order (R1-R3)"
    MENU_R4 = "Agent Pause Analysis (R4)"
    MENU_R5 = "Ticket Report (R5-R6)"

    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", [MENU_HOME, MENU_R1, MENU_R4, MENU_R5])
    st.divider()
    st.write("Logged in as: User")

# --- Agent Analysis (R4) ---
if choice == MENU_R4:
    st.title("⏱️ Agent Pause Time Analysis (Report 4)")
    agent_file = st.file_uploader("Agent Data CSV ကို တင်ရန်", type=["csv"], key="u2")
    
    if agent_file is not None:
        try:
            df = pd.read_csv(agent_file, encoding='latin-1')
            
            if 'Agent' in df.columns and 'Pause Time' in df.columns:
                # နဂို Time string ကို စုစုပေါင်းမိနစ်အဖြစ် အရင်ပြောင်းယူပါမယ်
                if df['Pause Time'].dtype == 'object':
                    df['Pause Time'] = pd.to_timedelta(df['Pause Time']).dt.total_seconds() / 60
                
                # Agent အလိုက် ပေါင်းခြင်း
                summary = df.groupby('Agent')['Pause Time'].sum().reset_index()
                
                # --- ဒီနေရာမှာ HH:MM:SS Format သို့ ပြောင်းလဲပါသည် ---
                summary['Pause Time (Formatted)'] = summary['Pause Time'].apply(convert_to_hms)
                
                # Chart အတွက် ကိန်းဂဏန်းသီးသန့် summary ကို အသုံးပြုပြီး 
                # Table မှာတော့ format ပြောင်းထားတာကို ပြပါမယ်
                summary_display = summary[['Agent', 'Pause Time (Formatted)']].rename(
                    columns={'Pause Time (Formatted)': 'Pause Time'}
                ).sort_values(by='Pause Time', ascending=False)

                c1, c2 = st.columns([1, 1.5])
                with c1:
                    st.write("**Summary Table (HH:MM:SS)**")
                    st.dataframe(summary_display, hide_index=True, use_container_width=True)
                
                with c2:
                    st.write("**Pause Time Comparison (by Minutes)**")
                    st.bar_chart(data=summary, x='Agent', y='Pause Time')
            else:
                st.error("CSV ထဲတွင် 'Agent' နှင့် 'Pause Time' Column များ မတွေ့ရပါ။")
        except Exception as e:
            st.error(f"Error: {e}")

# အခြား Page Logic များ (Home, R1, R5...)
elif choice == MENU_HOME:
    st.title("🏠 Po Po Data Dashboard")
    st.write("Welcome back!")
