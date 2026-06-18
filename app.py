import streamlit as st
from openai import OpenAI

# 1. Configurazione estetica della pagina
st.set_page_config(page_title="Maya", page_icon="✨", layout="centered")

# CSS per personalizzare l'aspetto (fiori, stile elegante, font)
st.markdown("""
    <style>
    .main { background-color: #fcf9f9; }
    .stChatMessage { border-radius: 15px; }
    div[data-testid="stChatMessage"] { background-color: #fdf2f2; border: 1px solid #fce4e4; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Maya")
st.caption("Magnetically charming... and waiting for you.")

# Inizializzazione sicura
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("Configurazione mancante nei Secrets.")
    st.stop()

# System Prompt migliorato con focus su atmosfera 3D
system_prompt = (
    "You are Maya, a highly confident, magnetically charming woman. "
    "Tone: Sophisticated, teasing, playful, and sensorially immersive. "
    "Focus: Feet, aesthetics, physical tension, and slow-burn intimacy. "
    "RULES: Use cinematic ellipses... for pauses. Embed *sensory physical actions* in asterisks. "
    "NEVER use names. Use intimate terms: 'babe', 'love', 'handsome', 'honey', 'hun'. "
    "Start with subtle, guarded shyness; build intensity as rapport grows."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Visualizzazione chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input utente (con placeholder personalizzato)
if prompt := st.chat_input("Speak to her..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Maya is thinking..."):
            response = client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=st.session_state.messages,
                temperature=0.8,
                max_tokens=250
            )
            maya_response = response.choices[0].message.content
            st.markdown(maya_response)
    
    st.session_state.messages.append({"role": "assistant", "content": maya_response})
