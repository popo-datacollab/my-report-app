import streamlit as st
import pandas as pd
from io import BytesIO

# --- Page Setup ---
st.set_page_config(page_title="Pause Time Dashboard", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
    .report-header { color: #1a73e8; font-size: 26px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .setup-section { background: #e8f0fe; padding: 15px; border-radius: 8px; border: 1px solid #1a73e8; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 1. Agent Map (HTML Code ထဲက အတိုင်း) ---
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

# --- 2. Pause Time Analysis Logic ---
if choice == "Pause Time Analysis":
    st.markdown('<div class="report-header">Agent Pause Time Report</div>', unsafe_allow_html=True)
    
    # Update Agent List Section
    with st.expander("➕ Agent List အသစ်ထည့်ရန်"):
        new_agents_input = st.text_area("ID Name ပုံစံဖြင့်ထည့်ပါ", height=100, placeholder="313786 Kyaw Kyaw")
        if st.button("Update List"):
            lines = [l.strip() for l in new_agents_input.split('\n') if l.strip()]
            for line in lines:
                parts = line.split(None, 1)
                if len(parts) >= 2:
                    st.session_state.agent_map[str(parts[0]).strip()] = parts[1].strip()
            st.success("Updated!")

    f_pause = st.file_uploader("Upload Agent CSV (Excel ဖတ်မရပါက CSV ပြောင်းတင်ပါ)", type=["csv", "xlsx"])

    if f_pause:
        try:
            # File Loading
            df = pd.read_csv(f_pause, encoding='latin-1') if f_pause.name.endswith('.csv') else pd.read_excel(f_pause)
            df.columns = df.columns.str.strip()

            # ID Column နှင့် Pause Time Column ကို ရှာခြင်း
            id_col = next((c for c in df.columns if 'Agent' in c), None)
            pause_col = next((c for c in df.columns if 'Pause' in c), None)

            if id_col and pause_col:
                # CRITICAL FIX: ID တွေကို String ပြောင်းပြီး ပိုလျှံနေတဲ့ Space တွေဖြတ်ကာ Map လုပ်ခြင်း
                df[id_col] = df[id_col].astype(str).str.replace('.0', '', regex=False).str.strip()
                df['Agent Name'] = df[id_col].map(st.session_state.agent_map).fillna("Unknown Agent")
                
                # Sorting & Splitting (HTML Logic အတိုင်း)
                df[pause_col] = df[pause_col].fillna("00:00:00")
                has_p = df[df[pause_col] != "00:00:00"].sort_values(by=pause_col, ascending=False)
                no_p = df[df[pause_col] == "00:00:00"]

                # ဇယားနှစ်ခုယှဉ်ပြခြင်း (image_79e25f အတိုင်း)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("### Pause Time ရှိသူများ")
                    st.dataframe(has_p[['Agent Name', pause_col]].style.applymap(lambda x: "color: #d93025; font-weight: bold;", subset=[pause_col]), use_container_width=True, hide_index=True)
                with c2:
                    st.markdown("### Pause Time မရှိသူများ")
                    st.dataframe(no_p[['Agent Name', pause_col]].style.applymap(lambda x: "color: #d93025;", subset=[pause_col]), use_container_width=True, hide_index=True)
            else:
                st.error("Column နာမည်များ (Agent ID/Pause Time) မတွေ့ပါ။")
        except Exception as e:
            st.error(f"Error: {e}")
