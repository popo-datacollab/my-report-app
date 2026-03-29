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
    st.title("📊 Po Po Dashboard Summary")
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Displaying the raw data table
        st.subheader("📋 Uploaded Data Table")
        st.dataframe(df, use_container_width=True)
        
        st.divider()

        # 4. Automatic Chart Generation
        # Uses the 1st column for Names (X) and 2nd column for Values (Y)
        if len(df.columns) >= 2:
            st.subheader("📈 Performance Chart")
            
            x_axis = df.columns[0] 
            y_axis = df.columns[1] 
            
            fig = px.bar(
                df, 
                x=x_axis, 
                y=y_axis, 
                color=x_axis,
                text_auto=True,
                title=f"{y_axis} by {x_axis}",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary Calculation
            if pd.api.types.is_numeric_dtype(df[y_axis]):
                total_val = df[y_axis].sum()
                st.info(f"Total {y_axis}: **{total_val}**")
        else:
            st.warning("The CSV file needs at least 2 columns to create a chart.")
            
    else:
        st.info("Please upload a CSV file to generate the report.")
