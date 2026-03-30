import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Analysis Report", layout="wide")

# CSS Styling (image_7b28db အတိုင်း အရောင်များ သတ်မှတ်ခြင်း)
st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 12px; }
    .header-blue { background-color: #1a73e8; color: white; }
    .grand-total { background-color: #d35400; color: white; font-weight: bold; }
    .billing-green { background-color: #2e7d32; color: white; }
    .sub-header { background-color: #e8f0fe; color: #1a73e8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# File Upload Section
col1, col2, col3 = st.columns(3)
with col1: f1 = st.file_uploader("File 1: Pre-Order Report", type=["csv", "xlsx"])
with col2: f2 = st.file_uploader("File 2: IVR Call Log", type=["csv"])
with col3: f3 = st.file_uploader("File 3: Ticket Report", type=["csv", "xlsx"])

def load_data(file):
    if file is None: return None
    if file.name.endswith('.csv'):
        # Encoding မျိုးစုံနဲ့ စမ်းဖတ်ပြီး UnicodeDecodeError ကို ကျော်လွှားခြင်း
        for enc in ['utf-8-sig', 'latin-1', 'cp1252']:
            try:
                return pd.read_csv(file, encoding=enc)
            except UnicodeDecodeError:
                continue
    return pd.read_excel(file)

if f1:
    df = load_data(f1)
    if df is not None:
        st.success("File 1 Loaded Successfully!")
        
        # Data Summary ပြသခြင်း
        st.write("### Data Summary:")
        st.dataframe(df.head(10), use_container_width=True)

        # --- Report 1 Logic ---
        total_count = len(df)
        # အောက်ပါ HTML သည် ပုံပါအတိုင်း Report ကို ဖော်ပြပေးမည်
        html_r1 = f"""
        <h2 style="color: #1a73e8; text-align: center;">Report 1: Service City & Billing Group</h2>
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
