import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
import json
import random

class HospitalFinder:
    def __init__(self):
        self.api_key = "HOSPITAL_API_KEY"  # 需要替换为实际API密钥
        self.hospitals = [
            {"name": "General Hospital", "address": "123 Health St", "distance": 1.2, "lat": 40.7120, "lng": -74.0050, "beds_available": 5, "specialty": "综合医院", "wait_time": "30分钟"},
            {"name": "City Medical Center", "address": "456 Care Ave", "distance": 2.3, "lat": 40.7150, "lng": -74.0080, "beds_available": 2, "specialty": "急诊中心", "wait_time": "45分钟"},
            {"name": "University Hospital", "address": "789 Research Blvd", "distance": 3.1, "lat": 40.7180, "lng": -74.0020, "beds_available": 8, "specialty": "教学医院", "wait_time": "15分钟"},
            {"name": "Children's Hospital", "address": "101 Pediatric Way", "distance": 3.5, "lat": 40.7100, "lng": -74.0100, "beds_available": 3, "specialty": "儿科医院", "wait_time": "20分钟"},
            {"name": "Community Health Center", "address": "202 Wellness Dr", "distance": 1.8, "lat": 40.7140, "lng": -74.0070, "beds_available": 0, "specialty": "社区医疗", "wait_time": "60分钟"},
        ]
    
    def _get_user_location(self):
        """获取用户位置"""
        # 真实情况下应使用地理定位API
        # 这里使用模拟数据
        return {"lat": 40.7128, "lng": -74.0060}
    
    def _search_nearby_hospitals(self, location, specialty=None, radius=10):
        """搜索附近的医院"""
        # 真实情况下应调用外部API查询附近医院
        # 这里使用模拟数据
        
        # 模拟搜索逻辑
        if specialty and specialty != "所有科室":
            # 过滤指定科室的医院
            filtered_hospitals = [h for h in self.hospitals if specialty.lower() in h["specialty"].lower()]
            return filtered_hospitals if filtered_hospitals else self.hospitals
        
        return self.hospitals
    
    def _create_hospital_map(self, user_location, hospitals):
        """创建医院地图"""
        # 创建地图对象
        m = folium.Map(location=[user_location["lat"], user_location["lng"]], zoom_start=13)
        
        # 添加用户位置标记
        folium.Marker(
            [user_location["lat"], user_location["lng"]],
            popup="您的位置",
            icon=folium.Icon(color="red", icon="home")
        ).add_to(m)
        
        # 添加医院标记
        for hospital in hospitals:
            # 根据床位可用性选择颜色
            color = "green" if hospital["beds_available"] > 0 else "orange"
            
            folium.Marker(
                [hospital["lat"], hospital["lng"]],
                popup=f"{hospital['name']}<br>{hospital['specialty']}<br>可用床位: {hospital['beds_available']}<br>预计等待时间: {hospital['wait_time']}",
                icon=folium.Icon(color=color, icon="plus-sign")
            ).add_to(m)
        
        return m
    
    def render(self):
        """渲染医院查找界面"""
        st.header("🏥 查找附近医院")
        
        # 用户输入
        st.write("查找附近医院和紧急护理中心")
        
        # 获取当前诊断的医疗条件
        medical_condition = None
        if 'current_diagnosis' in st.session_state and st.session_state.current_diagnosis:
            # 从诊断中提取医疗条件
            import re
            text = st.session_state.current_diagnosis
            condition_match = re.search(r'初步诊断[:：]\s*([^\n]+)', text)
            if condition_match:
                medical_condition = condition_match.group(1).strip()
        
        # 科室选择
        specialties = ["所有科室", "急诊科", "内科", "外科", "儿科", "妇产科", "神经科", "心脏科", "骨科", "眼科", "皮肤科"]
        
        # 如果有医疗条件，推荐相应科室
        recommended_specialty = None
        if medical_condition:
            # 简单的条件-科室映射逻辑
            condition_to_specialty = {
                "感冒": "内科",
                "流感": "内科",
                "骨折": "骨科",
                "心脏病": "心脏科",
                "头痛": "神经科",
                "皮疹": "皮肤科",
                "眼睛": "眼科",
                "儿童": "儿科"
            }
            
            for condition, specialty in condition_to_specialty.items():
                if condition.lower() in medical_condition.lower() and specialty in specialties:
                    recommended_specialty = specialty
                    break
        
        col1, col2 = st.columns(2)
        with col1:
            selected_specialty = st.selectbox(
                "选择医院科室:",
                specialties,
                index=specialties.index(recommended_specialty) if recommended_specialty else 0
            )
        with col2:
            radius = st.slider("搜索半径(公里):", 1, 30, 10)
        
        col3, col4 = st.columns(2)
        with col3:
            beds_filter = st.checkbox("仅显示有可用床位的医院", value=True)
        with col4:
            sort_by = st.selectbox("排序方式:", ["距离", "等待时间", "可用床位"])
        
        # 搜索按钮
        if st.button("搜索医院"):
            with st.spinner("正在查找附近医院..."):
                # 获取用户位置
                user_location = self._get_user_location()
                
                # 搜索医院
                hospitals = self._search_nearby_hospitals(user_location, selected_specialty, radius)
                
                # 应用筛选器
                if beds_filter:
                    hospitals = [h for h in hospitals if h["beds_available"] > 0]
                
                # 应用排序
                if sort_by == "距离":
                    hospitals = sorted(hospitals, key=lambda x: x["distance"])
                elif sort_by == "等待时间":
                    hospitals = sorted(hospitals, key=lambda x: int(x["wait_time"].replace("分钟", "")))
                elif sort_by == "可用床位":
                    hospitals = sorted(hospitals, key=lambda x: x["beds_available"], reverse=True)
                
                if hospitals:
                    st.success(f"找到 {len(hospitals)} 家附近医院")
                    
                    # 显示地图
                    st.subheader("附近医院地图")
                    m = self._create_hospital_map(user_location, hospitals)
                    folium_static(m)
                    
                    # 显示医院列表
                    st.subheader("医院列表")
                    
                    # 显示医院信息
                    for i, hospital in enumerate(hospitals):
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"#### {i+1}. {hospital['name']} ({hospital['specialty']})")
                                st.write(f"地址: {hospital['address']}")
                                st.write(f"距离: {hospital['distance']} 公里 | 等待时间: {hospital['wait_time']}")
                                st.write(f"可用床位: {hospital['beds_available']}")
                            with col2:
                                if st.button("导航", key=f"hosp_nav_{i}"):
                                    st.info(f"已开始导航至 {hospital['name']}")
                                
                                if st.button("预约", key=f"hosp_book_{i}"):
                                    st.success(f"已为您在 {hospital['name']} 预约挂号")
                            
                            st.divider()
                else:
                    st.error(f"在半径 {radius}公里内未找到符合条件的医院")
                    st.info("请尝试增加搜索半径或更改科室选择")