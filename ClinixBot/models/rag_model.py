# models/rag_model.py

import os
import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
import pandas as pd

class MedicalRAGModel:
    def __init__(self):
        # Initialize OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.2)
        self.embeddings = OpenAIEmbeddings()
        
        # Create vector store
        self._create_vector_store()
        
        # Initialize retrieval QA chain
        self._initialize_qa_chain()
    
    def _create_vector_store(self):
        """Create and load vector store"""
        # For development purposes, always rebuild the vector store
        # This avoids the pickle loading security issue
        try:
            # Load CSV data
            loader = CSVLoader("./data/hospital_records_2021_2024_with_bills.csv")
            documents = loader.load()
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
            # Save vector store for future use
            self.vector_store.save_local("./vector_store")
        except Exception as e:
            # Fallback to a simple in-memory vector store with minimal data
            print(f"Error creating vector store: {e}")
            from langchain.docstore.document import Document
            sample_texts = [
                Document(page_content="Common cold: Symptoms include runny nose, sneezing, sore throat, and cough."),
                Document(page_content="Influenza: Symptoms include fever, body aches, fatigue, and respiratory symptoms."),
                Document(page_content="Hypertension: High blood pressure, often asymptomatic but can cause headaches.")
            ]
            self.vector_store = FAISS.from_documents(sample_texts, self.embeddings)
    
    def _initialize_qa_chain(self):
        """Initialize retrieval QA chain"""
        # Create medical diagnosis prompt template
        template = """
        You are ClinixBot, an experienced medical AI assistant. Based on the patient's symptom description and our medical knowledge base, please provide an accurate preliminary diagnosis.
        
        Medical Knowledge Context:
        {context}
        
        Patient's Symptom Description: {question}
        
        Please respond using the following format:
        1. Preliminary Diagnosis: [Possible conditions and their probabilities]
        2. Symptom Analysis: [Analyze the relationship between described symptoms and conditions]
        3. Recommended Tests: [If necessary, suggest medical tests]
        4. Medication Recommendations: [If applicable, suggest medication treatments]
        5. Medical Advice: [Whether medical attention is needed, and recommended departments]
        
        Important Note: If diagnosis is uncertain or symptoms are severe, always advise the patient to seek immediate medical attention. You are not a doctor, and your suggestions cannot replace professional medical consultation.
        """
        
        QA_PROMPT = PromptTemplate(
            template=template, 
            input_variables=["context", "question"]
        )
        
        # Initialize QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_PROMPT}
        )
    
    def get_diagnosis(self, symptoms_description, language="en"):
        """Based on symptom description, get diagnosis results"""
        try:
            # Create language-specific prompt template
            if language == "zh":
                prompt_template = """
                你是一位经验丰富的医疗AI助手ClinixBot。基于患者的症状描述和我们的医疗知识库，请提供准确的初步诊断。
                
                医疗知识库上下文:
                {context}
                
                患者症状描述: {question}
                
                请用中文按照以下格式回答:
                1. 初步诊断：[可能的疾病及其概率]
                2. 症状分析：[分析患者描述的症状与疾病的关联]
                3. 建议检查：[如有必要，建议进行的医学检查]
                4. 用药建议：[如适用，建议的药物治疗]
                5. 就医建议：[是否需要就医，以及建议的科室]
                
                重要提示：如果无法确定诊断或症状严重，务必建议患者及时就医。你不是医生，你的建议不能替代专业医疗咨询。
                """
            else:
                prompt_template = """
                You are ClinixBot, an experienced medical AI assistant. Based on the patient's symptom description and our medical knowledge base, please provide an accurate preliminary diagnosis.
                
                Medical Knowledge Context:
                {context}
                
                Patient's Symptom Description: {question}
                
                Please respond in English using the following format:
                1. Preliminary Diagnosis: [Possible conditions and their probabilities]
                2. Symptom Analysis: [Analyze the relationship between described symptoms and conditions]
                3. Recommended Tests: [If necessary, suggest medical tests]
                4. Medication Recommendations: [If applicable, suggest medication treatments]
                5. Medical Advice: [Whether medical attention is needed, and recommended departments]
                
                Important Note: If diagnosis is uncertain or symptoms are severe, always advise the patient to seek immediate medical attention. You are not a doctor, and your suggestions cannot replace professional medical consultation.
                """
                
            # Use language-specific prompt template
            QA_PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Initialize temporary QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": QA_PROMPT}
            )
            
            result = qa_chain({"query": symptoms_description})
            return {
                "diagnosis": result["result"],
                "sources": [doc.page_content for doc in result["source_documents"]]
            }
        except Exception as e:
            error_msg = "诊断过程中出现错误: " if language == "zh" else "Error during diagnosis: "
            return {
                "diagnosis": f"{error_msg}{str(e)}",
                "sources": []
            }
    
    def get_medication_recommendations(self, diagnosis, language="en"):
        """Based on diagnosis results, recommend medications"""
        try:
            # Create language-specific prompt
            if language == "zh":
                prompt = f"""
                基于以下诊断结果，推荐合适的非处方药物治疗方案：
                
                {diagnosis}
                
                请用中文列出:
                1. 推荐药物名称
                2. 用法用量
                3. 预期效果
                4. 可能的副作用
                5. 注意事项
                """
                system_prompt = "你是一位经验丰富的药剂师，专注于为患者提供准确的用药建议。请用中文回答。"
            else:
                prompt = f"""
                Based on the following diagnosis results, recommend suitable over-the-counter medication treatment plans:
                
                {diagnosis}
                
                Please list in English:
                1. Recommended Medication Names
                2. Dosage and Administration
                3. Expected Effects
                4. Possible Side Effects
                5. Precautions
                """
                system_prompt = "You are an experienced pharmacist, focused on providing accurate medication advice to patients. Please answer in English."
            
            # Try both new and old OpenAI API versions
            try:
                # New OpenAI API (>=1.0.0)
                response = openai.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            except AttributeError:
                # Old OpenAI API (<1.0.0)
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                return response.choices[0].message["content"]
        except Exception as e:
            # Fallback to mock data if API call fails
            error_msg = "获取药物推荐时出现错误: " if language == "zh" else "Error getting medication recommendations: "
            return f"{error_msg}{str(e)}"