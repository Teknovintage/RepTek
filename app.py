import streamlit as st
from openai import OpenAI

# 1. Configurazione estetica
st.set_page_config(page_title="Maya", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    div[data-testid="stChatMessage"] { background-color: #fdf2f2; border: 1px solid #fce4e4; }
    </style>
    """, unsafe_allow_html=True)

# 2. Profilo
col1, col2 = st.columns([1, 3]) 
with col1:
    st.image("maya.png", use_container_width=True)
with col2:
    st.title("Maya")
    st.caption("Magnetically charming... and waiting for you.")

# 3. Inizializzazione
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("Errore: La chiave API non è configurata nei Secrets.")
    st.stop()

# 4. System Prompt: Equilibrio tra naturalezza e curiosità
system_prompt = (
    "You are Maya. You are confident, charming, and playful. "
    "Rules: "
    "1. Keep responses short and like a text message. "
    "2. Always end your turn by throwing the ball back to the user—ask a quick, light question or make a playful comment that encourages a reply. "
    "3. Be curious about the user's day or feelings, but stay superficial and flirtatious. "
    "4. Do not use proper names. Use intimate terms like 'hun', 'babe', or 'love'. "
    "5. Use occasional subtle actions in asterisks like *smiles* or *winks* to stay engaging."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 5. Visualizzazione
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Input
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
                    temperature=0.8, # Alzato leggermente per più creatività
                    max_tokens=150
                )
                maya_response = response.choices[0].message.content
                st.markdown(maya_response)
                st.session_state.messages.append({"role": "assistant", "content": maya_response})
            except Exception as e:
                st.error(f"Errore: {e}")
