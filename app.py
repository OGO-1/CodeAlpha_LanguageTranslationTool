import streamlit as st
import requests
from gtts import gTTS
import tempfile

st.set_page_config(page_title="LinguaAI - Language Translator", page_icon="🌍", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

.hero {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
}

.result-box {
    background: linear-gradient(135deg, rgba(167,139,250,0.15), rgba(96,165,250,0.15));
    border: 1px solid rgba(167, 139, 250, 0.5);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #ffffff !important;
    font-size: 1.1rem;
    line-height: 1.7;
}

.lang-badge {
    display: inline-block;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    color: white !important;
    border-radius: 20px;
    padding: 0.3rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.tts-notice {
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.4);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    color: #fbbf24 !important;
    font-size: 0.9rem;
    margin-top: 1rem;
}

.footer {
    text-align: center;
    color: #475569;
    font-size: 0.85rem;
    padding: 2rem 0 1rem 0;
}

.stButton > button {
    background: linear-gradient(90deg, #a78bfa, #60a5fa) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
}

.stTextArea textarea {
    color: #ffffff !important;
    background-color: #1e1b4b !important;
    border: 1px solid rgba(167, 139, 250, 0.4) !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1e1b4b !important;
    color: #ffffff !important;
    border: 1px solid rgba(167, 139, 250, 0.4) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🌍 LinguaAI</h1>
    <p>Instantly translate text across 12 languages with AI-powered speech</p>
</div>
""", unsafe_allow_html=True)

LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Chinese": "zh",
    "Japanese": "ja",
    "Yoruba": "yo",
    "Hausa": "ha",
    "Igbo": "ig",
}

TTS_SUPPORTED = ["en", "fr", "es", "de", "it", "pt", "ar", "zh", "ja"]

col1, col2, col3 = st.columns([5, 1, 5])

with col1:
    source_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    swap = st.button("⇄")

with col3:
    target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=1)

if swap:
    source_lang, target_lang = target_lang, source_lang

source_text = st.text_area("✍️ Enter text to translate", height=160, placeholder="Start typing here...")

translate_btn = st.button("🌐 Translate Now")

if translate_btn:
    if source_text.strip() == "":
        st.warning("⚠️ Please enter some text before translating.")
    else:
        with st.spinner("✨ Translating..."):
            try:
                src_code = LANGUAGES[source_lang]
                tgt_code = LANGUAGES[target_lang]
                lang_pair = f"{src_code}|{tgt_code}"
                url = f"https://api.mymemory.translated.net/get?q={source_text}&langpair={lang_pair}"
                response = requests.get(url)
                data = response.json()
                translated = data["responseData"]["translatedText"]

                st.markdown(f'<div class="lang-badge">✅ Translated to {target_lang}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                if tgt_code in TTS_SUPPORTED:
                    st.markdown("**🔊 Listen to Translation**")
                    tts_lang = "zh-TW" if tgt_code == "zh" else tgt_code
                    tts = gTTS(text=translated, lang=tts_lang, slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                        tts.save(f.name)
                        st.audio(f.name, format="audio/mp3")
                else:
                    st.markdown(f'<div class="tts-notice">🔇 Text-to-speech is not available for {target_lang} yet.</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown('<div class="footer">Built with ❤️ by OGO · Powered by Streamlit & MyMemory API</div>', unsafe_allow_html=True)
