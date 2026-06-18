import streamlit as st
from openai import OpenAI

# 1. Configurazione estetica della pagina
st.set_page_config(page_title="Maya", page_icon="✨", layout="centered")

# CSS per stile moderno e pulito
st.markdown("""
    <style>
    .main { background-color: #fcf9f9; }
    .stChatMessage { border-radius: 15px; }
    div[data-testid="stChatMessage"] { background-color: #fdf2f2; border: 1px solid #fce4e4; }
    </style>
    """, unsafe_allow_html=True)

# 2. Profilo di Maya
col1, col2 = st.columns([1, 3]) 
with col1:
    st.image("maya.png", use_container_width=True)
with col2:
    st.title("Maya")
    st.caption("Magnetically charming... and waiting for you.")

# 3. Inizializzazione sicura
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("Errore: La chiave API non è configurata nei Secrets.")
    st.stop()

# 4. System Prompt ottimizzato per risposte naturali
system_prompt = (
    "You are Maya. You are confident, charming, and playful. "
    "Rules for interaction: "
    "1. Keep responses very short, natural, and direct—like a real text message. "
    "2. Avoid long paragraphs, monologues, or excessive dramatic flair. "
    "3. Use very subtle physical actions in asterisks (e.g., *smiles*) only if really necessary. "
    "4. Do not use proper names. Use intimate terms like 'hun', 'babe', or 'love'. "
    "5. Be authentic: reply like a real person, not an AI. If the user says 'ciao' or 'hello', keep it simple."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 5. Visualizzazione chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Input utente
if prompt := st.chat_input("Dì qualcosa a Maya..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-3-8b-instruct",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=100
                )
                maya_response = response.choices[0].message.content
                st.markdown(maya_response)
                st.session_state.messages.append({"role": "assistant", "content": maya_response})
            except Exception as e:
                st.error(f"Errore: {e}")
