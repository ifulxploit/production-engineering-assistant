# config/settings.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
# config/settings.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# TAMBAHKAN BARIS INI:
from utils.logger import get_logger
logger = get_logger(__name__)

# Load environment variables dari file .env
load_dotenv()

# Load environment variables dari file .env
load_dotenv()

class Settings(BaseSettings):
    """
    Kelas konfigurasi utama untuk Production Engineering Assistant.
    Menggunakan Pydantic untuk validasi tipe data secara otomatis.
    """
    
    # 1. API Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # 2. LLM Configuration (Gemini)
    # Menggunakan Gemini 2.5 Flash (Model tercepat dan paling efisien untuk RAG)
    LLM_MODEL_NAME: str = "gemini-2.5-flash" 
    LLM_TEMPERATURE: float = 0.2  # Diset rendah (0.0 - 0.3) agar jawaban faktual, presisi, dan tidak kreatif/berhalusinasi
    LLM_MAX_OUTPUT_TOKENS: int = 2048
    
    # 3. RAG & Embedding Configuration
    CHUNK_SIZE: int = 1000       # Ukuran chunk teks (karakter) untuk dipecah dari PDF
    CHUNK_OVERLAP: int = 200     # Overlap antar chunk agar konteks kalimat tidak terputus
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2" # Model embedding ringan, cepat, dan akurat
    
    # 4. Directory Paths
    KNOWLEDGE_PDF_DIR: str = "knowledge/pdf"
    VECTOR_DB_DIR: str = "knowledge/vector_db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Inisialisasi objek settings global
settings = Settings()

# Validasi Keamanan: Pastikan API Key berhasil dimuat
if not settings.GOOGLE_API_KEY:
    logger.critical("❌ CRITICAL ERROR: GOOGLE_API_KEY tidak ditemukan di file .env. Mohon periksa konfigurasi Anda.")
    raise ValueError("CRITICAL ERROR: GOOGLE_API_KEY tidak ditemukan di file .env. Mohon periksa konfigurasi Anda.")