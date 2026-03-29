import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Dashboard Configuration
st.set_page_config(page_title="Po Po Dashboard", layout="wide")

# 2. Login System
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
    # 3. Main Dashboard Content
    st.title("📊 Po Po Dashboard - Advanced Analytics")
    
    # Sidebar for Settings
    st.sidebar.header("Settings")
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # UI Layout: Metrics at the top
        if len(df.columns) >= 2:
            name_col = df.columns[0]
            val_col = df.columns[1]
            
            if pd.api.types.is_numeric_dtype(df[val_col]):
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Agents", len(df))
                col2.metric(f"Total {val_col}", f"{df[val_col].sum():,.0f}")
                col3.metric(f"Average {val_col}", f"{df[val_col].mean():,.2f}")

            st.divider()

            # Chart Selection Sidebar
            st.sidebar.subheader("Visualization Options")
            chart_type = st.sidebar.selectbox(
                "Select Chart Type",
                ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart", "Scatter Plot"]
            )

            # 4. Multi-Chart Generation
            st.subheader(f"📈 {chart_type} Visualization")
            
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=name_col, y=val_col, color=name_col, text_auto=True, template="plotly_white")
            
            elif chart_type == "Pie Chart":
                fig = px.pie(df, names=name_col, values=val_col, hole=0.4, template="plotly_white")
            
            elif chart_type == "Line Chart":
                fig = px.line(df, x=name_col, y=val_col, markers=True, template="plotly_white")
            
            elif chart_type == "Area Chart":
                fig = px.area(df, x=name_col, y=val_col, template="plotly_white")
            
            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=name_col, y=val_col, size=val_col, color=name_col, template="plotly_white")

            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        
        # 5. Data Table with Search
        st.subheader("📋 Detailed Data Table")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("Please upload a CSV file from the sidebar to start visualization.")
