import streamlit as st
import pandas as pd
import plotly.express as px

# Password သတ်မှတ်ခြင်း
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.title("🔐 My Private Dashboard")
    password = st.text_input("Password ရိုက်ထည့်ပါ", type="password")
    if st.button("Login"):
        if password == "12345":
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ Password မှားနေပါတယ်။")
    return False

if check_password():
    st.title("📊 My Custom Report Dashboard")
    uploaded_file = st.file_uploader("CSV file ကို ဒီမှာ Upload တင်ပါ", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File Upload အောင်မြင်ပါတယ်!")
        st.subheader("📋 Data Preview")
        st.write(df.head())
        
        columns = df.columns.tolist()
        st.subheader("📈 Visualization")
        x_axis = st.selectbox("X-axis ရွေးပါ", columns)
        y_axis = st.selectbox("Y-axis ရွေးပါ", columns)
        
        fig = px.bar(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)
