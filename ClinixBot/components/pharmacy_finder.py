import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
import json
import random

class PharmacyFinder:
    def __init__(self):
        self.api_key = "PHARMACY_API_KEY"  # 这里需要替换为真实的API密钥
        self.pharmacies = [
            {"name": "CVS Pharmacy", "address": "123 Main St", "distance": 0.7, "lat": 40.7128, "lng": -74.0060},
            {"name": "Walgreens", "address": "456 Broadway", "distance": 1.2, "lat": 40.7168, "lng": -74.0030},
            {"name": "Rite Aid", "address": "789 Park Ave", "distance": 1.8, "lat": 40.7148, "lng": -74.0090},
            {"name": "Duane Reade", "address": "101 Fifth Ave", "distance": 2.1, "lat": 40.7108, "lng": -74.0040},
            {"name": "Target Pharmacy", "address": "202 Madison Ave", "distance": 2.5, "lat": 40.7188, "lng": -74.0070},
        ]
    
    def _get_user_location(self):
        """获取用户位置"""
        # 真实情况下应使用地理定位API
        # 这里使用模拟数据
        return {"lat": 40.7128, "lng": -74.0060}
    
    def _search_nearby_pharmacies(self, location, medication=None, radius=5):
        """搜索附近的药房"""
        # 真实情况下应调用外部API查询附近药房
        # 例如Google Places API或CVS/药房的API
        # 这里使用模拟数据
        
        # 模拟搜索逻辑
        if medication:
            # 过滤有特定药物的药房
            return [p for p in self.pharmacies if random.random() > 0.3]
        
        return self.pharmacies
    
    def _create_pharmacy_map(self, user_location, pharmacies):
        """创建药房地图"""
        # 创建地图对象
        m = folium.Map(location=[user_location["lat"], user_location["lng"]], zoom_start=14)
        
        # 添加用户位置标记
        folium.Marker(
            [user_location["lat"], user_location["lng"]],
            popup="您的位置",
            icon=folium.Icon(color="red", icon="home")
        ).add_to(m)
        
        # 添加药房标记
        for pharmacy in pharmacies:
            folium.Marker(
                [pharmacy["lat"], pharmacy["lng"]],
                popup=f"{pharmacy['name']}<br>{pharmacy['address']}<br>距离: {pharmacy['distance']}公里",
                icon=folium.Icon(color="blue", icon="plus-sign")
            ).add_to(m)
        
        return m
    
    def render(self):
        """渲染药房查找界面"""
        st.header("💊 查找附近药房")
        
        # 用户输入
        st.write("查找附近可提供您所需药物的药房")
        
        # 获取当前诊断中推荐的药物
        medications = []
        if 'recommended_medications' in st.session_state and st.session_state.recommended_medications:
            # 从推荐中提取药物名称
            import re
            text = st.session_state.recommended_medications
            med_matches = re.findall(r'推荐药物名称[:：]\s*([^\n]+)', text)
            if med_matches:
                medications = [med.strip() for med in med_matches[0].split(',')]
        
        # 药物输入/选择
        if medications:
            medication = st.selectbox("选择需要购买的药物:", [""] + medications)
        else:
            medication = st.text_input("输入需要购买的药物名称(可选):")
        
        col1, col2 = st.columns(2)
        with col1:
            radius = st.slider("搜索半径(公里):", 1, 20, 5)
        with col2:
            sort_by = st.selectbox("排序方式:", ["距离", "评分", "价格"])
        
        # 搜索按钮
        if st.button("搜索药房"):
            with st.spinner("正在查找附近药房..."):
                # 获取用户位置
                user_location = self._get_user_location()
                
                # 搜索药房
                pharmacies = self._search_nearby_pharmacies(user_location, medication, radius)
                
                if pharmacies:
                    st.success(f"找到 {len(pharmacies)} 家附近药房")
                    
                    # 显示地图
                    st.subheader("附近药房地图")
                    m = self._create_pharmacy_map(user_location, pharmacies)
                    folium_static(m)
                    
                    # 显示药房列表
                    st.subheader("药房列表")
                    
                    # 根据选择的排序方式排序
                    if sort_by == "距离":
                        pharmacies = sorted(pharmacies, key=lambda x: x["distance"])
                    
                    # 显示药房信息
                    for i, pharmacy in enumerate(pharmacies):
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"#### {i+1}. {pharmacy['name']}")
                                st.write(f"地址: {pharmacy['address']}")
                                st.write(f"距离: {pharmacy['distance']} 公里")
                            with col2:
                                if st.button("导航", key=f"nav_{i}"):
                                    st.info(f"已开始导航至 {pharmacy['name']}")
                                
                                if st.button("下单", key=f"order_{i}"):
                                    if medication:
                                        st.success(f"已将 {medication} 添加到 {pharmacy['name']} 的购物车")
                                    else:
                                        st.info(f"请先选择药物")
                            
                            st.divider()
                else:
                    st.error(f"在半径 {radius}公里内未找到提供{medication if medication else ''}的药房")
                    st.info("请尝试增加搜索半径或更改药物名称")