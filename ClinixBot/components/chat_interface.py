# components/chat_interface.py
import streamlit as st
import time
import random
import re
from utils.language_utils import LanguageUtils

class ChatInterface:
    def __init__(self, rag_model, language="en"):
        self.rag_model = rag_model
        self.language = language
    
    def _get_avatar(self, is_user):
        """获取头像URL"""
        return "👤" if is_user else "🏥"
    
    def _add_message(self, message, is_user=True):
        """添加消息到聊天历史"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.append({
            "message": message,
            "is_user": is_user,
            "timestamp": time.time()
        })
    
    def _get_initial_greeting(self):
        """获取初始欢迎消息"""
        return LanguageUtils.get_text("chat", "greeting", self.language)
    
    def _detect_language(self, text):
        """检测输入文本的语言"""
        # 简单的中文检测 - 检查是否包含中文字符
        if re.search("[\u4e00-\u9FFF]", text):
            return "zh"
        return "en"
    
    def _handle_user_input(self):
        """处理用户输入"""
        user_input = st.session_state.user_input
        
        if user_input:
            # 添加用户消息
            self._add_message(user_input, is_user=True)
            
            # 清空输入框
            st.session_state.user_input = ""
            
            # 检测输入语言
            input_language = self._detect_language(user_input)
            
            # 获取诊断结果
            with st.spinner(LanguageUtils.get_text("chat", "analyzing", self.language)):
                diagnosis_result = self.rag_model.get_diagnosis(user_input, language=input_language)
            
            # 保存当前诊断
            st.session_state.current_diagnosis = diagnosis_result["diagnosis"]
            
            # 添加机器人回复
            self._add_message(diagnosis_result["diagnosis"], is_user=False)
            
            # 如果有诊断结果，获取药物推荐
            if ("初步诊断" in diagnosis_result["diagnosis"]) or ("Preliminary Diagnosis" in diagnosis_result["diagnosis"]):
                with st.spinner(LanguageUtils.get_text("chat", "generating_recommendations", self.language)):
                    medications = self.rag_model.get_medication_recommendations(diagnosis_result["diagnosis"], language=input_language)
                    st.session_state.recommended_medications = medications
    
    def render(self):
        """渲染聊天界面"""
        # 初始化聊天历史
        if 'chat_history' not in st.session_state or not st.session_state.chat_history:
            self._add_message(self._get_initial_greeting(), is_user=False)
        
        # 聊天容器
        chat_container = st.container()
        
        with chat_container:
            # 显示聊天历史
            for message in st.session_state.chat_history:
                with st.chat_message(name="user" if message["is_user"] else "assistant", avatar=self._get_avatar(message["is_user"])):
                    st.write(message["message"])
        
        # 用户输入
        st.text_input(LanguageUtils.get_text("chat", "symptom_input", self.language), key="user_input", on_change=self._handle_user_input)
        
        # 如果有推荐的药物，显示药物推荐和附近药房按钮
        if 'recommended_medications' in st.session_state and st.session_state.recommended_medications:
            with st.expander(LanguageUtils.get_text("chat", "view_recommendations", self.language), expanded=True):
                st.markdown(st.session_state.recommended_medications)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(LanguageUtils.get_text("chat", "find_pharmacy", self.language)):
                        st.session_state.active_view = "pharmacy"
                        try:
                            st.rerun()  # 新版Streamlit
                        except:
                            try:
                                st.experimental_rerun()  # 旧版Streamlit
                            except:
                                st.error("请手动切换到药房页面")
                with col2:
                    if st.button(LanguageUtils.get_text("chat", "find_hospital", self.language)):
                        st.session_state.active_view = "hospital"
                        try:
                            st.rerun()  # 新版Streamlit
                        except:
                            try:
                                st.experimental_rerun()  # 旧版Streamlit
                            except:
                                st.error("请手动切换到医院页面")