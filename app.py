app.pyimport streamlit as st
import pandas as pd
import plotly.express as px

# ၁။ Password သတ်မှတ်ခြင်း
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.title("🔐 My Private Dashboard")
    password = st.text_input("Password ရိုက်ထည့်ပါ", type="password")
    if st.button("Login"):
        if password == "12345": # ဒီနေရာမှာ မိမိစိတ်ကြိုက် password ပြောင်းနိုင်ပါတယ်
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ Password မှားနေပါတယ်။")
    return False

# Password မှန်မှ အောက်ကအပိုင်းကို ပြသမည်
if check_password():
    st.sidebar.title("Settings")
    st.title("📊 My Custom Report Dashboard")
    
    # ၂။ CSV File Upload တင်သည့်နေရာ
    uploaded_file = st.file_uploader("CSV file ကို ဒီမှာ Upload တင်ပါ", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.success("File Upload အောင်မြင်ပါတယ်!")
        
        # ၃။ Data အနှစ်ချုပ် ပြသခြင်း
        st.subheader("📋 Data Summary")
        st.write(df.head()) # ပထမဆုံး row ၅ ခုကို ပြပေးမယ်
        
        # ၄။ Chart များ ပြသခြင်း (ဥပမာ Column တစ်ခုခုကို ရွေးပြီး Chart ဆွဲခြင်း)
        columns = df.columns.tolist()
        st.subheader("📈 Visualization")
        
        x_axis = st.selectbox("X-axis အတွက် Column ရွေးပါ", columns)
        y_axis = st.selectbox("Y-axis အတွက် Column ရွေးပါ", columns)
        
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
        st.plotly_chart(fig)
    else:
        st.info("ရှေ့ဆက်ဖို့ CSV file လေး အရင် Upload တင်ပေးပါ။")
