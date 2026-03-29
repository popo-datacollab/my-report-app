import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Po Po Dashboard", layout="wide")

# 2. Simplified Login Security
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
    # CSV, XLSX, XLS, XLSM အကုန်ဖတ်နိုင်အောင် လုပ်ထားပါတယ်
    file = st.sidebar.file_uploader("Upload WPS or Excel File", type=["csv", "xlsx", "xls", "xlsm"])
    
    if file:
        try:
            # ဖိုင်အမျိုးအစားအလိုက် ခွဲခြားဖတ်ခြင်း
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                # Excel ဖိုင်များအတွက် openpyxl ကို အသုံးပြုခြင်း
                df = pd.read_excel(file)
            
            # ကိန်းဂဏန်း (Numbers) နဲ့ စာသား (Text) Column များကို ခွဲခြားခြင်း
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()

            if len(num_cols) > 0 and len(text_cols) > 0:
                st.sidebar.subheader("Visualization Settings")
                x_axis = st.sidebar.selectbox("Choose Category (Names/ID)", text_cols)
                y_axis = st.sidebar.selectbox("Choose Value (Pause Time/Amount)", num_cols)
                
                chart_selection = st.sidebar.radio("Select Chart Style", ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart"])

                st.divider()

                # 4. Chart Display Section
                st.subheader(f"📈 {chart_selection}: {y_axis} vs {x_axis}")
                
                if chart_selection == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, text_auto=True, template="plotly_dark")
                elif chart_selection == "Pie Chart":
                    fig = px.pie(df, names=x_axis, values=y_axis, hole=0.4, template="plotly_dark")
                elif chart_selection == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_dark")
                elif chart_selection == "Area Chart":
                    fig = px.area(df, x=x_axis, y=y_axis, template="plotly_dark")

                st.plotly_chart(fig, use_container_width=True)

                # Metrics
                st.markdown("### 📌 Statistics")
                m1, m2 = st.columns(2)
                m1.metric("Total Rows", len(df))
                m2.metric(f"Total {y_axis}", f"{df[y_axis].sum():,.0f}")

            else:
                st.warning("Ensure your file has at least one text column and one numeric column.")

            st.divider()
            st.subheader("📋 Raw Data Table")
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("👋 Ready to analyze! Please upload your file from the sidebar.")
