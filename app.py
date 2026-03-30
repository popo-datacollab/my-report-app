import streamlit as st
import pandas as pd
import io

# 1. Page Config & CSS Styling
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 20px; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 10px; }
    .header-blue { background-color: #1a73e8 !important; color: white !important; }
    .grand-total { background-color: #d35400 !important; color: white !important; font-weight: bold; }
    .billing-green { background-color: #2e7d32 !important; color: white !important; }
    .sub-header { background-color: #f8f9fa; color: #1a73e8; font-weight: bold; }
    .report5-card { background: white; border-left: 10px solid #1a73e8; padding: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .count-num { font-size: 45px; font-weight: bold; color: #1a73e8; margin: 0; }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Menu
with st.sidebar:
    st.title("📌 Main Menu")
    app_mode = st.radio("Choose Analysis", ["Pre-Order (R1-R3)", "Call Log & Ticket (R4-R6)"])

# 3. CSV Loading with Error Handling
def load_data(file):
    if file is None: return None
    try:
        # Encoding မျိုးစုံဖြင့် စမ်းဖတ်ပြီး Error ကာကွယ်ခြင်း
        content = file.read()
        for enc in ['utf-8-sig', 'latin-1', 'cp1252']:
            try:
                return pd.read_csv(io.BytesIO(content), encoding=enc)
            except:
                continue
        st.error("ဖိုင်ကို ဖတ်၍မရပါ။ CSV Format မှန်မမှန် စစ်ဆေးပါ။")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Global Lists (လူကြီးမင်းပေးထားသော List များ)
group1 = ["AEY", "BGY", "BNY", "INY", "KGY", "KTY", "LAY", "LWY", "MEY", "MTY", "SGY", "SRY", "TEY", "TNY"]
group2 = ["ANM", "CIM", "MYM", "NPW", "DIN", "PIN"]

# 4. Main UI
st.title("📊 Comprehensive Data Analysis (Report 1-6)")

# Upload Boxes
c1, c2, c3 = st.columns(3)
with c1: f1 = st.file_uploader("File 1: Pre-Order Report", type=["csv"])
with c2: f2 = st.file_uploader("File 2: IVR Call Log", type=["csv"])
with c3: f3 = st.file_uploader("File 3: Ticket Report", type=["csv"])

df1 = load_data(f1)
df2 = load_data(f2)
df3 = load_data(f3)

if app_mode == "Pre-Order (R1-R3)":
    if df1 is not None:
        # Pre-filter Data
        allowed_types = ["Installation", "TVie (New)"]
        allowed_channels = ["CS", "Website (Kobo)", "Social Media", "Facebook", "Loan Sale", "TikTok"]
        
        filtered_df = df1[
            (df1['Preorder type'].isin(allowed_types)) & 
            (df1['Channel'].isin(allowed_channels)) & 
            (df1['Service Type'] != "Bridge Fiber")
        ].copy()

        # Report 1: City & Billing Group Logic
        total = len(filtered_df)
        b1_count = filtered_df[filtered_df['Billing Group'].isin(group1)].shape[0]
        b2_count = filtered_df[filtered_df['Billing Group'].isin(group2) | filtered_df['Billing Group'].str.contains("PAN", na=False)].shape[0]

        st.markdown(f"""
        <h3 style="color:#1a73e8; text-align:center;">Report 1: Service City & Billing Group</h3>
        <table class="report-table">
            <tr class="header-blue">
                <th rowspan="2">Category</th><th rowspan="2" class="grand-total">Grand Total</th>
                <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
                <th class="billing-green">List 1</th><th class="billing-green">List 2/PAN</th>
            </tr>
            <tr class="sub-header">
                <td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td>
                <td>Count</td><td>Count</td>
            </tr>
            <tr>
                <td>Count</td><td class="grand-total">{total}</td>
                <td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>
                <td class="billing-green">{b1_count}</td><td class="billing-green">{b2_count}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

        # Report 3: Manual Search
        st.subheader("Report 3: Manual Case ID Search")
        case_input = st.text_area("Case ID များထည့်ရန် (POI-...)")
        if st.button("Generate Report 3"):
            search_ids = [x.strip() for x in case_input.replace(',', ' ').split()]
            found = df1[df1['Case ID'].isin(search_ids)]
            st.dataframe(found)

elif app_mode == "Call Log & Ticket (R4-R6)":
    # Report 4 Logic
    if df2 is not None:
        st.subheader("Report 4: Green Light Issue")
        r4 = df2[(df2['Call Type'] == "Green Light Issue ( Plan Upgrade FRSLA)") & 
                 (df2['Green Light Issue ( Plan Upsell FRSLA)'].str.lower() == "yes")]
        st.table(r4[['Timestamp', 'Agent ID (Eg - 1246)', 'Customer ID', 'POI Number']])

    # Report 5 & 6 Logic
    if df3 is not None:
        st.markdown("---")
        # Report 5: Connection Issues
        r5 = df3[(df3['Status'].str.lower() != 'cancelled') & 
                 (df3['Ticket Problem'] == "No Internet Connection") & 
                 (df3['Queue'] == "CS-SbS (Inbound)")]
        
        st.markdown(f"""
        <div class="report5-card">
            <p class="count-num">{len(r5)}</p>
            <p style="font-weight:bold;">TOTAL CONNECTION ISSUES (R5)</p>
        </div>
        """, unsafe_allow_html=True)

        # Report 6: Installation Type Change
        st.subheader("Report 6: Installation Type Change Details")
        r6 = df3[df3['Root Cause'] == "Installation Type Change"]
        st.dataframe(r6[['Ticket No', 'Status', 'Customer ID', 'Queue']] if not r6.empty else "Data မရှိပါ။")
