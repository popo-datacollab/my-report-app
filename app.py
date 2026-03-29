import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard Setting (စာမျက်နှာ အပြင်အဆင်)
st.set_page_config(page_title="Agent Performance AI", layout="wide")

# ၁။ Password System
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True
    
    st.markdown("<h1 style='text-align: center;'>🔐 Secure Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        password = st.text_input("Please enter your password", type="password")
        if st.button("Access Dashboard"):
            if password == "12345":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("❌ Invalid Password!")
    return False

if check_password():
    # Dashboard Header
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>📊 Agent Performance Analytics</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Side Bar (File Upload)
    st.sidebar.header("📂 Data Upload")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # ၂။ Metric Summary Cards (အနှစ်ချုပ် ဂဏန်းများ)
        st.subheader("📌 Quick Summary")
        m1, m2, m3, m4 = st.columns(4)
        
        # Agent Pause Time ပါမပါ စစ်ဆေးခြင်း
        pause_col = "Agent Pause Time" if "Agent Pause Time" in df.columns else df.columns[1]
        
        total_pause = df[pause_col].sum() if pd.api.types.is_numeric_dtype(df[pause_col]) else 0
        avg_pause = df[pause_col].mean() if pd.api.types.is_numeric_dtype(df[pause_col]) else 0
        
        m1.metric("Total Pause Time", f"{total_pause:,.0f} min", delta="Minutes")
        m2.metric("Average Pause", f"{avg_pause:.2f} min")
        m3.metric("Total Agents/Records", len(df))
        m4.metric("Status", "🟢 Live Data")

        st.divider()

        # ၃။ Interactive Tabs (Report ကို ကဏ္ဍခွဲကြည့်ရန်)
        tab1, tab2, tab3 = st.tabs(["📈 Visualization", "📋 Data Explorer", "⚙️ Settings"])

        with tab1:
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("### 📊 Agent Comparison (Bar)")
                x_ax = st.selectbox("Select Agent Column (X)", df.columns)
                y_ax = st.selectbox("Select Value Column (Y)", df.columns, index=min(len(df.columns)-1, 1))
                
                fig_bar = px.bar(df, x=x_ax, y=y_ax, color=x_ax, 
                                 text_auto='.2s', 
                                 template="plotly_dark",
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_right:
                st.markdown("### 🍕 Distribution (Pie)")
                pie_target = st.selectbox("Select Column for Pie Chart", df.columns, index=0)
                fig_pie = px.pie(df, names=pie_target, values=y_ax, 
                                 hole=0.4, 
                                 template="plotly_dark",
                                 color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Line Chart for trends
            st.markdown("### 📉 Performance Trend")
            fig_line = px.line(df, x=x_ax, y=y_ax, markers=True, 
                               template="plotly_dark", 
                               line_shape="spline", 
                               render_mode="svg")
            st.plotly_chart(fig_line, use_container_width=True)

        with tab2:
            st.markdown("### 🔍 Search & Filter Data")
            st.dataframe(df, use_container_width=True)
            
            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Processed CSV", data=csv, file_name="agent_report.csv", mime="text/csv")

        with tab3:
            st.info("Additional dashboard settings and customization will be added here.")
            
    else:
        # File မရှိသေးခင် ပြမည့် ပုံရိပ်
        st.info("👋 Welcome! Please upload your CSV file in the sidebar to generate charts.")
        st.image("https://raw.githubusercontent.com/streamlit/documentation/main/assets/images/streamlit_logo.png", width=200)
