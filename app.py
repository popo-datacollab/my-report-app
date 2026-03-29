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
    # 3. Main Dashboard
    st.title("📊 Po Po Dashboard - Universal Analysis")
    st.sidebar.header("Data Control Center")
    file = st.sidebar.file_uploader("Upload WPS, Excel or CSV", type=["csv", "xlsx", "xls"])
    
    if file:
        try:
            # --- ပိုမိုကောင်းမွန်သော File Reading စနစ် ---
            if file.name.endswith('.csv'):
                # encoding='latin1' သုံးခြင်းက utf-8 error ကို ကျော်လွှားနိုင်ပါတယ်
                df = pd.read_csv(file, encoding='latin1')
            else:
                df = pd.read_excel(file, engine='openpyxl')
            
            # Clean data: Column နာမည်တွေမှာ ပါနေတဲ့ space တွေကို ဖယ်ရှားခြင်း
            df.columns = df.columns.str.strip()

            # Data Analysis
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

            if len(num_cols) > 0:
                st.sidebar.subheader("🎯 Analysis Settings")
                # နာမည်ပြရမယ့် Column (X-axis)
                x_axis = st.sidebar.selectbox("Select Name/Agent Column", text_cols if text_cols else df.columns)
                # တန်ဖိုးပြရမယ့် Column (Y-axis)
                y_axis = st.sidebar.selectbox("Select Value (e.g. Pause Time)", num_cols)
                
                chart_type = st.sidebar.radio("Select Chart Style", ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart"])

                # 4. Dashboard Metrics
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Records", len(df))
                m2.metric(f"Total {y_axis}", f"{df[y_axis].sum():,.0f}")
                m3.metric(f"Average", f"{df[y_axis].mean():,.2f}")

                # 5. Visualizations
                st.subheader(f"📈 {chart_type} Analysis")
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, text_auto=True, template="plotly_dark")
                elif chart_type == "Pie Chart":
                    fig = px.pie(df, names=x_axis, values=y_axis, hole=0.4, template="plotly_dark")
                elif chart_selection == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_dark")
                else:
                    fig = px.area(df, x=x_axis, y=y_axis, template="plotly_dark")

                st.plotly_chart(fig, use_container_width=True)

                st.divider()
                st.subheader("📋 Full Data Table")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ ဖိုင်ထဲမှာ ကိန်းဂဏန်း (Numbers) ပါတဲ့ column မတွေ့ရပါ။ ကျေးဇူးပြု၍ ဖိုင်ကို စစ်ဆေးပေးပါ။")

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            st.info("💡 Tip: တကယ်လို့ CSV နဲ့ မရရင် WPS ထဲမှာ .xlsx (Excel) အနေနဲ့ Save ပြီး ပြန်တင်ကြည့်ပါဗျာ။")
    else:
        st.info("👋 Welcome! Please upload your file to start the analysis.")
