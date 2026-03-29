import streamlit as st
import pandas as pd
import plotly.express as px

# ၁။ Password သတ်မှတ်ခြင်း (ဒီမှာ ပြင်နိုင်ပါတယ်)
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True
    st.title("🔐 Agent Performance Dashboard")
    password = st.text_input("Password ရိုက်ထည့်ပါ", type="password")
    if st.button("Login"):
        if password == "12345": 
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ Password မှားနေပါတယ်။")
    return False

if check_password():
    st.title("📊 Agent Metrics Analysis")
    uploaded_file = st.file_uploader("Agent Data (CSV) ကို Upload တင်ပါ", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Data loaded successfully!")

        # ၂။ အပေါ်ဆုံးမှာ အနှစ်ချုပ် (Summary Metrics) ပြခြင်း
        # ဥပမာ Agent Pause Time ရဲ့ ပျမ်းမျှ သို့မဟုတ် စုစုပေါင်းကို ပြမယ်
        cols = st.columns(3)
        if "Agent Pause Time" in df.columns:
            total_pause = df["Agent Pause Time"].sum()
            avg_pause = df["Agent Pause Time"].mean()
            cols[0].metric("Total Pause Time", f"{total_pause:.2f}")
            cols[1].metric("Avg Pause Time", f"{avg_pause:.2f}")
            cols[2].metric("Total Records", len(df))

        st.divider()

        # ၃။ Charts များ ပြသခြင်း
        col1, col2 = st.columns(2)
        
        columns = df.columns.tolist()

        with col1:
            st.subheader("Comparison Chart")
            x_axis = st.selectbox("X-axis (ဥပမာ - Agent Name)", columns)
            y_axis = st.selectbox("Y-axis (ဥပမာ - Pause Time)", columns)
            fig_bar = px.bar(df, x=x_axis, y=y_axis, color=x_axis, title="Agent Comparison")
            st.plotly_chart(fig_bar, chart_type = st.radio("Chart အမျိုးအစား ရွေးပါ", ["Bar", "Line", "Area"])

if chart_type == "Bar":
    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis)
elif chart_type == "Line":
    fig = px.line(df, x=x_axis, y=y_axis)
else:
    fig = px.area(df, x=x_axis, y=y_axis)

st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Data Distribution (Pie)")
            pie_col = st.selectbox("Select column for Pie Chart", columns)
            fig_pie = px.pie(df, names=pie_col, values=y_axis if y_axis else None, title="Data Share")
            st.plotly_chart(fig_pie, use_container_width=True)

        # ၄။ Data Table
        st.subheader("📋 Full Data Table")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("CSV file လေး အရင်တင်ပေးပါဗျ။")
