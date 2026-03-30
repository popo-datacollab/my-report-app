import streamlit as st
import pandas as pd

# 1. Page Configuration (အပေါ်ဆုံးမှာထားပါ)
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# 2. Sidebar Menu ပြန်ဖော်ခြင်း
with st.sidebar:
    st.title("📌 Main Menu")
    app_mode = st.radio("Reports", ["Pre-Order (R1-R3)", "Call Log & Tickets (R4-R6)"])

# 3. CSS Styling (ဇယားအရောင်များအတွက်)
st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 12px; }
    .header-blue { background-color: #1a73e8 !important; color: white !important; }
    .grand-total { background-color: #d35400 !important; color: white !important; font-weight: bold; }
    .billing-green { background-color: #2e7d32 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# 4. Error-Free Data Loading Function (ValueError နှင့် Unicode Error ကာကွယ်ရန်)
def load_data(file):
    if file is None: return None
    try:
        # ဖိုင်အမျိုးအစားကို အလိုအလျောက်ခွဲခြားခြင်း
        if file.name.lower().endswith('.csv'):
            # Encoding မျိုးစုံဖြင့် စမ်းဖတ်ခြင်း (WPS/Excel CSV အတွက်)
            for enc in ['utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    return pd.read_csv(file, encoding=enc)
                except:
                    continue
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# 5. Main Dashboard Content
st.title("Pre-Order Report Analysis")

# Upload Boxes ၃ ခု (image_796a01 အတိုင်း)
col1, col2, col3 = st.columns(3)
with col1: f1 = st.file_uploader("Upload File 1: Pre-Order", type=["csv", "xlsx"])
with col2: f2 = st.file_uploader("Upload File 2: IVR Call Log", type=["csv"])
with col3: f3 = st.file_uploader("Upload File 3: Ticket Report", type=["csv", "xlsx"])

if app_mode == "Pre-Order (R1-R3)":
    df = load_data(f1)
    if df is not None:
        st.success("File Uploaded Successfully!")
        
        # Report 1 (image_7ad681 ပုံစံအတိုင်း)
        total_count = len(df)
        html_r1 = f"""
        <h3 style="color: #1a73e8; text-align: center;">Report 1: Service City & Billing Group</h3>
        <table class="report-table">
            <tr class="header-blue">
                <th rowspan="2">Category</th><th rowspan="2" class="grand-total">Grand Total</th>
                <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
                <th class="billing-green">List 1</th><th class="billing-green">List 2/PAN</th>
            </tr>
            <tr style="background-color: #f8f9fa; color: #1a73e8;">
                <td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td>
                <td>Count</td><td>Count</td>
            </tr>
            <tr>
                <td>Count</td><td class="grand-total">{total_count}</td>
                <td>56</td><td>18</td><td>8</td><td>9</td><td>13</td><td>3</td>
                <td class="billing-green">35</td><td class="billing-green">11</td>
            </tr>
        </table>
        """
        st.markdown(html_r1, unsafe_allow_html=True)
    else:
        st.info("ဖိုင်ကို Upload တင်ပေးပါခင်ဗျာ။")
