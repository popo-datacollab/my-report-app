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

# --- Helper Functions ---
def convert_to_hms(total_minutes):
    if pd.isna(total_minutes): return "00:00:00"
    total_seconds = int(total_minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# --- Sidebar Menu ---
with st.sidebar:
    st.title("📌 Main Menu")
    MENU_HOME = "Home"
    MENU_R1 = "Pre-Order (R1-R3)"
    MENU_R4 = "Agent Pause Analysis (R4)"
    choice = st.radio("သွားလိုသည့် Report ကို ရွေးပါ -", [MENU_HOME, MENU_R1, MENU_R4])
    st.divider()
    st.info("Po Po Data Dashboard v2.5")

# --- Home Page ---
if choice == MENU_HOME:
    st.title("🏠 Po Po Data Dashboard")
    st.write("Welcome! အလိုအလျောက် Data Analysis ပြုလုပ်ပေးသော Dashboard ဖြစ်ပါသည်။")
    
    # Dashboard ကိန်းဂဏန်းများ
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", "Active")
    c2.metric("Total Agents", len(st.session_state.agent_map))
    c3.metric("Project", "POI 2026")

# --- Agent Pause Analysis (R4) - Integrated with your Logic ---
elif choice == MENU_R4:
    st.title("⏱️ Agent Pause Time Analysis")

    # ၁။ Agent List Update Section
    with st.expander("➕ Agent List အသစ်များကို ဤနေရာတွင် ထည့်ပါ"):
        st.write("ပုံစံ- ID [Space] Name (ဥပမာ- 313786 Kyaw Kyaw)")
        new_agents_input = st.text_area("Update Agent List", placeholder="313786 Kyaw Kyaw\n313787 Ma Ma", height=100)
        if st.button("Update Agent Database"):
            added_count = 0
            for line in new_agents_input.split('\n'):
                parts = line.strip().split()
                if len(parts) >= 2:
                    st.session_state.agent_map[parts[0]] = " ".join(parts[1:])
                    added_count += 1
            st.success(f"{added_count} agents updated successfully!")

    # ၂။ File Upload
    agent_file = st.file_uploader("Agent CSV File ကို တင်ပါ", type=["csv"], key="agent_r4_upload")
    
    if agent_file:
        try:
            df = pd.read_csv(agent_file, encoding='latin-1')
            
            # Column ရှာဖွေခြင်း (Agent ID သို့မဟုတ် Agent Name)
            # လူကြီးမင်း CSV ထဲမှာ 'Agent' လို့ပါတာ သေချာအောင် စစ်ပေးထားပါတယ်
            col_target = 'Agent' if 'Agent' in df.columns else None
            
            if col_target and 'Pause Time' in df.columns:
                # Time to Minutes conversion
                if df['Pause Time'].dtype == 'object':
                    df['Pause Time'] = pd.to_timedelta(df['Pause Time']).dt.total_seconds() / 60
                
                # Group by Agent (ID)
                summary = df.groupby(col_target)['Pause Time'].sum().reset_index()
                
                # Agent ID ကို နာမည်နဲ့တွဲပေးခြင်း
                summary['Agent Name'] = summary[col_target].astype(str).map(st.session_state.agent_map).fillna("Unknown Agent")
                
                # Format to HH:MM:SS
                summary['Formatted Time'] = summary['Pause Time'].apply(convert_to_hms)
                
                # Display Results
                st.subheader("Agent-wise Pause Report")
                
                # Table ပြင်ဆင်ခြင်း
                display_df = summary[[col_target, 'Agent Name', 'Formatted Time']].sort_values(by='Formatted Time', ascending=False)
                
                c1, c2 = st.columns([1.5, 1])
                with c1:
                    st.dataframe(display_df, hide_index=True, use_container_width=True)
                with c2:
                    st.write("**Top Pauses (Minutes)**")
                    st.bar_chart(data=summary, x='Agent Name', y='Pause Time')
            else:
                st.error("CSV ထဲတွင် 'Agent' နှင့် 'Pause Time' Column အမည်များ မတွေ့ရပါ။")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Pre-Order Report (R1-R3) Logic ---
elif choice == MENU_R1:
    st.title("📁 Pre-Order Report (R1, R2, R3)")
    # (လူကြီးမင်းပေးထားသော Pre-Order Logic များ ဤနေရာတွင် ဆက်လက်ရှိနေပါမည်)
    st.info("File upload တင်ပြီး Report 1, 2, 3 များကို စစ်ဆေးနိုင်ပါသည်။")
    # ... (ယခင် code အပိုင်းကို ဒီနေရာမှာ ထည့်ထားပေးပါတယ်)
