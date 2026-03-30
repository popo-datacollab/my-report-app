import streamlit as st
import pandas as pd
import io

# 1. Page Config & CSS Styling
st.set_page_config(page_title="Data Analysis System", layout="wide")

st.markdown("""
<style>
    .report-table { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 30px; font-size: 14px; }
    .report-table th, .report-table td { border: 1px solid #dee2e6; padding: 12px 5px; }
    .header-blue { background-color: #1a73e8 !important; color: white !important; }
    .grand-total-col { background-color: #d35400 !important; color: white !important; font-weight: bold; }
    .billing-group-col { background-color: #2e7d32 !important; color: white !important; font-weight: bold; }
    .sub-header { background-color: #e8f0fe; color: #1a73e8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. Password Access Control (Password: admin123)
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔒 Security Access")
    pwd = st.text_input("Please enter password to unlock", type="password")
    if st.button("Unlock App"):
        if pwd == "admin123":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Password မှားယွင်းနေပါသည်။")
    st.stop()

# 3. Sidebar Menu
with st.sidebar:
    st.title("📌 Main Menu")
    app_mode = st.radio("Reports Selection", ["Pre-Order (R1-R3)", "Call Log & Ticket (R4-R6)"])
    st.markdown("---")
    if st.button("Log Out"):
        st.session_state["password_correct"] = False
        st.rerun()

# 4. Data Loading Function
def load_data(file):
    if file is None: return None
    try:
        content = file.read()
        for enc in ['utf-8-sig', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(io.BytesIO(content), encoding=enc)
                df.columns = df.columns.str.strip() # Column ရှေ့နောက် space များဖြတ်ခြင်း
                return df
            except: continue
        return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# 5. File Uploaders
st.title("📊 Comprehensive Data Analysis Report")
c1, c2, c3 = st.columns(3)
with c1: f1 = st.file_uploader("File 1: Pre-Order Report", type=["csv"])
with c2: f2 = st.file_uploader("File 2: IVR Call Log", type=["csv"])
with c3: f3 = st.file_uploader("File 3: Ticket Report", type=["csv"])

df1 = load_data(f1)

if app_mode == "Pre-Order (R1-R3)":
    if df1 is not None:
        # Data Filtering Logic
        allowed_types = ["Installation", "TVie (New)"]
        allowed_channels = ["CS", "Website (Kobo)", "Social Media", "Facebook", "Loan Sale", "TikTok"]
        
        f_df = df1[(df1['Preorder type'].isin(allowed_types)) & 
                  (df1['Channel'].isin(allowed_channels)) & 
                  (df1['Service Type'] != "Bridge Fiber")].copy()

        # --- REPORT 1: City & Billing Group ---
        ygn = f_df[f_df['Service City'] == "Yangon"]
        mdy = f_df[f_df['Service City'] == "Mandalay"]
        other = f_df[~f_df['Service City'].isin(["Yangon", "Mandalay"])]

        def get_counts(df):
            p = pd.to_numeric(df['Price'], errors='coerce')
            return df[p < 30000].shape[0], df[p >= 30000].shape[0]

        y_u, y_o = get_counts(ygn); m_u, m_o = get_counts(mdy); o_u, o_o = get_counts(other)
        
        g1_list = ["AEY", "BGY", "BNY", "INY", "KGY", "KTY", "LAY", "LWY", "MEY", "MTY", "SGY", "SRY", "TEY", "TNY"]
        g2_list = ["ANM", "CIM", "MYM", "NPW", "DIN", "PIN"]
        b1 = f_df[f_df['Billing Group'].isin(g1_list)].shape[0]
        b2 = f_df[f_df['Billing Group'].isin(g2_list) | f_df['Billing Group'].str.contains("PAN", na=False)].shape[0]

        st.markdown(f"""
        <h3 style='text-align: center; color: #1a73e8;'>Report 1: Service City & Billing Group</h3>
        <table class="report-table">
            <tr class="header-blue">
                <th rowspan="2">Category</th><th rowspan="2" class="grand-total-col">Grand Total</th>
                <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
                <th class="billing-group-col">List 1</th><th class="billing-group-col">List 2/PAN</th>
            </tr>
            <tr class="sub-header">
                <td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td>
                <td>Count</td><td>Count</td>
            </tr>
            <tr>
                <td>Count</td><td class="grand-total-col">{len(f_df)}</td>
                <td>{y_u}</td><td>{y_o}</td><td>{m_u}</td><td>{m_o}</td><td>{o_u}</td><td>{o_o}</td>
                <td class="billing-group-col">{b1}</td><td class="billing-group-col">{b2}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

        # --- REPORT 2: Service Type Grouping ---
        st_fr = f_df[f_df['Service Type'] == "FR-SLA"].shape[0]
        st_biz = f_df[f_df['Service Type'].isin(["MNet Biz", "G2 Biz"])].shape[0]
        st_plus = f_df[f_df['Service Type'].isin(["G2 Plus", "MNet Plus"])].shape[0]
        st_net = f_df[f_df['Service Type'].isin(["MNet", "G2 Net"])].shape[0]
        st_other = len(f_df) - (st_fr + st_biz + st_plus + st_net)

        st.markdown(f"""
        <h3 style='text-align: center; color: #1a73e8;'>Report 2: Service Type Grouping</h3>
        <table class="report-table">
            <tr class="header-blue">
                <th>Category</th><th class="grand-total-col">Grand Total</th>
                <th>FR-SLA</th><th>Biz Group</th><th>Plus Group</th><th>Net Group</th><th>Other</th>
            </tr>
            <tr>
                <td>Count</td><td class="grand-total-col">{len(f_df)}</td>
                <td>{st_fr}</td><td>{st_biz}</td><td>{st_plus}</td><td>{st_net}</td><td>{st_other}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

    else:
        st.info("File 1 (Pre-Order Report) ကို Upload အရင်တင်ပေးပါခင်ဗျာ။")
