import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Po Po Dashboard", layout="wide")

# 2. Login Security
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
    # 3. Main Dashboard Header
    st.title("📊 Po Po Dashboard - WPS & Excel Support")
    
    st.sidebar.header("Data Control Center")
    # WPS Spreadsheets အများစုသုံးတဲ့ format အားလုံးကို လက်ခံရန် ပြင်ဆင်ထားပါတယ်
    file = st.sidebar.file_uploader("Upload WPS or Excel File", type=["csv", "xlsx", "xls", "xlsm"])
    
    if file:
        try:
            # ဖိုင်အမျိုးအစားအလိုက် ခွဲခြားဖတ်ခြင်း
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                # WPS xlsx/xls ဖိုင်များကို engine='openpyxl' ဖြင့် ဖတ်ခြင်း
                df = pd.read_excel(file, engine='openpyxl')
            
            # ကိန်းဂဏန်း (Numbers) နဲ့ စာသား (Text) Column များကို ခွဲခြားခြင်း
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()

            if len(num_cols) > 0 and len(text_cols) > 0:
                st.sidebar.subheader("Visualization Settings")
                x_axis = st.sidebar.selectbox("Category (e.g. Agent Name)", text_cols)
                y_axis = st.sidebar.selectbox("Value (e.g. Pause Time)", num_cols)
                
                chart_selection = st.sidebar.radio("Select Chart Style", 
                                                 ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart", "Scatter Plot"])

                st.divider()

                # 4. Chart Display
                st.subheader(f"📈 {chart_selection}: {y_axis} vs {x_axis}")
                
                if chart_selection == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, text_auto=True, template="plotly_dark")
                elif chart_selection == "Pie Chart":
                    fig = px.pie(df, names=x_axis, values=y_axis, hole=0.4, template="plotly_dark")
                elif chart_selection == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_dark")
                elif chart_selection == "Area Chart":
                    fig = px.area(df, x=x_axis, y=y_axis, template="plotly_dark")
                elif chart_selection == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, size=y_axis, color=x_axis, template="plotly_dark")

                st.plotly_chart(fig, use_container_width=True)

                # Metrics Summary
                st.markdown("### 📌 Statistics")
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Rows", len(df))
                m2.metric(f"Total {y_axis}", f"{df[y_axis].sum():,.0f}")
                m3.metric(f"Average {y_axis}", f"{df[y_axis].mean():,.2f}")

            else:
                st.warning("Ensure your WPS file has at least one Text column and one Numeric column.")

            st.divider()
            st.subheader("📋 Data Preview")
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Error reading WPS/Excel file: {e}")
    else:
        st.info("👋 Ready to analyze! Please upload your WPS (.xlsx) or CSV file.")
