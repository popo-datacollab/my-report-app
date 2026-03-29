import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Po Po Dashboard", layout="wide")

# 2. Simplified Login Logic (Error ကင်းအောင် အသစ်ပြန်ရေးထားပါတယ်)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Po Po Dashboard")
    pwd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pwd == "12345":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Incorrect Password!")
else:
    # 3. Main Dashboard
    st.title("📊 Po Po Dashboard - All-in-One Analytics")
    
    st.sidebar.header("Data Source")
    file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    
    if file:
        df = pd.read_csv(file)
        
        # ကိန်းဂဏန်းပါတဲ့ Column နဲ့ စာသားပါတဲ့ Column ကို ခွဲထုတ်ခြင်း
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()

        if len(num_cols) > 0 and len(text_cols) > 0:
            # User စိတ်ကြိုက် Column ရွေးနိုင်အောင် လုပ်ပေးထားခြင်း
            st.sidebar.subheader("Chart Settings")
            x_axis = st.sidebar.selectbox("Select Agent/Category Name", text_cols)
            y_axis = st.sidebar.selectbox("Select Value/Pause Time", num_cols)
            
            chart_type = st.sidebar.radio("Select Chart Style", ["Bar", "Pie", "Line", "Area"])

            st.divider()

            # 4. Visualization Section
            st.subheader(f"📈 {chart_type} Chart: {y_axis} vs {x_axis}")
            
            if chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, text_auto=True)
            elif chart_type == "Pie":
                fig = px.pie(df, names=x_axis, values=y_axis, hole=0.4)
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis, markers=True)
            elif chart_type == "Area":
                fig = px.area(df, x=x_axis, y=y_axis)

            st.plotly_chart(fig, use_container_width=True)

            # Metrics
            c1, c2 = st.columns(2)
            c1.metric("Total Rows", len(df))
            c2.metric(f"Total {y_axis}", f"{df[y_axis].sum():,.0f}")
        else:
            st.warning("Your CSV must have at least one column with numbers (e.g., Pause Time) and one with text (e.g., Agent Name).")

        st.divider()
        st.subheader("📋 Raw Data Table")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Please upload a CSV file to start.")
