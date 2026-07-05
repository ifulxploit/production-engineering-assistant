# config/settings.py
import os
import streamlit as st
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.logger import get_logger
logger = get_logger(__name__)

# Load environment variables dari file .env (untuk pengembangan lokal)
load_dotenv()

class Settings(BaseSettings):
    """
    Kelas konfigurasi utama untuk Production Engineering Assistant.
    Menggunakan Pydantic v2 untuk validasi tipe data secara otomatis.
    """
    
    # 1. API Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # 2. LLM Configuration (Gemini)
    LLM_MODEL_NAME: str = "gemini-2.5-flash" 
    LLM_TEMPERATURE: float = 0.2  # Diset rendah agar jawaban faktual dan presisi
    LLM_MAX_OUTPUT_TOKENS: int = 2048
    
    # 3. RAG & Embedding Configuration
    CHUNK_SIZE: int = 1000       
    CHUNK_OVERLAP: int = 200     
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2" 
    
    # 4. Directory Paths
    KNOWLEDGE_PDF_DIR: str = "knowledge/pdf"
    VECTOR_DB_DIR: str = "knowledge/vector_db"
    
    # Konfigurasi Pydantic v2
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Inisialisasi objek settings global
settings = Settings()

# ==========================================
# STREAMLIT CLOUD SECRETS FALLBACK
# ==========================================
# Jika GOOGLE_API_KEY tidak ditemukan di .env (misalnya saat di-deploy di Streamlit Cloud),
# sistem akan otomatis mencoba mengambilnya dari st.secrets.
if not settings.GOOGLE_API_KEY:
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            settings.GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
            logger.info("✅ GOOGLE_API_KEY berhasil dimuat dari Streamlit Secrets.")
    except Exception:
        pass

# Validasi Keamanan Final
if not settings.GOOGLE_API_KEY:
    logger.critical("❌ CRITICAL ERROR: GOOGLE_API_KEY tidak ditemukan di .env maupun Streamlit Secrets.")
    raise ValueError("CRITICAL ERROR: GOOGLE_API_KEY tidak ditemukan. Mohon periksa konfigurasi Anda.")