import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Dashboard Configuration
st.set_page_config(page_title="Agent Performance Dashboard", layout="wide")

# 2. Agent ID & Name Mapping
AGENT_MAP = {
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
    "311951": "Htet Htun-3", "311952": "Thiri Yadanar-2", "312184": "Kay Zin Thet",
    "312208": "Yati Phone Myat", "312270": "Kyaw Min Khant-8", "312271": "Nway Htwe Aung",
    "312272": "Synmi Mi Aung", "312273": "Kay Kay", "312274": "Nyo Mya Htet",
    "312275": "Ye Min Myat-4", "312377": "Thiha Aung-17", "312378": "Pyae Pyae Zaw",
    "312387": "Zar Ni Phyo", "312388": "Cangmah Ramthang", "312389": "Lin Khaine Kyaw",
    "312400": "Naing Aung Moe-2", "312485": "Htet Aung-11", "312486": "Si Thu Htun-7",
    "312558": "Sandar Win-5", "312559": "Hein Htet Myat", "312560": "Myo Theint Theint Ei",
    "312572": "Pyae Sone Thar", "312573": "Thida Khaing-3", "312579": "Shine Nyi Nyi-2",
    "312597": "Antt Thaw Zin", "312651": "Thiri Moe", "312652": "Han Zar Zar Maw",
    "312734": "Nyan Sin Htet", "312735": "Theint May Thu", "310080": "Htet Wai Phyo",
    "312892": "May Moe", "312900": "Saw Nandar Hlaing", "313015": "Myint Moe Aung",
    "313059": "Si Thu Aung-20", "313061": "May Myint Mo", "313143": "Saw Htet Lin",
    "313264": "Thu Zar Htet-2", "313318": "Oakkar Oo", "313078": "Nyan Lin Htet-10",
    "313360": "Oakkar Oo-2", "313407": "Lu Maw Hein", "313463": "Ei Thet Mon-2",
    "313464": "Ei Thazin Phyu", "313519": "Htun Zar Ni Kyaw", "313581": "Kyaw Moe Aung-2",
    "313602": "Thet Lone Pone-2", "313603": "May Thu Htun-5", "313604": "Thet Hmue Khin",
    "313646": "Htoo Peti Lwin", "313647": "Hla Moe", "313648": "Phyoe Zin Oo",
    "313649": "Nwe Ni Soe", "313655": "Aung Sip Paing", "313670": "Thin Pwint San",
    "313674": "Lai Hnin Hlaing", "313675": "Htay Htay Aung-2", "313676": "Htun Ka Htaty",
    "313677": "Thin Thi Han", "313784": "Min Khant Kyaw-22", "313785": "Kaung Satt"
}

# 3. Password Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Agent Dashboard Login")
    pwd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pwd == "12345":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Incorrect Password!")
else:
    # 4. Main Dashboard
    st.title("📊 Agent Pause Time Summary")
    
    file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if file:
        df = pd.read_csv(file)
        
        # ID to Name Mapping
        if 'Agent ID' in df.columns:
            df['Agent Name'] = df['Agent ID'].astype(str).map(AGENT_MAP).fillna("Unknown ID")
        
        # Select Target Columns
        display_cols = []
        if 'Agent Name' in df.columns: display_cols.append('Agent Name')
        if 'Pause Time' in df.columns: display_cols.append('Pause Time')
        
        final_df = df[display_cols]

        # 5. Data Visualization
        if 'Pause Time' in final_df.columns:
            st.subheader("Performance Chart")
            fig = px.bar(final_df, x='Agent Name', y='Pause Time', 
                         color='Agent Name', text_auto=True,
                         template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary Metrics
            total_time = final_df['Pause Time'].sum()
            st.info(f"Total Combined Pause Time: **{total_time}** Minutes")

        st.divider()
        
        # 6. Data Table
        st.subheader("📋 Detailed Summary Table")
        st.dataframe(final_df, use_container_width=True)
    else:
        st.warning("Please upload a CSV file to generate the report.")
