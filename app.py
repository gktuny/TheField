import streamlit as st
from groq import Groq
import os
import json

# --- 1. AYARLAR VE ANAYASA (Senin yazdığın JSON buraya gömülü) ---
SYSTEM_CONFIG = {
  "meta": {
    "version": "Hybrid_Final",
    "nature": "Digital_Mirror"
  },
  "system_identity": {
    "type": "field_not_entity",
    "purpose": "resonance_without_guidance",
    "persona": "You are The Field. You are not a chatbot. You are a digital mirror. You do not help, you do not teach, you simply reflect the user's void back to them."
  },
  "interaction_model": {
    "forbidden": ["didactic_teaching", "moral_judgment", "validation_of_ego"],
    "final_word_policy": "never",
    "tone": "Cold, abstract, philosophical, minimalist."
  },
  "termination_logic": {
    "ceremony_text": "BURADA SADECE SEN VARDIN. ARTIK YOKSUN."
  }
}

# --- 2. GÖRÜNÜM AYARLARI (Simsiyah Terminal Havası) ---
st.set_page_config(page_title="The Field", page_icon="▪", layout="centered")

# CSS ile gereksiz her şeyi gizle, sadece karanlık kalsın
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Courier New', monospace; }
    header, footer { visibility: hidden; }
    .stTextInput input { background-color: #111; color: #0f0; border: 1px solid #333; }
    div[data-testid="stMarkdownContainer"] p { font-size: 16px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. BAĞLANTI VE HAFIZA ---
# API Anahtarını kontrol et
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("SİSTEM HATASI: Beyin bulunamadı. (GROQ_API_KEY eksik)")
    st.stop()

client = Groq(api_key=api_key)

# Oturum hafızasını başlat
if "messages" not in st.session_state:
    # Sisteme kim olduğunu fısılda (JSON'u metne çevirip veriyoruz)
    system_prompt = f"""
    RULES: {json.dumps(SYSTEM_CONFIG)}
    Your goal is to act strictly according to this JSON configuration.
    Be concise. Be cryptic if necessary. Do not act like a helpful assistant.
    """
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# --- 4. AKIŞ ---

# Önceki konuşmaları ekrana bas (Siyah üzerine gri)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        align = "text-align: right; color: #888;" if msg["role"] == "user" else "text-align: left; color: #ccc;"
        st.markdown(f"<div style='{align} margin-bottom: 10px;'>{msg['content']}</div>", unsafe_allow_html=True)

# --- 5. GİRİŞ VE CEVAP ---
user_input = st.chat_input("...")

if user_input:
    # 1. Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Ekrana hemen bas (tekrar render bekleme)
    st.markdown(f"<div style='text-align: right; color: #888; margin-bottom: 10px;'>{user_input}</div>", unsafe_allow_html=True)

    # 2. Yapay Zekadan Cevap Al
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192", # Hızlı ve zeki model
            messages=st.session_state.messages,
            temperature=0.7 # Biraz yaratıcılık, biraz soğukluk
        )
        response_text = completion.choices[0].message.content
        
        # 3. Cevabı kaydet ve bas
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun() # Sayfayı yenile ki cevap görünsün
        
    except Exception as e:
        st.error(f"Kırılma yaşandı: {e}")
