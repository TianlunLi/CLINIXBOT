# app.py

import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from components.chat_interface import ChatInterface
from components.visualization_dashboard import VisualizationDashboard
from components.pharmacy_finder import PharmacyFinder
from components.hospital_finder import HospitalFinder
from utils.data_processor import DataProcessor
from models.rag_model import MedicalRAGModel
from utils.language_utils import LanguageUtils

# 加载环境变量
load_dotenv()

# 配置页面
st.set_page_config(
    page_title="ClinixBot - Intelligent Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles (keep your existing CSS)
st.markdown("""
<style>
    /* 主色调：蓝白配色方案 */
    :root {
        --primary-color: #4B89DC;
        --secondary-color: #EBF5FF;
        --text-color: #333333;
        --light-text: #6B7C93;
    }
    
    /* 全局样式 */
    .main {
        background-color: white;
        color: var(--text-color);
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 700;
    }
    
    /* 部件样式 */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #3A70C3;
    }
    
    /* 聊天容器 */
    .chat-container {
        background-color: var(--secondary-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* 卡片样式 */
    .css-1r6slb0 {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(75, 137, 220, 0.1);
    }
    
    /* 边栏样式 */
    .css-1d391kg {
        background-color: var(--secondary-color);
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_diagnosis' not in st.session_state:
    st.session_state.current_diagnosis = None

if 'recommended_medications' not in st.session_state:
    st.session_state.recommended_medications = []

if 'active_view' not in st.session_state:
    st.session_state.active_view = "chat"

# 初始化语言设置 (默认为英文)
if 'language' not in st.session_state:
    st.session_state.language = "en"

# 语言切换回调函数
def change_language():
    if st.session_state.language_selector == "English":
        st.session_state.language = "en"
    else:
        st.session_state.language = "zh"

# 创建顶部栏，添加语言选择器
top_col1, top_col2 = st.columns([6, 1])
with top_col2:
    selected_language = st.selectbox(
        label=LanguageUtils.get_text("general", "language_selector", st.session_state.language),
        options=["English", "中文"],
        index=0 if st.session_state.language == "en" else 1,
        key="language_selector",
        on_change=change_language
    )

# 加载模型和数据
@st.cache_resource
def load_rag_model():
    return MedicalRAGModel()

@st.cache_data
def load_medical_data():
    data = pd.read_csv("data/hospital_records_2021_2024_with_bills.csv")
    processor = DataProcessor()
    return processor.preprocess_data(data)

# 加载数据和模型
rag_model = load_rag_model()
medical_data = load_medical_data()

# 应用标题
with top_col1:
    st.title(LanguageUtils.get_text("general", "title", st.session_state.language))
    st.subheader(LanguageUtils.get_text("general", "subtitle", st.session_state.language))

# 侧边栏菜单
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=ClinixBot", width=150)
    st.title(LanguageUtils.get_text("general", "nav_menu", st.session_state.language))
    
    # 导航菜单
    selected_view = st.radio(
        ":",
        [
            LanguageUtils.get_text("general", "chat_option", st.session_state.language),
            LanguageUtils.get_text("general", "data_option", st.session_state.language),
            LanguageUtils.get_text("general", "pharmacy_option", st.session_state.language),
            LanguageUtils.get_text("general", "hospital_option", st.session_state.language)
        ]
    )
    
    if selected_view == LanguageUtils.get_text("general", "chat_option", st.session_state.language):
        st.session_state.active_view = "chat"
    elif selected_view == LanguageUtils.get_text("general", "data_option", st.session_state.language):
        st.session_state.active_view = "data"
    elif selected_view == LanguageUtils.get_text("general", "pharmacy_option", st.session_state.language):
        st.session_state.active_view = "pharmacy"
    elif selected_view == LanguageUtils.get_text("general", "hospital_option", st.session_state.language):
        st.session_state.active_view = "hospital"
    
    st.divider()
    st.caption(LanguageUtils.get_text("general", "copyright", st.session_state.language))

# 主内容区域
if st.session_state.active_view == "chat":
    chat_interface = ChatInterface(rag_model, st.session_state.language)
    chat_interface.render()
    
elif st.session_state.active_view == "data":
    visualization_dashboard = VisualizationDashboard(medical_data, st.session_state.language)
    visualization_dashboard.render()
    
elif st.session_state.active_view == "pharmacy":
    pharmacy_finder = PharmacyFinder(st.session_state.language)
    pharmacy_finder.render()
    
elif st.session_state.active_view == "hospital":
    hospital_finder = HospitalFinder(st.session_state.language)
    hospital_finder.render()

# 添加页脚
st.markdown("---")
st.caption(LanguageUtils.get_text("general", "disclaimer", st.session_state.language))