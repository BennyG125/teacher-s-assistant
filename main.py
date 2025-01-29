import openai
import os
from dotenv import load_dotenv
import streamlit as st
from kategori_bestemmer import bestem_kategori
from evaluering import novelle, essay, litteraturhistorie, rapport

# Last inn API-nøkkel
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funksjon for tekstvurdering basert på kategori
def evaluer_tekst(tekst):
    # Bestem kategori for teksten
    kategori = bestem_kategori(tekst)

    # Kall på riktig vurderingsfunksjon basert på kategori
    if kategori == "novelle":
        return novelle.vurder_novelle(tekst)
    elif kategori == "essay":
        return essay.vurder_essay(tekst)
    elif kategori == "litteraturhistorie":
        return litteraturhistorie.vurder_litteraturhistorie(tekst)
    elif kategori == "rapport":
        return rapport.vurder_rapport(tekst)
    else:
        return "Ukjent kategori. Kan ikke evaluere."

# Streamlit app start
st.title("Lærerassistent Chatbot")

# Legg til CSS for mørk bakgrunn
st.markdown(
    """
    <style>
    body {
        background-color: #222; /* Mørk bakgrunn */
        color: #eee; /* Lys tekstfarge for kontrast */
    }
    .chat-message { /* Styling for chat-meldinger */
        background-color: #333; /* Litt lysere bakgrunn for meldinger */
        color: #eee;
        border-radius: 8px; /* Avrundede hjørner for meldinger */
        padding: 10px; /* Padding rundt teksten i meldingene */
        margin-bottom: 10px; /* Margin mellom meldinger */
    }
    .user-message { /* Spesifikk styling for brukermeldinger */
        background-color: #444; /* Litt mørkere bakgrunn for brukermeldinger */
    }
    .assistant-message { /* Spesifikk styling for assistentmeldinger */
        background-color: #555; /* Enda litt mørkere bakgrunn for assistentmeldinger */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initier chatboks
if "messages" not in st.session_state:
    st.session_state.messages = []

# Funksjon for å vise chat-historikk
def display_chat():
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

# Sørg for at chatfeltet er nederst etter hver ny melding
if st.session_state.messages:
    # Display chat history first
    display_chat()

# Håndterer brukerinput og genererer svar
user_input = st.text_area("Skriv inn teksten du ønsker å evaluere:", height=200)

if user_input:
    # Forkort brukerens tekst til de første 20 ordene
    first_20_words = " ".join(user_input.split()[:20])

    # Legg til brukerens forkortede tekst i chat-historikken
    st.session_state.messages.append({"role": "user", "content": f"{first_20_words}..."})

    # Evaluer teksten
    vurdering = evaluer_tekst(user_input)

    # Legg til botens svar i chat-historikken
    st.session_state.messages.append({"role": "assistant", "content": vurdering})

    # Display updated chat history again, with new message
    display_chat()

    # Scroll to bottom using JavaScript (valgfritt, se forklaring under)
    st.markdown(
        """
        <script>
        const chatContainer = document.querySelector('div[role="main"]');
        chatContainer.scrollTop = chatContainer.scrollHeight;
        </script>
        """,
        unsafe_allow_html=True,
    )