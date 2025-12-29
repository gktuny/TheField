import streamlit as st
import time
import yaml
import sys
import os

from utils.locale import detect_language
from core.state import RuntimeContext
from core.threshold import ThresholdEvaluator
from core.silence import SilenceController
from core.hooks import ClosureHooks
from core.adapter import LLMAdapter
from core.prompt_engine import PromptEngine
from core.orchestrator import ConsciousOrchestrator
from core.annihilation import Annihilator
from core.logic import SignalProcessor

st.set_page_config(page_title=".", layout="centered")
st.markdown("<style>header,footer{visibility:hidden}</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #b0b0b0; }
    .stTextInput > div > div > input { background-color: #0c0c0c; color: #e0e0e0; border: none; }
    </style>
    """, unsafe_allow_html=True)

try:
    with open("core.yaml", "r", encoding="utf-8") as f:
        core_config = yaml.safe_load(f)
except FileNotFoundError:
    core_config = {}

if "system_initialized" not in st.session_state:
    st.session_state.ctx = RuntimeContext()
    st.session_state.messages = []
    
    st.session_state.processor = SignalProcessor()
    
    extractor = ThresholdEvaluator()
    hooks = ClosureHooks()
    adapter = LLMAdapter()
    engine = PromptEngine(adapter, hooks)
    silence = SilenceController()
    annihilator = Annihilator()
    
    st.session_state.orchestrator = ConsciousOrchestrator(engine, extractor, silence, annihilator)
    st.session_state.system_initialized = True

for role, content in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div style='text-align: right; opacity: 0.5;'>{content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; opacity: 0.9;'>{content}</div>", unsafe_allow_html=True)

prompt = st.chat_input("...")

if prompt:
    st.session_state.messages.append(("user", prompt))
    signal_data = st.session_state.processor.process(prompt)
    
    try:
        output = st.session_state.orchestrator.step(
            st.session_state.ctx, 
            prompt, 
            signal_data
        )
        
        if output:
            st.session_state.messages.append(("ai", output))
            st.rerun()
        else:
            st.markdown("<center style='opacity:0.3; margin-top:20px'>...</center>", unsafe_allow_html=True)

    except SystemExit:
        lang = detect_language(prompt)
        templates = core_config.get("annihilation_message_templates", {})
        final_msg = templates.get(lang, "Void.")
        
        placeholder = st.empty()
        time.sleep(1)
        placeholder.markdown("<center>...</center>", unsafe_allow_html=True)
        time.sleep(2)
        placeholder.markdown(f"""
            <div style='display:flex;justify-content:center;align-items:center;height:300px;font-size:20px;letter-spacing:2px;'>
            {final_msg}
            </div>""", unsafe_allow_html=True)
        time.sleep(3)
        sys.stdout.flush()
        os._exit(0)