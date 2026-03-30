import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .grand-total { background-color: #d35400 !important; color: white; font-weight: bold; text-align: center; }
    .report-header { color: #1a73e8; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 30px; font-size: 24px; font-weight: bold; text-align: center; }
    .pause-card { background-color: #f8f9fa; border-left: 5px solid #e74c3c; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    # Menu Bar မှာ Pause Time ထည့်သွင်းခြင်း
    choice = st.radio("Reports", ["Pre-Order (R1-R3)", "Call Log & Tickets (R4-R6)", "Pause Time Analysis"])

# --- Pre-Order & Tickets Logic (အရင်အတိုင်းထားပါသည်) ---
if choice == "Pre-Order (R1-R3)":
    st.markdown('<div class="report-header">Pre-Order Report Analysis</div>', unsafe_allow_html=True)
    f1 = st.file_uploader("Upload File 1: Pre-Order Report", type=["csv", "xlsx"])
    if f1:
        # ... (အရင်က အဆင်ပြေခဲ့သည့် Pre-Order Code များ ဤနေရာတွင် ရှိပါမည်) ...
        st.success("Pre-Order Data ဖတ်ရှုပြီးပါပြီ။")
        # (image_796a01.png ထဲကအတိုင်း ဇယားများ ပေါ်လာပါမည်)

elif choice == "Call Log & Tickets (R4-R6)":
    st.markdown('<div class="report-header">Call Log & Ticket Analysis</div>', unsafe_allow_html=True)
    # ... (R4-R6 Code များ) ...

# --- NEW: PAUSE TIME ANALYSIS MENU ---
elif choice == "Pause Time Analysis":
    st.markdown('<div class="report-header">⏱️ Pause Time Analysis</div>', unsafe_allow_html=True)
    
    f_pause = st.file_uploader("Agent CSV File ကို တင်ပါ", type=["csv"])

    if f_pause:
        try:
            # Encoding ပြဿနာမရှိအောင် latin-1 ဖြင့်ဖတ်ခြင်း
            dfp = pd.read_csv(f_pause, encoding='latin-1')
            dfp.columns = dfp.columns.str.strip() # Space များဖြတ်ခြင်း

            # Column နာမည်များကို ရှာဖွေခြင်း (KeyError မတက်စေရန်)
            agent_col = next((c for c in dfp.columns if 'Agent' in c), None)
            pause_col = next((c for c in dfp.columns if 'Pause' in c and 'Time' in c), None)
            reason_col = next((c for c in dfp.columns if 'Reason' in c), None)

            if agent_col and pause_col:
                st.subheader("📊 Summary by Agent")
                
                # Pause Time ကို စုစုပေါင်းတွက်ချက်ခြင်း (Raw Data အတိုင်းပြသခြင်း)
                summary = dfp.groupby([agent_col, reason_col])[pause_col].sum().reset_index() if reason_col else dfp.groupby(agent_col)[pause_col].sum().reset_index()
                
                # အလှဆုံးဖြစ်အောင် Table ပြသခြင်း
                st.dataframe(summary, use_container_width=True, hide_index=True)
                
                st.divider()
                st.subheader("📑 Detailed View")
                st.write(dfp)
            else:
                st.error("ဖိုင်ထဲတွင် 'Agent' သို့မဟုတ် 'Pause Time' column မတွေ့ပါ။ ကျေးဇူးပြု၍ ဖိုင်မှန်မမှန် စစ်ဆေးပေးပါ။")
        
        except Exception as e:
            st.error(f"Error ဖြစ်ပွားပါသည်: {e}")
    else:
        st.info("Agent Availability CSV ဖိုင်ကို အပေါ်တွင် တင်ပေးပါခင်ဗျာ။")
