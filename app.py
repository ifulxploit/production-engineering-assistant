# app.py
import streamlit as st
import os
import base64

# ==========================================
# INISIALISASI LOGGER GLOBAL
# ==========================================
from utils.logger import app_logger
from utils.helpers import get_sample_questions
from core.chatbot import get_response
from core.rag import build_vector_db
from config.settings import settings

app_logger.info("=" * 60)
app_logger.info("🚀 Production Engineering Assistant (PEA) - Starting Up")
app_logger.info("=" * 60)

# ==========================================
# AUTO-BUILD VECTOR DB
# ==========================================
if not os.path.exists(settings.VECTOR_DB_DIR) or not os.listdir(settings.VECTOR_DB_DIR):
    try:
        with st.spinner("🏗️ Membangun Knowledge Base..."):
            build_vector_db()
    except:
        build_vector_db()

# ==========================================
# HELPER FUNCTION
# ==========================================
def get_image_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="PEA | Saiful Miqdar",
    page_icon="🛢️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Background & Font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background - Deep Slate */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
        background-color: transparent;
    }

    /* ==========================================
       SIDEBAR - DARK PURPLE THEME
       ========================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    /* Sidebar Text Colors */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1 !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        background-color: transparent !important;
    }

    /* Reset Button - Purple Gradient */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 12px rgba(139, 92, 246, 0.35) !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #a855f7 0%, #c084fc 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.5) !important;
    }

    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3) !important;
    }

    /* ==========================================
       HEADER & TITLE
       ========================================== */
    .header-title {
        background: linear-gradient(135deg, #38bdf8 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
    }

    /* ==========================================
       WELCOME CARD - PURPLE/CYAN GRADIENT
       ========================================== */
    .welcome-card {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }

    /* ==========================================
       SUGGESTION CHIPS - CYAN ACCENT
       ========================================== */
    div[data-testid="stVerticalBlock"] div[data-testid="stElementContainer"] button[kind="secondary"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
        white-space: normal !important;
        height: auto !important;
        line-height: 1.5 !important;
        text-align: left !important;
        margin-bottom: 10px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    div[data-testid="stVerticalBlock"] div[data-testid="stElementContainer"] button[kind="secondary"]:hover {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
        border-color: #38bdf8 !important;
        color: #7dd3fc !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 16px rgba(56, 189, 248, 0.3) !important;
    }

    /* Category Header */
    .category-header {
        color: #a855f7 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        padding-left: 12px !important;
        border-left: 3px solid #8b5cf6 !important;
    }

    /* ==========================================
       CHAT INPUT - DARK THEME WITH CYAN GLOW
       ========================================== */
    .stChatInput > div {
        background-color: #1e293b !important;
        border-radius: 16px !important;
        border: 2px solid #334155 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        padding: 8px 12px !important;
    }

    .stChatInput > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 24px rgba(56, 189, 248, 0.35) !important;
    }

    .stChatInput textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        color: #f8fafc !important;
        border: none !important;
        background-color: transparent !important;
        padding: 8px 10px !important;
        resize: none !important;
    }

    .stChatInput textarea::placeholder {
        color: #64748b !important;
        font-style: italic !important;
        font-weight: 500 !important;
    }

    .stChatInput button {
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        border: none !important;
        min-width: 40px !important;
        min-height: 40px !important;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.3) !important;
    }

    .stChatInput button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        transform: scale(1.08) !important;
        box-shadow: 0 4px 16px rgba(56, 189, 248, 0.5) !important;
    }

    /* ==========================================
       CHAT MESSAGES - DARK THEME
       ========================================== */
    .stChatMessage {
        padding: 10px 0 !important;
    }
    
    /* User Message */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(56, 189, 248, 0.1) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border-left: 3px solid #38bdf8 !important;
    }
    
    /* Assistant Message */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(139, 92, 246, 0.1) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border-left: 3px solid #8b5cf6 !important;
    }

    /* ==========================================
       SPINNER & LOADING
       ========================================== */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }

    /* ==========================================
       SCROLLBAR - DARK THEME
       ========================================== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR
# ==========================================
with st.sidebar:
    profile_path = "assets/profile.png"
    if os.path.exists(profile_path):
        img_base64 = get_image_as_base64(profile_path)
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 24px; margin-top: 20px; padding: 20px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(56, 189, 248, 0.1) 100%); border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.2);">
            <img src="data:image/png;base64,{img_base64}" width="120" style="border-radius: 12px; object-fit: cover; border: 3px solid #8b5cf6; box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);">
            <h2 style="color: #f8fafc; margin: 12px 0 4px 0; font-weight: 800; font-size: 20px;">Saiful Miqdar</h2>
            <p style="color: #38bdf8; font-size: 14px; margin: 0; font-weight: 600;">Production Engineer</p>
            <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 0 0;">S1 Teknik Perminyakan (2025)</p>
            <p style="color: #64748b; font-size: 11px; margin: 2px 0 0 0;">Universitas Proklamasi 45</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Foto profil tidak ditemukan.")
        st.markdown("<h2 style='text-align: center; color: #f8fafc;'>Saiful Miqdar</h2>", unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("### 🚀 About This Project")
    st.markdown("""
    <div style="color: #cbd5e1; font-size: 13px; line-height: 1.6; text-align: justify;">
        Aplikasi ini dikembangkan sebagai <b style="color: #a855f7;">Final Project</b> untuk kelas 
        <b style="color: #38bdf8;">Maju Bareng AI - Hacktiv8</b>.
        <br><br>
        <b style="color: #38bdf8;">🎯 Tujuan:</b><br>
        Menjadi <i>Decision Support Assistant</i> bagi mahasiswa dan engineer 
        dalam mendiagnosis masalah produksi sumur secara cepat dan berbasis data.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    if st.button("🗑️ Reset Chat Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    # ==========================================
    # ==========================================
    # SOCIAL MEDIA LINKS
    # ==========================================
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <p style="color: #94a3b8; font-size: 11px; margin-bottom: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
            Connect with Me
        </p>
    </div>
    """, unsafe_allow_html=True)

    # GitHub Button
    st.markdown("""
    <a href="https://github.com/ifulxploit" target="_blank" style="text-decoration: none; display: block; margin-bottom: 8px;">
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(56, 189, 248, 0.15) 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 8px; padding: 10px 16px; text-align: center; transition: all 0.3s ease;">
            <span style="color: #8b5cf6; font-weight: 600; font-size: 13px;">GitHub → @ifulxploit</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

    # LinkedIn Button
    st.markdown("""
    <a href="https://www.linkedin.com/in/saiful-miqdar-7050511b1/" target="_blank" style="text-decoration: none; display: block; margin-bottom: 8px;">
        <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 10px 16px; text-align: center; transition: all 0.3s ease;">
            <span style="color: #38bdf8; font-weight: 600; font-size: 13px;">LinkedIn → Saiful Miqdar</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

    # Instagram Button
    st.markdown("""
    <a href="https://www.instagram.com/saiful_miqdar" target="_blank" style="text-decoration: none; display: block; margin-bottom: 8px;">
        <div style="background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 8px; padding: 10px 16px; text-align: center; transition: all 0.3s ease;">
            <span style="color: #a855f7; font-weight: 600; font-size: 13px;">Instagram → @saiful_miqdar</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

    # CSS untuk hover effect
    st.markdown("""
    <style>
        a[href*="github.com"] > div:hover {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(56, 189, 248, 0.25) 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
        }
        
        a[href*="linkedin.com"] > div:hover {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
        }
        
        a[href*="instagram.com"] > div:hover {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.25) 0%, rgba(236, 72, 153, 0.25) 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Tambahkan CSS untuk hover effect
    st.markdown("""
    <style>
        /* Social Media Icons Hover Effect */
        a:hover > div {
            transform: translateY(-3px) scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 11px; margin-top: 20px;">
        Powered by <span style="color: #8b5cf6;">Gemini 2.5 Flash</span> & <span style="color: #38bdf8;">FAISS</span><br>
        © 2026 Saiful Miqdar
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MAIN AREA: HEADER
# ==========================================
st.markdown("""
<div style="text-align: center; margin-bottom: 32px; padding: 24px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(56, 189, 248, 0.1) 100%); border-radius: 20px; border: 1px solid rgba(139, 92, 246, 0.2);">
    <h1 class="header-title" style="margin-bottom: 8px; font-size: 36px;">
        🛢️ Production Engineering Assistant
    </h1>
    <p style="color: #94a3b8; font-size: 15px; margin: 0;">
        AI-Powered Troubleshooting & Decision Support System
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ==========================================
# 5. HANDLE PENDING QUESTION
# ==========================================
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.spinner("🩺 Menganalisis masalah..."):
        response = get_response(st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ==========================================
# 6. RENDER CHAT HISTORY
# ==========================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 7. WELCOME SCREEN
# ==========================================
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div style="text-align: center;">
            <h3 style="color: #f8fafc; margin-bottom: 8px; font-size: 22px; font-weight: 700;">Selamat datang, Engineer! 👋</h3>
            <p style="color: #94a3b8; font-size: 14px; margin: 0;">
                Pilih pertanyaan di bawah atau ketik masalah Anda sendiri
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load sample questions
    categories = get_sample_questions()
    
    if categories:
        # Tampilkan HANYA 2 kategori pertama
        for cat in categories[:2]:
            category_name = cat.get("category", "General")
            icon = cat.get("icon", "💡")
            questions = cat.get("questions", [])[:3]
            
            # Category header
            st.markdown(f"""
            <div class="category-header">
                {icon} {category_name}
            </div>
            """, unsafe_allow_html=True)
            
            # Render chips
            for i, question in enumerate(questions):
                button_key = f"chip_{category_name}_{i}"
                
                if st.button(
                    question, 
                    key=button_key,
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.pending_question = question
                    st.rerun()
    else:
        st.info("💡 Ketik pertanyaan Anda di bawah untuk memulai.")

# ==========================================
# 8. CHAT INPUT
# ==========================================
if prompt := st.chat_input("Ketik masalah produksi sumur Anda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🩺 Menganalisis masalah..."):
            response = get_response(st.session_state.messages)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})