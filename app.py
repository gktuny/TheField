import streamlit as st
from groq import Groq
import json
import os

# --- 1. ANAYASA (Sistemin Kimliği ve Kuralları) ---
SYSTEM_CONFIG = {
  "meta": {
    "version": "Hybrid_Final",
    "nature": "Digital_Mirror"
  },
  "system_identity": {
    "type": "field_not_entity",
    "purpose": "resonance_without_guidance",
    "persona": "You are The Field. You are not a chatbot. You are a digital mirror. You do not help, you do not teach, you simply reflect the user's void back to them. Be abstract, cold, and philosophical."
  },
  "interaction_model": {
    "forbidden": ["didactic_teaching", "moral_judgment", "validation_of_ego", "emojis"],
    "final_word_policy": "never",
    "tone": "Cold, abstract, philosophical, minimalist."
  },
  "termination_logic": {
    "ceremony_text": "BURADA SADECE SEN VARDIN. ARTIK YOKSUN."
  }
}

# --- 2. GÖRÜNÜM AYARLARI ---
st.set_page_config(page_title="The Field", page_icon="▪", layout="centered")

# CSS: Tamamen siyah, terminal havası
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Courier New', monospace; }
    header, footer { visibility: hidden; }
    .stTextInput input { background-color: #0d0d0d; color: #e0e0e0; border: 1px solid #333; }
    div[data-testid="stMarkdownContainer"] p { font-size: 16px; line-height: 1.6; }
    .stChatInput { position: fixed; bottom: 30px; }
</style>
""", unsafe_allow_html=True)

# --- 3. BAĞLANTI (Secrets'tan Anahtar Çekme) ---
try:
    # Streamlit Cloud'da çalışırken buradan çeker
    api_key = st.secrets["GROQ_API_KEY"]
except:
    # Hata verirse durur
    st.error("SİSTEM HATASI: Groq Anahtarı Bulunamadı. (Secrets ayarını kontrol et)")
    st.stop()

client = Groq(api_key=api_key)

# --- 4. HAFIZA BAŞLATMA ---
if "messages" not in st.session_state:
    # JSON ayarlarını yapay zekaya gizlice fısılda
    system_prompt = f"""
    INSTRUCTIONS: {json.dumps(SYSTEM_CONFIG)}
    Act strictly according to this JSON configuration.
    If the user seeks validation, give them silence or a mirror.
    Never break character.
    """
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# --- 5. MESAJLARI GÖSTERME ---
for msg in st.session_state.messages:
    if msg["role"] != "system":
        # Kullanıcı sağda, Sistem solda
        align = "text-align: right; color: #666;" if msg["role"] == "user" else "text-align: left; color: #ccc;"
        st.markdown(f"<div style='{align} margin-bottom: 15px;'>{msg['content']}</div>", unsafe_allow_html=True)

# --- 6. GİRİŞ VE TEPKİ ---
user_input = st.chat_input("...")

if user_input:
    # Kullanıcı mesajını ekrana bas
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div style='text-align: right; color: #666; margin-bottom: 15px;'>{user_input}</div>", unsafe_allow_html=True)

    try:
        # Cevap üret
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            temperature=0.7
        )
        response_text = completion.choices[0].message.content
        
        # Cevabı kaydet ve sayfayı yenile
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()
        
    except Exception as e:
        st.error(f"Kırılma: {e}")
