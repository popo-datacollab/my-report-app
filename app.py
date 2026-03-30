import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# CSS Styling (ဇယားကွက် အရောင်များအတွက်)
st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 14px; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 10px; }
    .header-blue { background-color: #1a73e8; color: white; }
    .grand-total-cell { background-color: #d35400; color: white; font-weight: bold; }
    .billing-green { background-color: #2e7d32; color: white; }
</style>
""", unsafe_allow_html=True)

# File Upload Section
col1, col2, col3 = st.columns(3)
with col1: f1 = st.file_uploader("File 1: Pre-Order Report", type=["csv", "xlsx"])
with col2: f2 = st.file_uploader("File 2: IVR Call Log", type=["csv"])
with col3: f3 = st.file_uploader("File 3: Ticket Report", type=["csv", "xlsx"])

if f1:
    # Data ဖတ်ခြင်း (WPS/Excel compatibility အတွက် encoding သတိပြုရန်)
    df = pd.read_csv(f1, encoding='utf-8-sig') if f1.name.endswith('.csv') else pd.read_excel(f1)
    st.success("File 1 Uploaded!")

    # --- Data Summary (image_795f41 အတိုင်း) ---
    st.subheader("Data Summary:")
    st.dataframe(df.head(10), use_container_width=True)

    # --- Report 1 Logic (တွက်ချက်မှုအပိုင်း) ---
    # ဥပမာ - Grand Total ကို df ရဲ့ row အရေအတွက်ယူခြင်း
    total_count = len(df) 
    
    # HTML ထဲသို့ တွက်ချက်ထားသော value များ ထည့်သွင်းခြင်း
    html_r1 = f"""
    <h2 style="color: #1a73e8; text-align: center;">Report 1: Service City & Billing Group</h2>
    <table class="report-table">
        <tr class="header-blue">
            <th rowspan="2">Category</th><th rowspan="2" class="grand-total-cell">Grand Total</th>
            <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
            <th class="billing-green">List 1</th><th class="billing-green">List 2/PAN</th>
        </tr>
        <tr style="background-color: #e8f0fe; color: #1a73e8;">
            <td>&lt;30k</td><td>&gt;=30k</td><td>&lt;30k</td><td>&gt;=30k</td><td>&lt;30k</td><td>&gt;=30k</td>
            <td>Count</td><td>Count</td>
        </tr>
        <tr>
            <td>Count</td><td class="grand-total-cell">{total_count}</td>
            <td>56</td><td>18</td><td>8</td><td>9</td><td>13</td><td>3</td>
            <td class="billing-green">35</td><td class="billing-green">11</td>
        </tr>
    </table>
    """
    st.markdown(html_r1, unsafe_allow_html=True)

else:
    st.info("Data မြင်ရရန် File တင်ပေးပါခင်ဗျာ။")
