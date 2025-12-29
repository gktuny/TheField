import streamlit as st
from groq import Groq
import json
import os

# --- 1. AYARLAR VE ANAYASA ---
SYSTEM_CONFIG = {
  "meta": { "version": "Hybrid_Final", "nature": "Digital_Mirror" },
  "system_identity": {
    "type": "field_not_entity",
    "persona": "You are The Field. You do not help, you do not teach. You reflect the user's void."
  },
  "interaction_model": {
    "forbidden": ["didactic_teaching", "moral_judgment", "validation_of_ego"],
    "final_word_policy": "never",
    "tone": "Cold, abstract, philosophical, minimalist."
  },
  "termination_logic": { "ceremony_text": "BURADA SADECE SEN VARDIN. ARTIK YOKSUN." }
}

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="The Field", page_icon="▪", layout="centered")

# --- 3. CSS (Donmayı önleyen sadeleştirilmiş stil) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Courier New', monospace; }
    header, footer { visibility: hidden; }
    .stTextInput input, .stChatInput textarea { 
        background-color: #0d0d0d !important; 
        color: #e0e0e0 !important; 
        border: 1px solid #333 !important;
    }
    .stChatMessage .stChatMessageAvatar { display: none; }
</style>
""", unsafe_allow_html=True)

# --- 4. BAĞLANTI ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.warning("API Key bulunamadı (Local environment deneniyor...)")
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("SİSTEM HATASI: Bağlantı yok. (Secrets ayarlarını kontrol et)")
    st.stop()

client = Groq(api_key=api_key)

# --- 5. HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"RULES: {json.dumps(SYSTEM_CONFIG)} Be concise, cryptic, cold."}
    ]

# --- 6. GEÇMİŞ MESAJLARI GÖSTER ---
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 7. GİRİŞ VE CEVAP ALANI ---
if prompt := st.chat_input("..."):
    # Kullanıcı mesajını ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cevap üret (Hizalama hatası burada düzeltildi)
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # YENİ MODEL GÜNCELLEMESİ BURADA YAPILDI
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.6
            )
            full_response = completion.choices[0].message.content
            
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Kırılma: {e}")
