import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Po Po Data Dashboard", layout="wide")

# --- Agent Database (လူကြီးမင်းပေးထားသော List) ---
if 'agent_map' not in st.session_state:
    st.session_state.agent_map = {
        "301246": "Thae Su Myat Noe", "304558": "Phyo Ko Ko", "305527": "Aye Myat Mon-4",
        "306432": "Ei Pwint Phyu-2", "306564": "Thin Thin Nwe-3", "307381": "Ye Myat Thu",
        "307832": "Hnin Aye Soe", "308059": "Nyo Nyo Tun Lwin", "308086": "Lin Htet Paing",
        "308489": "Tin Zar Thaw", "308863": "Zun Pwint Phyu", "308915": "San San Aye",
        "308924": "Yoon Waddy", "309197": "Than Than Sint", "309299": "Toe Hlaing Win-2",
        "309535": "Myint Myat Thu-2", "309607": "Hnin Oo Wai-3", "309609": "Shun La Pyae",
        "309700": "Kay Zin Htwe", "306099": "Htet Aung Khant", "306098": "Hsu Po Po Aung",
        "306023": "Zin Me Me Htun", "306956": "Win Win Aye-2", "310387": "Kyawt Shwe Yee Win",
        "310478": "Chit Su San", "310557": "Aung Si Phyo", "310822": "Hein Htet Aung-46",
        "310917": "Zon Thaw Tar Htet", "310968": "Wai Yan Htet-10", "310963": "Mya Sint Chal",
        "310965": "Hnin Wutt Yee-2", "311013": "Lin Htein", "311159": "Aye Nyein Nyein Moe",
        "311464": "Eingyin Khaing-2", "311465": "Hnin Nadi Nway", "311493": "Yu Thandi Moe",
        "311569": "Nay Chi Win Lae", "311691": "Hay Mar Hnin Oo", "303220": "Tin Myo Swe Zin Tun",
        "311951": "Htet Htet Htun-3", "311952": "Thiri Yadanar-2", "312184": "Kay Zin Thet",
        "312208": "Yati Phone Myat", "312270": "Kyaw Min Khant-8", "312271": "Nway Htwe Aung",
        "312272": "Synmi Mi Aung", "312273": "Kay Kay", "312274": "Nyo Mya Htet",
        "312275": "Ye Min Myat-4", "312377": "Thiha Aung-17", "312378": "Pyae Pyae Zaw",
        "312387": "Zar Ni Phyo", "312388": "Cangmah Ramthang", "312389": "Lin Khaine Kyaw",
        "312400": "Naing Aung Moe-2", "312485": "Htet Htet Aung-11", "312486": "Si Thu Htun-7",
        "312558": "Sandar Win-5", "312559": "Hein Htet Myat", "312560": "Myo Theint Theint Ei",
        "312572": "Pyae Sone Thar", "312573": "Thida Khaing-3", "312579": "Shine Nyi Nyi-2",
        "312597": "Antt Thaw Zin", "312651": "Thiri Moe", "312652": "Han Zar Zar Maw",
        "312734": "Nyan Sin Htet", "312735": "Theint May Thu", "310080": "Htet Wai Phyo",
        "312892": "May Moe", "312899": "Sai Wai Yan Htun", "312900": "Saw Nandar Hlaing",
        "313015": "Myint Moe Aung", "313059": "Si Thu Aung-20", "313061": "May Myint Mo",
        "313143": "Saw Htet Lin", "313264": "Thu Zar Htet-2", "313318": "Oakkar Oo",
        "313078": "Nyan Lin Htet-10", "313360": "Oakkar Oo-2", "313407": "Lu Maw Hein",
        "313463": "Ei Thet Mon-2", "313464": "Ei Thazin Phyu", "313519": "Htun Zar Ni Kyaw",
        "313581": "Kyaw Moe Aung-2", "313602": "Thet Lone Pone-2", "313603": "May Thu Htun-5",
        "313604": "Thet Hmue Khin", "313646": "Htoo Peti Lwin", "313647": "Hla Moe",
        "313648": "Phyoe Zin Oo", "313649": "Nwe Ni Soe", "313655": "Aung Sip Paing",
        "313670": "Thin Pwint San", "313674": "Lai Hnin Hlaing", "313675": "Htay Htay Aung-2",
        "313676": "Htun Ka Htaty", "313677": "Thin Thi Han", "313784": "Min Khant Kyaw-22",
        "313785": "Kaung Satt"
    }

def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", ["Home", "Pre-Order (R1-R3)", "Agent Pause Analysis (R4)"])

# --- Home Page ---
if choice == "Home":
    st.title("🏠 Welcome")
    st.write("App is running successfully!")
    st.info("ဘယ်ဘက် Menu ကနေ စစ်ဆေးလိုတဲ့ Report အမျိုးအစားကို ရွေးချယ်ပေးပါ။")

# --- Pre-Order Report (R1-R3) ---
elif choice == "Pre-Order (R1-R3)":
    st.title("📁 Pre-Order Report Analysis")
    
    # ၁။ File Upload Section
    col1, col2 = st.columns(2)
    with col1:
        preorder_file = st.file_uploader("Pre-Order Report File ကို တင်ပါ", type=["xlsx", "csv", "xls"])
    
    if preorder_file:
        try:
            # File Type စစ်ဆေးပြီး ဖတ်ခြင်း
            if preorder_file.name.endswith('.csv'):
                df = pd.read_csv(preorder_file, encoding='latin-1')
            else:
                df = pd.read_excel(preorder_file)
            
            st.success(f"File '{preorder_file.name}' ကို ဖတ်လို့ရပါပြီ။")
            
            # ၂။ Report Generation Logic (ဥပမာ Report 3: Manual Case ID Search)
            st.divider()
            st.subheader("Report 3: Manual Case ID Search")
            case_ids_input = st.text_area("Case ID များကို ထည့်ပါ (တစ်ကြောင်းချင်းစီ သို့မဟုတ် comma ခြား၍)", placeholder="POI-26-03-XXXX...")
            
            if st.button("Generate Report 3"):
                if case_ids_input:
                    # Input များကို သန့်စင်ခြင်း
                    search_list = [x.strip() for x in case_ids_input.replace('\n', ',').split(',') if x.strip()]
                    # Column ရှာခြင်း (ဥပမာ Case ID column name)
                    case_col = [col for col in df.columns if 'case' in col.lower() or 'id' in col.lower()]
                    
                    if case_col:
                        result = df[df[case_col[0]].astype(str).isin(search_list)]
                        st.write(f"ရှာဖွေတွေ့ရှိမှု - {len(result)} ခု")
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.warning("Case ID column ကို ရှာမတွေ့ပါ။")
                else:
                    st.error("Case ID တစ်ခုခု အရင်ထည့်ပေးပါ။")
            
            # (အခြား Report 1, 2 logic များကိုလည်း ဤနေရာတွင် ထပ်ဖြည့်နိုင်ပါသည်)
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("စတင်ရန်အတွက် အပေါ်က 'Browse files' ကနေ Excel/CSV file တစ်ခု အရင်တင်ပေးပါ။")

# --- Agent Pause Analysis (R4) ---
elif choice == "Agent Pause Analysis (R4)":
    st.title("⏱️ Agent Pause Time Analysis")
    agent_file = st.file_uploader("Agent CSV File ကို တင်ပါ", type=["csv"], key="r4_file")
    
    if agent_file:
        df = pd.read_csv(agent_file, encoding='latin-1')
        df.columns = df.columns.str.strip()
        
        if 'Agent' in df.columns and 'Pause Time' in df.columns:
            # ID သန့်စင်ခြင်း (Agent/313820 -> 313820)
            df['Agent'] = df['Agent'].astype(str).str.replace('Agent/', '', regex=False).str.strip()
            
            # Numeric ပြောင်းခြင်း
            df['Pause Time'] = pd.to_numeric(df['Pause Time'], errors='coerce').fillna(0)
            
            summary = df.groupby('Agent')['Pause Time'].sum().reset_index()
            summary['Agent Name'] = summary['Agent'].map(st.session_state.agent_map).fillna("Unknown Agent")
            summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
            
            st.subheader("Summary Table")
            st.dataframe(summary[['Agent', 'Agent Name', 'Formatted Time']].sort_values(by='Agent'), use_container_width=True, hide_index=True)
            st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
        else:
            st.error("လိုအပ်သော Column များ မတွေ့ပါ။")
