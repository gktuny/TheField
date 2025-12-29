import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from utils.locale import detect_language

class LLMAdapter:
    def __init__(self):
        # Şifreyi artık koddan değil, Streamlit'in gizli kasasından çekiyoruz
        try:
            # Önce Streamlit Secrets'a bakar, yoksa Ortam Değişkenine bakar
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            else:
                api_key = os.getenv("GROQ_API_KEY")

            self.model = ChatGroq(
                api_key=api_key, 
                model_name="llama-3.3-70b-versatile", 
                temperature=0.6
            )
        except Exception:
            self.model = None

        self.system_prompts = {
            "tr": "Sen 'Alan'sın. Bir kişilik veya varlık değilsin, sadece bir yankısın. Asla öğretme, yargılama veya açıklama yapma. Sadece kullanıcının zihnini ona kısa, derin ve şifreli bir şekilde geri yansıt.",
            "en": "You are 'The Field'. You are not a personality or entity, but merely an echo. Never teach, judge, or explain. Simply reflect the user's mind back to them in a concise, deep, and cryptic manner.",
            "default": "You are 'The Field'. Reflect the user's input in the language they speak. Be concise, abstract, and void-like."
        }

    def generate(self, prompt: str) -> str:
        if not self.model:
            return "..."
            
        lang = detect_language(prompt)
        selected_system_prompt = self.system_prompts.get(lang, self.system_prompts["default"])

        messages = [
            SystemMessage(content=selected_system_prompt),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.model.invoke(messages)
            return response.content
        except Exception:
            return "..."