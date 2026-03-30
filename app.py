import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Comprehensive Analysis", layout="wide")

# CSS Styling (ဇယားအရောင်များ အမှန်အတိုင်းဖြစ်စေရန်)
st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 30px; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 12px 5px; }
    .header-blue { background-color: #1a73e8 !important; color: white !important; }
    .grand-total-col { background-color: #d35400 !important; color: white !important; font-weight: bold; }
    .billing-group-col { background-color: #2e7d32 !important; color: white !important; font-weight: bold; }
    .sub-header { background-color: #e8f0fe; color: #1a73e8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 1. Error-Free Data Loading Function
def load_data(file):
    if file is None: return None
    try:
        content = file.read()
        for enc in ['utf-8-sig', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(io.BytesIO(content), encoding=enc)
                # Column အမည်များရှိ Space များကို ဖယ်ရှားခြင်း
                df.columns = df.columns.str.strip()
                return df
            except:
                continue
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# 2. Main UI
st.title("📊 Comprehensive Data Analysis (Report 1-6)")

col1, col2, col3 = st.columns(3)
with col1: f1 = st.file_uploader("File 1: Pre-Order Report", type=["csv"])
with col2: f2 = st.file_uploader("File 2: IVR Call Log", type=["csv"])
with col3: f3 = st.file_uploader("File 3: Ticket Report", type=["csv"])

df1 = load_data(f1)

if df1 is not None:
    # --- Data Filtering Logic (HTML အတိုင်း) ---
    allowed_types = ["Installation", "TVie (New)"]
    allowed_channels = ["CS", "Website (Kobo)", "Social Media", "Facebook", "Loan Sale", "TikTok"]
    
    # Filter ပထမအဆင့်
    mask = (df1['Preorder type'].isin(allowed_types)) & \
           (df1['Channel'].isin(allowed_channels)) & \
           (df1['Service Type'] != "Bridge Fiber")
    f_df = df1[mask].copy()

    # --- Report 1 Calculation ---
    # City အလိုက် ခွဲခြားခြင်း
    ygn = f_df[f_df['Service City'] == "Yangon"]
    mdy = f_df[f_df['Service City'] == "Mandalay"]
    other = f_df[~f_df['Service City'].isin(["Yangon", "Mandalay"])]

    # Price အလိုက် ခွဲခြားခြင်း (30,000)
    def get_counts(df):
        under = df[pd.to_numeric(df['Price'], errors='coerce') < 30000].shape[0]
        over = df[pd.to_numeric(df['Price'], errors='coerce') >= 30000].shape[0]
        return under, over

    ygn_u, ygn_o = get_counts(ygn)
    mdy_u, mdy_o = get_counts(mdy)
    oth_u, oth_o = get_counts(other)
    
    gt = len(f_df)

    # Billing Group Logic
    g1_list = ["AEY", "BGY", "BNY", "INY", "KGY", "KTY", "LAY", "LWY", "MEY", "MTY", "SGY", "SRY", "TEY", "TNY"]
    g2_list = ["ANM", "CIM", "MYM", "NPW", "DIN", "PIN"]
    
    b1 = f_df[f_df['Billing Group'].isin(g1_list)].shape[0]
    b2 = f_df[f_df['Billing Group'].isin(g2_list) | f_df['Billing Group'].str.contains("PAN", na=False)].shape[0]

    # Display Report 1
    st.markdown(f"""
    <h2 style='text-align: center; color: #1a73e8;'>Report 1: Service City & Billing Group</h2>
    <table class="report-table">
        <thead>
            <tr class="header-blue">
                <th rowspan="2">Category</th><th rowspan="2" class="grand-total-col">Grand Total</th>
                <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
                <th rowspan="2" class="billing-group-col">List 1</th><th rowspan="2" class="billing-group-col">List 2/PAN</th>
            </tr>
            <tr class="sub-header">
                <td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Count</td><td class="grand-total-col">{gt}</td>
                <td>{ygn_u}</td><td>{ygn_o}</td><td>{mdy_u}</td><td>{mdy_o}</td><td>{oth_u}</td><td>{oth_o}</td>
                <td class="billing-group-col">{b1}</td><td class="billing-group-col">{b2}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # --- Report 2 Logic ---
    st_rep = {
        "FR-SLA": f_df[f_df['Service Type'] == "FR-SLA"].shape[0],
        "Biz Group": f_df[f_df['Service Type'].isin(["MNet Biz", "G2 Biz"])].shape[0],
        "Plus Group": f_df[f_df['Service Type'].isin(["G2 Plus", "MNet Plus"])].shape[0],
        "Net Group": f_df[f_df['Service Type'].isin(["MNet", "G2 Net"])].shape[0]
    }
    st_rep["Other"] = gt - sum(st_rep.values())

    st.markdown(f"""
    <h2 style='text-align: center; color: #1a73e8;'>Report 2: Service Type Grouping</h2>
    <table class="report-table">
        <tr class="header-blue">
            <th>Category</th><th class="grand-total-col">Grand Total</th>
            <th>FR-SLA</th><th>Biz Group</th><th>Plus Group</th><th>Net Group</th><th>Other</th>
        </tr>
        <tr>
            <td>Count</td><td class="grand-total-col">{gt}</td>
            <td>{st_rep['FR-SLA']}</td><td>{st_rep['Biz Group']}</td><td>{st_rep['Plus Group']}</td><td>{st_rep['Net Group']}</td><td>{st_rep['Other']}</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
