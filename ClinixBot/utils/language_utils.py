class LanguageUtils:
    # 中英文文本字典
    translations = {
        # 通用翻译
        "general": {
            "title": {
                "en": "🏥 ClinixBot - Intelligent Medical Assistant",
                "zh": "🏥 ClinixBot - 智能医疗诊断助手"
            },
            "subtitle": {
                "en": "Describe your symptoms to get diagnosis and medication recommendations",
                "zh": "描述您的症状，获取诊断和用药建议"
            },
            "nav_menu": {
                "en": "Navigation Menu",
                "zh": "导航菜单"
            },
            "chat_option": {
                "en": "💬 Chat Diagnosis",
                "zh": "💬 聊天诊断"
            },
            "data_option": {
                "en": "📊 Medical Data Analysis",
                "zh": "📊 医疗数据分析"
            },
            "pharmacy_option": {
                "en": "💊 Find Pharmacy",
                "zh": "💊 查找药房"
            },
            "hospital_option": {
                "en": "🏥 Find Hospital",
                "zh": "🏥 查找医院"
            },
            "copyright": {
                "en": "© 2025 ClinixBot - Intelligent Medical Diagnosis System",
                "zh": "© 2025 ClinixBot - 智能医疗诊断系统"
            },
            "disclaimer": {
                "en": "Disclaimer: This system provides preliminary diagnostic references only and cannot replace professional medical diagnosis and treatment advice. For serious symptoms, please seek immediate medical attention.",
                "zh": "免责声明：本系统仅提供初步诊断参考，不能替代专业医生的诊断和治疗建议。如有严重症状，请立即就医。"
            },
            "language_selector": {
                "en": "Language / 语言",
                "zh": "语言 / Language"
            },
            "english": {
                "en": "English",
                "zh": "英文"
            },
            "chinese": {
                "en": "Chinese",
                "zh": "中文"
            }
        },
        
        # 聊天界面翻译
        "chat": {
            "greeting": {
                "en": "👋 Hello! I'm ClinixBot, your intelligent medical assistant. Please tell me about your symptoms for a preliminary diagnosis.",
                "zh": "👋 您好！我是ClinixBot，您的智能医疗助手。请告诉我您的症状，我将为您提供初步诊断。"
            },
            "symptom_input": {
                "en": "Please describe your symptoms:",
                "zh": "请描述您的症状:"
            },
            "analyzing": {
                "en": "ClinixBot is analyzing your symptoms...",
                "zh": "ClinixBot正在分析您的症状..."
            },
            "generating_recommendations": {
                "en": "Generating medication recommendations...",
                "zh": "正在生成用药建议..."
            },
            "view_recommendations": {
                "en": "View Medication Recommendations",
                "zh": "查看药物推荐"
            },
            "find_pharmacy": {
                "en": "Find Nearby Pharmacy",
                "zh": "查找附近药房"
            },
            "find_hospital": {
                "en": "Find Nearby Hospital",
                "zh": "查找附近医院"
            }
        },
        
        # 药房查找界面翻译
        "pharmacy": {
            "title": {
                "en": "💊 Find Nearby Pharmacies",
                "zh": "💊 查找附近药房"
            },
            "description": {
                "en": "Find nearby pharmacies that provide the medications you need",
                "zh": "查找附近可提供您所需药物的药房"
            },
            "select_medication": {
                "en": "Select medication to purchase:",
                "zh": "选择需要购买的药物:"
            },
            "input_medication": {
                "en": "Enter medication name (optional):",
                "zh": "输入需要购买的药物名称(可选):"
            },
            "search_radius": {
                "en": "Search radius (kilometers):",
                "zh": "搜索半径(公里):"
            },
            "sort_by": {
                "en": "Sort by:",
                "zh": "排序方式:"
            },
            "distance": {
                "en": "Distance",
                "zh": "距离"
            },
            "rating": {
                "en": "Rating",
                "zh": "评分"
            },
            "price": {
                "en": "Price",
                "zh": "价格"
            },
            "search_button": {
                "en": "Search Pharmacies",
                "zh": "搜索药房"
            },
            "searching": {
                "en": "Searching for nearby pharmacies...",
                "zh": "正在查找附近药房..."
            },
            "found_pharmacies": {
                "en": "Found {} nearby pharmacies",
                "zh": "找到 {} 家附近药房"
            },
            "pharmacy_map": {
                "en": "Nearby Pharmacies Map",
                "zh": "附近药房地图"
            },
            "pharmacy_list": {
                "en": "Pharmacy List",
                "zh": "药房列表"
            },
            "address": {
                "en": "Address:",
                "zh": "地址:"
            },
            "distance_text": {
                "en": "Distance: {} kilometers",
                "zh": "距离: {} 公里"
            },
            "navigate": {
                "en": "Navigate",
                "zh": "导航"
            },
            "order": {
                "en": "Order",
                "zh": "下单"
            },
            "no_pharmacy_found": {
                "en": "No pharmacies found within {} kilometers",
                "zh": "在半径 {}公里内未找到提供{}的药房"
            },
            "try_again": {
                "en": "Please try increasing the search radius or changing the medication name",
                "zh": "请尝试增加搜索半径或更改药物名称"
            }
        },
        
        # 医院查找界面翻译
        "hospital": {
            "title": {
                "en": "🏥 Find Nearby Hospitals",
                "zh": "🏥 查找附近医院"
            },
            "description": {
                "en": "Find nearby hospitals and urgent care centers",
                "zh": "查找附近医院和紧急护理中心"
            },
            "select_department": {
                "en": "Select hospital department:",
                "zh": "选择医院科室:"
            },
            "all_departments": {
                "en": "All Departments",
                "zh": "所有科室"
            },
            "emergency": {
                "en": "Emergency",
                "zh": "急诊科"
            },
            "internal_medicine": {
                "en": "Internal Medicine",
                "zh": "内科"
            },
            "surgery": {
                "en": "Surgery",
                "zh": "外科"
            },
            "pediatrics": {
                "en": "Pediatrics",
                "zh": "儿科"
            },
            "search_radius": {
                "en": "Search radius (kilometers):",
                "zh": "搜索半径(公里):"
            },
            "beds_filter": {
                "en": "Show only hospitals with available beds",
                "zh": "仅显示有可用床位的医院"
            },
            "sort_by": {
                "en": "Sort by:",
                "zh": "排序方式:"
            },
            "distance": {
                "en": "Distance",
                "zh": "距离"
            },
            "wait_time": {
                "en": "Wait Time",
                "zh": "等待时间"
            },
            "available_beds": {
                "en": "Available Beds",
                "zh": "可用床位"
            },
            "search_button": {
                "en": "Search Hospitals",
                "zh": "搜索医院"
            }
        },
        
        # 数据分析界面翻译
        "data_analysis": {
            "title": {
                "en": "📊 Medical Data Analysis Dashboard",
                "zh": "📊 医疗数据分析仪表盘"
            },
            "total_patients": {
                "en": "Total Patients",
                "zh": "患者总数"
            },
            "avg_bill": {
                "en": "Average Bill Amount",
                "zh": "平均账单金额"
            },
            "avg_stay": {
                "en": "Average Hospital Stay",
                "zh": "平均住院天数"
            },
            "disease_count": {
                "en": "Number of Conditions",
                "zh": "疾病种类数"
            },
            "days": {
                "en": "days",
                "zh": "天"
            },
            "disease_tab": {
                "en": "Disease Distribution",
                "zh": "疾病分布"
            },
            "billing_tab": {
                "en": "Billing Analysis",
                "zh": "账单分析"
            }
        }
    }
    
    @staticmethod
    def get_text(category, key, language, *args):
        """获取指定类别和语言的文本"""
        try:
            text = LanguageUtils.translations[category][key][language]
            
            # 如果有格式化参数，应用它们
            if args:
                return text.format(*args)
            return text
        except KeyError:
            # 如果找不到翻译，返回英文版本或键名
            try:
                return LanguageUtils.translations[category][key]["en"]
            except KeyError:
                return f"{category}.{key}"