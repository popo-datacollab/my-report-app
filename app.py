import streamlit as st
import pandas as pd
from io import BytesIO

# --- Page Setup ---
st.set_page_config(page_title="Pause Time Dashboard", layout="wide")

# --- CSS for Image-like Table Styling ---
st.markdown("""
    <style>
    .report-header { color: #1a73e8; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .pause-red { color: #d93025; font-weight: bold; }
    .zero-pause { color: #d93025; }
    </style>
""", unsafe_allow_html=True)

# --- Agent Map Data ---
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

# --- Sidebar ---
with st.sidebar:
    st.title("📌 Main Menu")
    choice = st.radio("Reports", ["Pre-Order (R1-R3)", "Pause Time Analysis"])

# --- Pause Time Analysis ---
if choice == "Pause Time Analysis":
    st.markdown('<div class="report-header">Agent Pause Time Report</div>', unsafe_allow_html=True)
    
    f_pause = st.file_uploader("Upload Agent CSV/Excel", type=["csv", "xlsx"])

    if f_pause:
        # File Loading
        if f_pause.name.endswith('.csv'):
            df = pd.read_csv(f_pause, encoding='latin-1')
        else:
            df = pd.read_excel(f_pause)

        # Basic Cleanup
        df.columns = df.columns.str.strip()
        id_col = next((c for c in df.columns if 'Agent' in c), None)
        pause_col = 'Pause Time'

        if id_col and pause_col in df.columns:
            # Mapping Names
            df['Agent Name'] = df[id_col].astype(str).str.strip().map(st.session_state.agent_map).fillna("Unknown Agent")
            
            # Data Formatting
            df[pause_col] = df[pause_col].fillna("00:00:00")
            
            # ခွဲခြားခြင်း (Pause Time ရှိသူ နှင့် မရှိသူ)
            has_pause = df[df[pause_col] != "00:00:00"].sort_values(by=pause_col, ascending=False)
            no_pause = df[df[pause_col] == "00:00:00"]

            # Displaying in Two Columns like image_79799f
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Pause Time ရှိသူများ")
                # Table with red text for time
                st.dataframe(
                    has_pause[['Agent Name', pause_col]].style.map(lambda x: "color: #d93025; font-weight: bold;", subset=[pause_col]),
                    use_container_width=True, hide_index=True
                )

            with col2:
                st.markdown("### Pause Time မရှိသူများ")
                # Table with red text for 00:00:00
                st.dataframe(
                    no_pause[['Agent Name', pause_col]].style.map(lambda x: "color: #d93025;", subset=[pause_col]),
                    use_container_width=True, hide_index=True
                )
        else:
            st.error("လိုအပ်သော Column များ မတွေ့ပါ။")
