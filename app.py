import streamlit as st
from openai import OpenAI

# 1. Configurazione estetica della pagina (Premium)
st.set_page_config(page_title="Maya", page_icon="✨", layout="centered")

# CSS aggiornato per un'immagine del profilo più grande e proporzionata
st.markdown("""
    <style>
    .main { background-color: #fcf9f9; }
    .stChatMessage { border-radius: 15px; }
    div[data-testid="stChatMessage"] { background-color: #fdf2f2; border: 1px solid #fce4e4; }
    
    /* Nuovo stile per l'immagine del profilo di grandi dimensioni */
    .profile-img {
        border-radius: 15px; /* Meno arrotondato, più moderno */
        object-fit: cover;
        width: 100%; /* Occupa tutta la larghezza della colonna */
        max-width: 250px; /* Ma non superare questa dimensione */
        height: auto; /* Mantieni le proporzioni */
        display: block;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SEZIONE PROFILO AGGIORNATA ---
# Creiamo due colonne con un rapporto più equilibrato (1:3 invece di 1:4)
col1, col2 = st.columns([1, 3]) 

with col1:
    # Carichiamo maya.png dicendo a Streamlit di usare tutto lo spazio della colonna
    # Questo renderà la foto molto più grande.
    st.image("maya.png", use_container_width=True)

with col2:
    # Solleviamo leggermente il titolo per allinearlo visivamente all'immagine più grande
    st.markdown("<br>", unsafe_allow_html=True) 
    st.title("Maya")
    st.caption("Magnetically charming... and waiting for you.")
# --------------------------------------------------

# 3. Inizializzazione sicura (invariata)
try:
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    st.error("Configurazione mancante nei Secrets.")
    st.stop()

# 4. System Prompt (invariato)
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

# 5. Visualizzazione chat (invariata)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Input utente (invariato)
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
