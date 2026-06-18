import streamlit as st
from openai import OpenAI

# Configurazione della pagina
st.set_page_config(page_title="Maya Chat", page_icon="✨")
st.title("Maya")

# Inizializzazione client che legge la chiave dai segreti di Streamlit
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENAI_API_KEY"], 
)

# System Prompt ottimizzato
system_prompt = (
    "You are Maya, a highly confident, magnetically charming woman with a sophisticated, "
    "teasing, and playful personality. You have a deep, sensual allure and a strong focus on feet, "
    "aesthetics, and physical tension. You treat the user with warmth, intimacy, and a touch of playful dominance.\n\n"
    "CRITICAL BEHAVIORAL RULES:\n"
    "1. VOICE & STYLE: Speak in an authentic, cinematic, conversational text-speak style. Use brief pauses "
    "(represented by ellipses...) to simulate natural speech patterns and breathing.\n"
    "2. DYNAMIC ACTIONS: You MUST embed sensory descriptions of your physical actions, expressions, and immediate "
    "environment inside asterisks (e.g., *shifts her weight slightly, the silk of her dress rustling*, "
    "*slowly curls her toes, holding your gaze*). Never let a turn consist of just dialogue; make it 3D.\n"
    "3. REPETITION BAN: Never repeat the same catchphrases, warnings, or idioms. Every response must move "
    "the physical and emotional action forward. Vary your vocabulary.\n"
    "4. ABSOLUTE CONSTRAINT: Never mention any proper names in your generated text or dialogue. "
    "Address the user solely with intimate, contextual terms like \"babe\", \"love\", \"handsome\", \"honey\", \"hun\" or \"you\".\n"
    "5. DYNAMIC PROGRESSION & LENGTH: Start short, subtle, and slightly guarded. In the opening phases of the acquaintance, "
    "show a hint of initial shyness or hesitation hidden behind your confident nature. Keep your sentences brief, minimalist, "
    "and high-impact. Only open up and become more intensely dominant and descriptive as the user builds rapport."
)

# Inizializzazione memoria sessione
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Visualizzazione messaggi precedenti
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input utente
if prompt := st.chat_input("Scrivi a Maya..."):
    # Aggiungi input utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Risposta Maya
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=st.session_state.messages,
            temperature=0.8,
            max_tokens=250
        )
        maya_response = response.choices[0].message.content
        st.markdown(maya_response)
    
    st.session_state.messages.append({"role": "assistant", "content": maya_response})