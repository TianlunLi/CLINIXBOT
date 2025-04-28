import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

class VisualizationDashboard:
    # components/visualization_dashboard.py 中的 __init__ 方法

    def __init__(self, data, language="en"):
        self.data = data
        self.language = language
        
    def _preprocess_data(self):
        """数据预处理"""
        # 转换日期列
        date_columns = ['Admit Date', 'Discharge Date']
        for col in date_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_datetime(self.data[col])
        
        # 计算住院天数
        if 'Admit Date' in self.data.columns and 'Discharge Date' in self.data.columns:
            self.data['Stay Duration'] = (self.data['Discharge Date'] - self.data['Admit Date']).dt.days
        
        # 提取年月信息
        if 'Admit Date' in self.data.columns:
            self.data['Admit Year'] = self.data['Admit Date'].dt.year
            self.data['Admit Month'] = self.data['Admit Date'].dt.month
            self.data['Admit YearMonth'] = self.data['Admit Date'].dt.strftime('%Y-%m')
        
        return self.data
    
    def _plot_medical_conditions_distribution(self):
        """绘制医疗条件分布图"""
        if 'Medical Condition' not in self.data.columns:
            return st.error("数据中缺少'Medical Condition'列")
        
        # 统计Top 10医疗条件
        condition_counts = self.data['Medical Condition'].value_counts().nlargest(10)
        
        # 使用Plotly创建条形图
        fig = px.bar(
            x=condition_counts.values,
            y=condition_counts.index,
            orientation='h',
            title='Top 10 医疗条件分布',
            labels={'x': '患者数量', 'y': '医疗条件'},
            color=condition_counts.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="患者数量",
            yaxis_title="医疗条件",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _plot_billing_analysis(self):
        """绘制账单分析图表"""
        if 'Bill Amount' not in self.data.columns or 'Medical Condition' not in self.data.columns:
            return st.error("数据中缺少必要的列")
        
        # 按医疗条件统计平均账单金额
        avg_bill_by_condition = self.data.groupby('Medical Condition')['Bill Amount'].mean().nlargest(10)
        
        # 创建条形图
        fig = px.bar(
            x=avg_bill_by_condition.index,
            y=avg_bill_by_condition.values,
            title='各医疗条件的平均账单金额',
            labels={'x': '医疗条件', 'y': '平均账单金额 ($)'},
            color=avg_bill_by_condition.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="医疗条件",
            yaxis_title="平均账单金额 ($)",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render(self):
        """渲染可视化仪表盘"""
        st.header("📊 医疗数据分析仪表盘")
        
        # 预处理数据
        self._preprocess_data()
        
        # 显示关键指标
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("患者总数", f"{len(self.data):,}")
        with col2:
            avg_bill = self.data['Bill Amount'].mean()
            st.metric("平均账单金额", f"${avg_bill:.2f}")
        with col3:
            if 'Stay Duration' in self.data.columns:
                avg_stay = self.data['Stay Duration'].mean()
                st.metric("平均住院天数", f"{avg_stay:.1f} 天")
        with col4:
            if 'Medical Condition' in self.data.columns:
                unique_conditions = self.data['Medical Condition'].nunique()
                st.metric("疾病种类数", f"{unique_conditions}")
        
        # 创建选项卡
        tab1, tab2 = st.tabs(["疾病分布", "账单分析"])
        
        with tab1:
            self._plot_medical_conditions_distribution()
        
        with tab2:
            self._plot_billing_analysis()