import streamlit as st
import pandas as pd

# 1. Page Configuration (အကျယ်ချဲ့ခြင်း)
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# 2. CSS Styling (အရောင်နှင့် ဇယားပုံစံများ - image_7ad681 အတိုင်း)
st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; font-family: sans-serif; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 12px; }
    .header-blue { background-color: #1a73e8 !important; color: white !important; }
    .grand-total { background-color: #d35400 !important; color: white !important; font-weight: bold; }
    .billing-green { background-color: #2e7d32 !important; color: white !important; }
    .sub-header { background-color: #f8f9fa; color: #1a73e8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Menu (ဘေးက Menu Bar ပြန်ဖော်ရန်)
with st.sidebar:
    st.title("📌 Main Menu")
    app_mode = st.radio("Reports", ["Pre-Order (R1-R3)", "Call Log & Tickets (R4-R6)"])

# 4. Data Loading Function (Encoding Error ကာကွယ်ရန်)
def load_data(file):
    if file is None: return None
    if file.name.endswith('.csv'):
        # WPS/Excel CSV format မျိုးစုံကို ဖတ်နိုင်ရန်
        for enc in ['utf-8-sig', 'latin-1', 'cp1252']:
            try:
                return pd.read_csv(file, encoding=enc)
            except:
                continue
    return pd.read_excel(file)

# 5. Main Dashboard Header
st.title("Pre-Order Report Analysis")

# File Upload Section (image_796a01 ပုံစံအတိုင်း ၃ ခုခွဲထားခြင်း)
col1, col2, col3 = st.columns(3)
with col1: f1 = st.file_uploader("Upload File 1: Pre-Order Report", type=["csv", "xlsx"])
with col2: f2 = st.file_uploader("Upload File 2: IVR Call Log", type=["csv"])
with col3: f3 = st.file_uploader("Upload File 3: Ticket Report", type=["csv", "xlsx"])

# --- Logic for Pre-Order (R1-R3) ---
if app_mode == "Pre-Order (R1-R3)":
    if f1:
        df = load_data(f1)
        st.success("File 1 Uploaded Successfully!")
        
        # Data Summary (image_795f41 အတိုင်း)
        st.write("### Data Summary:")
        st.dataframe(df.head(10), use_container_width=True)

        # Report 1 (image_7ad681 ပုံစံအတိုင်း)
        total_count = len(df)
        html_r1 = f"""
        <h3 style="color: #1a73e8; text-align: center;">Report 1: Service City & Billing Group</h3>
        <table class="report-table">
            <thead>
                <tr class="header-blue">
                    <th rowspan="2">Category</th><th rowspan="2" class="grand-total">Grand Total</th>
                    <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
                    <th class="billing-green">List 1</th><th class="billing-green">List 2/PAN</th>
                </tr>
                <tr class="sub-header">
                    <td>&lt;30k</td><td>&gt;=30k</td><td>&lt;30k</td><td>&gt;=30k</td><td>&lt;30k</td><td>&gt;=30k</td>
                    <td>Count</td><td>Count</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Count</td><td class="grand-total">{total_count}</td>
                    <td>56</td><td>18</td><td>8</td><td>9</td><td>13</td><td>3</td>
                    <td class="billing-green">35</td><td class="billing-green">11</td>
                </tr>
            </tbody>
        </table>
        """
        st.markdown(html_r1, unsafe_allow_html=True)

        # Report 2
        st.markdown("<br>", unsafe_allow_html=True)
        html_r2 = f"""
        <h3 style="color: #1a73e8; text-align: center;">Report 2: Service Type Grouping</h3>
        <table class="report-table">
            <tr class="header-blue">
                <th>Category</th><th class="grand-total">Grand Total</th>
                <th>FR-SLA</th><th>Biz Group</th><th>Plus Group</th><th>Net Group</th><th>Other</th>
            </tr>
            <tr>
                <td>Count</td><td class="grand-total">{total_count}</td>
                <td>20</td><td>1</td><td>35</td><td>51</td><td>0</td>
            </tr>
        </table>
        """
        st.markdown(html_r2, unsafe_allow_html=True)
    else:
        st.info("File 1 (Pre-Order Report) ကို အရင်တင်ပေးပါခင်ဗျာ။")

# --- Logic for Call Log & Tickets (R4-R6) ---
elif app_mode == "Call Log & Tickets (R4-R6)":
    st.write("### Call Log & Ticket Analysis Section")
    # ဤနေရာတွင် Report 4, 5, 6 အတွက် ဇယားများ ထည့်သွင်းနိုင်သည်
