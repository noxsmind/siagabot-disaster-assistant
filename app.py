import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="SiagaBot | Asisten Bencana",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — TEMA "EMERGENCY MODERN"
# Palet: merah darurat, oranye peringatan, netral gelap, aksen kuning
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    :root {
        --danger: #E63946;
        --danger-dark: #B71C2B;
        --warning: #FF9F1C;
        --safe: #2ECC71;
        --ink: #1B1B2F;
        --panel: #16181D;
        --panel-2: #1F222A;
        --text-soft: #C8CCD6;
    }

    .stApp {
        background: radial-gradient(circle at 15% 0%, #241318 0%, #0E0F14 45%, #0B0C10 100%);
    }

    /* ---------- HERO BANNER ---------- */
    .hero-wrap {
        position: relative;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 22px;
        background: linear-gradient(120deg, #B71C2B 0%, #E63946 45%, #FF9F1C 100%);
        box-shadow: 0 10px 35px rgba(230, 57, 70, 0.35);
        overflow: hidden;
    }
    .hero-wrap::after {
        content: "";
        position: absolute;
        top: -40%; right: -10%;
        width: 260px; height: 260px;
        background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0,0,0,0.25);
        color: #fff;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 12px;
        backdrop-filter: blur(4px);
    }
    .pulse-dot {
        width: 8px; height: 8px;
        background: #fff;
        border-radius: 50%;
        animation: pulse 1.4s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.6); }
        70% { box-shadow: 0 0 0 9px rgba(255,255,255,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
    }
    .hero-title {
        color: #fff;
        font-size: 34px;
        font-weight: 800;
        margin: 0 0 6px 0;
        line-height: 1.15;
    }
    .hero-sub {
        color: rgba(255,255,255,0.92);
        font-size: 15.5px;
        max-width: 640px;
        margin: 0;
    }

    /* ---------- QUICK TOPIC CHIPS ---------- */
    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: linear-gradient(180deg, var(--panel-2), var(--panel)) !important;
        color: #EDEEF2 !important;
        padding: 14px 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }
    div[data-testid="stButton"] > button:hover {
        border-color: var(--warning) !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 18px rgba(255, 159, 28, 0.25);
        color: #fff !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(0px);
    }

    /* ---------- SECTION LABEL ---------- */
    .section-label {
        color: var(--warning);
        font-weight: 700;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 22px 0 10px 2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-label::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(255,159,28,0.4), transparent);
    }

    /* ---------- CHAT BUBBLES ---------- */
    div[data-testid="stChatMessage"] {
        background: var(--panel-2);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 6px 4px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }

    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    div[data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14151A 0%, #0C0D11 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-title {
        color: #fff;
        font-weight: 800;
        font-size: 18px;
        margin: 4px 0 2px 0;
    }
    .sidebar-sub {
        color: var(--text-soft);
        font-size: 12.5px;
        margin-bottom: 14px;
    }

    .contact-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--panel-2);
        border: 1px solid rgba(255,255,255,0.06);
        border-left: 4px solid var(--danger);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: all 0.15s ease;
    }
    .contact-card:hover {
        border-left-color: var(--warning);
        background: #23262E;
    }
    .contact-name {
        color: #E9EAF0;
        font-size: 13.5px;
        font-weight: 600;
    }
    .contact-number {
        color: var(--warning);
        font-weight: 800;
        font-size: 15px;
        font-family: 'Courier New', monospace;
    }

    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(46, 204, 113, 0.12);
        color: var(--safe);
        border: 1px solid rgba(46, 204, 113, 0.35);
        padding: 5px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }
    .status-chip-off {
        background: rgba(230, 57, 70, 0.12);
        color: var(--danger);
        border-color: rgba(230, 57, 70, 0.35);
    }

    .footer-note {
        text-align: center;
        color: #6B6E78;
        font-size: 11.5px;
        margin-top: 18px;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# STATE AWAL
# ============================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Halo! Saya **SiagaBot** 🚨.\n\nSaya siap memberikan panduan keselamatan darurat, persiapan mitigasi, dan langkah evakuasi. Apa yang bisa saya bantu hari ini?\n\n*Contoh: 'Apa yang harus ada di dalam tas siaga bencana?'*")
    ]
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.image("https://cdn-icons-png.flaticon.com/512/3253/3253245.png", width=48)
    with col_b:
        st.markdown('<div class="sidebar-title">SiagaBot</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">Asisten Mitigasi Bencana</div>', unsafe_allow_html=True)

    api_key = st.text_input("🔑 Google API Key", type="password", help="Dapatkan di Google AI Studio")

    if api_key:
        st.markdown('<span class="status-chip">● Terhubung — Siap Digunakan</span>', unsafe_allow_html=True)
        os.environ["GOOGLE_API_KEY"] = api_key
    else:
        st.markdown('<span class="status-chip status-chip-off">● Belum Terhubung</span>', unsafe_allow_html=True)
        st.info("Masukkan API Key untuk mengaktifkan SiagaBot.")
        st.stop()

    st.divider()
    st.markdown('<div class="section-label">📞 Kontak Darurat</div>', unsafe_allow_html=True)

    kontak_darurat = [
        ("Panggilan Darurat", "112"),
        ("Ambulans / Kemenkes", "119"),
        ("Basarnas (SAR)", "115"),
        ("BNPB", "117"),
        ("Pemadam Kebakaran", "113"),
        ("Polisi", "110"),
    ]
    for nama, nomor in kontak_darurat:
        st.markdown(f"""
        <div class="contact-card">
            <span class="contact-name">{nama}</span>
            <span class="contact-number">{nomor}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Bersihkan Riwayat Chat", use_container_width=True):
        st.session_state.chat_history = [
            AIMessage(content="Riwayat dibersihkan. Ada yang bisa saya bantu lagi? 🚨")
        ]
        st.rerun()

    st.markdown('<div class="footer-note">© 2026 SiagaBot — AI Agent Project</div>', unsafe_allow_html=True)

# ============================================================
# HERO / HEADER UTAMA
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge"><span class="pulse-dot"></span> Pusat Tanggap Darurat • Online 24/7</div>
    <div class="hero-title">🚨 SiagaBot: Asisten Mitigasi Anda</div>
    <p class="hero-sub">Tanyakan panduan keselamatan, persiapan tas siaga bencana, atau rute evakuasi.
    Saya di sini untuk membantu Anda dengan cepat, tenang, dan akurat.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# QUICK TOPIC CHIPS (interaktif)
# ============================================================
st.markdown('<div class="section-label">⚡ Topik Cepat</div>', unsafe_allow_html=True)

quick_topics = [
    ("🏚️", "Gempa Bumi", "Apa langkah keselamatan yang harus saya lakukan saat terjadi gempa bumi?"),
    ("🌊", "Banjir", "Bagaimana cara evakuasi yang aman saat terjadi banjir besar?"),
    ("🔥", "Kebakaran", "Apa yang harus saya lakukan jika terjadi kebakaran di rumah?"),
    ("🎒", "Tas Siaga", "Apa saja isi tas siaga bencana yang wajib saya siapkan?"),
    ("🏥", "P3K Dasar", "Bagaimana cara memberikan pertolongan pertama dasar pada korban luka?"),
    ("🏃", "Rute Evakuasi", "Bagaimana cara menyusun rute evakuasi keluarga yang aman?"),
]

cols = st.columns(6)
for col, (emoji, label, query) in zip(cols, quick_topics):
    with col:
        if st.button(f"{emoji}\n{label}", key=f"topic_{label}", use_container_width=True):
            st.session_state.pending_query = query

# ============================================================
# AREA CHAT
# ============================================================
st.markdown('<div class="section-label">💬 Konsultasi</div>', unsafe_allow_html=True)

# --- INISIALISASI MODEL & PROMPT ---
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

prompt = ChatPromptTemplate.from_messages([
    ("system", """Kamu adalah SiagaBot, asisten virtual tanggap darurat dan mitigasi bencana di Indonesia. 
    Karaktermu: Tenang, profesional, cepat tanggap, empati, dan sangat instruktif.
    Aturan Format Jawaban:
    1. Selalu berikan struktur yang sangat rapi dan mudah dibaca (scannable).
    2. Gunakan **Markdown Bold** untuk poin krusial.
    3. Gunakan Bullet Points (-) atau Numbering (1, 2, 3) untuk instruksi langkah demi langkah.
    4. Sertakan emoji yang relevan (seperti ⚠️, 🎒, 🏥, 🏃) agar respons tidak kaku.
    Fokus utama: Panduan keselamatan gempa, banjir, kebakaran, P3K dasar, dan mitigasi pasca-bencana."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()

# --- RENDER RIWAYAT PERCAKAPAN ---
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(msg.content)
    else:
        with st.chat_message("assistant", avatar="🚨"):
            st.markdown(msg.content)

# --- INPUT USER (dari chat box ATAU dari tombol topik cepat) ---
typed_query = st.chat_input("Ketik pertanyaan darurat/mitigasi di sini...")
user_query = st.session_state.pending_query or typed_query
st.session_state.pending_query = None

if user_query:
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="🚨"):
        with st.spinner("🔎 Mengumpulkan panduan keselamatan..."):
            response = chain.invoke({
                "input": user_query,
                "chat_history": st.session_state.chat_history
            })
            st.markdown(response)

    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=response))