import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# --- Custom Styling (HTML ထဲက CSS နဲ့ တူအောင်) ---
st.markdown("""
    <style>
    .grand-total { background-color: #d35400 !important; color: white; font-weight: bold; text-align: center; }
    .billing-group { background-color: #2e7d32 !important; color: white; font-weight: bold; text-align: center; }
    .tvie-col { background-color: #8e44ad !important; color: white; font-weight: bold; text-align: center; }
    .report-header { color: #1a73e8; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 30px; font-size: 24px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- Parameters (HTML ထဲကအတိုင်း) ---
group1List = ["AEY", "BGY", "BNY", "INY", "KGY", "KTY", "LAY", "LWY", "MEY", "MTY", "SGY", "SRY", "TEY", "TNY"]
group2List = ["ANM", "CIM", "MYM", "NPW", "DIN", "PIN"]
allowedTypes = ["Installation", "TVie (New)"]
allowedChannels = ["CS", "Website (Kobo)", "Social Media", "Facebook", "Loan Sale", "TikTok"]

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("Reports", ["Pre-Order (R1-R3)", "Call Log & Tickets (R4-R6)"])

# --- Main Logic ---
if choice == "Pre-Order (R1-R3)":
    st.markdown('<div class="report-header">Pre-Order Report Analysis</div>', unsafe_allow_html=True)
    
    f1 = st.file_uploader("Upload File 1: Pre-Order Report", type=["csv", "xlsx"])

    if f1:
        df = pd.read_csv(f1, encoding='latin-1') if f1.name.endswith('.csv') else pd.read_excel(f1)
        df.columns = df.columns.str.strip()

        # Data Filtering (HTML Logic အတိုင်း)
        mask = (
            df['Preorder type'].fillna('').str.strip().isin(allowedTypes) & 
            df['Channel'].fillna('').str.strip().isin(allowedChannels) & 
            (df['Service Type'].fillna('').str.strip() != "Bridge Fiber")
        )
        filtered_df = df[mask].copy()

        # --- Report 1 Logic ---
        st.markdown('<div class="report-header">Report 1: Service City & Billing Group</div>', unsafe_allow_html=True)
        
        def get_city_group(city):
            city = str(city).strip()
            return city if city in ["Yangon", "Mandalay"] else "Other"

        filtered_df['City_Group'] = filtered_df['Service City'].apply(get_city_group)
        filtered_df['Price_Num'] = pd.to_numeric(filtered_df['Price'], errors='coerce').fillna(0)
        
        # Counting
        y_under = len(filtered_df[(filtered_df['City_Group'] == "Yangon") & (filtered_df['Price_Num'] < 30000)])
        y_over = len(filtered_df[(filtered_df['City_Group'] == "Yangon") & (filtered_df['Price_Num'] >= 30000)])
        m_under = len(filtered_df[(filtered_df['City_Group'] == "Mandalay") & (filtered_df['Price_Num'] < 30000)])
        m_over = len(filtered_df[(filtered_df['City_Group'] == "Mandalay") & (filtered_df['Price_Num'] >= 30000)])
        o_under = len(filtered_df[(filtered_df['City_Group'] == "Other") & (filtered_df['Price_Num'] < 30000)])
        o_over = len(filtered_df[(filtered_df['City_Group'] == "Other") & (filtered_df['Price_Num'] >= 30000)])
        
        b1 = len(filtered_df[filtered_df['Billing Group'].fillna('').str.strip().isin(group1List)])
        b2 = len(filtered_df[filtered_df['Billing Group'].fillna('').str.strip().isin(group2List) | 
                             filtered_df['Billing Group'].fillna('').str.contains("PAN", na=False)])

        # Display Report 1 Table
        r1_html = f"""
        <table style="width:100%; border-collapse: collapse; text-align: center; border: 1px solid #ddd;">
            <tr style="background-color: #1a73e8; color: white;">
                <th rowspan="2">Category</th><th rowspan="2" class="grand-total">Grand Total</th>
                <th colspan="2">Yangon</th><th colspan="2">Mandalay</th><th colspan="2">Other</th>
                <th rowspan="2" class="billing-group">List 1</th><th rowspan="2" class="billing-group">List 2/PAN</th>
            </tr>
            <tr style="background-color: #e8f0fe; color: #1a73e8;">
                <td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td><td><30k</td><td>>=30k</td>
            </tr>
            <tr>
                <td>Count</td><td class="grand-total">{len(filtered_df)}</td>
                <td>{y_under}</td><td>{y_over}</td><td>{m_under}</td><td>{m_over}</td><td>{o_under}</td><td>{o_over}</td>
                <td class="billing-group">{b1}</td><td class="billing-group">{b2}</td>
            </tr>
        </table><br>
        """
        st.markdown(r1_html, unsafe_allow_html=True)

        # --- Report 2 Logic ---
        st.markdown('<div class="report-header">Report 2: Service Type Grouping</div>', unsafe_allow_html=True)
        st_counts = {
            "FR-SLA": len(filtered_df[filtered_df['Service Type'] == "FR-SLA"]),
            "Biz Group": len(filtered_df[filtered_df['Service Type'].isin(["MNet Biz", "G2 Biz"])]),
            "Plus Group": len(filtered_df[filtered_df['Service Type'].isin(["G2 Plus", "MNet Plus"])]),
            "Net Group": len(filtered_df[filtered_df['Service Type'].isin(["MNet", "G2 Net"])]),
        }
        st_counts["Other"] = len(filtered_df) - sum(st_counts.values())

        st.table(pd.DataFrame([st_counts], index=["Count"]))

        # --- Report 3: Manual Search ---
        st.markdown('<div class="report-header">Report 3: Manual Case ID Search</div>', unsafe_allow_html=True)
        case_input = st.text_area("Case ID များကို ထည့်ပါ (comma ခြား၍)", placeholder="POI-26-03-XXXX...")
        if st.button("Generate Report 3"):
            search_ids = [x.strip() for x in case_input.replace('\n', ',').split(',') if x.strip()]
            res_df = df[df['Case ID'].fillna('').str.strip().isin(search_ids)]
            st.dataframe(res_df)

else:
    st.markdown('<div class="report-header">Call Log & Ticket Analysis</div>', unsafe_allow_html=True)
    f2 = st.file_uploader("Upload File 2: IVR Call Log (R4)", type=["csv"])
    f3 = st.file_uploader("Upload File 3: Ticket Report (R5-R6)", type=["csv"])

    if f2:
        st.subheader("Report 4: Green Light Issue")
        df2 = pd.read_csv(f2, encoding='latin-1')
        r4_res = df2[(df2['Call Type'].str.contains('Green Light', na=False)) & 
                     (df2['Green Light Issue ( Plan Upsell FRSLA)'].str.lower() == 'yes')]
        st.dataframe(r4_res)

    if f3:
        df3 = pd.read_csv(f3, encoding='latin-1')
        
        # Report 5 Card
        r5_count = len(df3[(df3['Status'].str.lower() != 'cancelled') & 
                           (df3['Ticket Problem'] == 'No Internet Connection') & 
                           (df3['Queue'] == 'CS-SbS (Inbound)')])
        
        st.markdown(f"""
            <div style="background: white; border-left: 10px solid #1a73e8; padding: 20px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #1a73e8; font-size: 50px;">{r5_count}</h1>
                <p><b>Report 5: TOTAL CONNECTION ISSUES</b></p>
            </div>
        """, unsafe_allow_html=True)

        # Report 6
        st.subheader("Report 6: Installation Type Change Details")
        r6_df = df3[df3['Root Cause'] == "Installation Type Change"]
        st.dataframe(r6_df[['Ticket ID', 'Status', 'Customer ID', 'Queue']] if not r6_df.empty else "Data မရှိပါ။")
