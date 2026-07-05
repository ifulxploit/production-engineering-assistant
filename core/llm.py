# core/llm.py
"""
Modul ini bertanggung jawab untuk menginisialisasi dan mengelola koneksi 
ke Large Language Model (Gemini API) menggunakan LangChain.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings
from utils.logger import get_logger

# Konfigurasi logging dasar untuk modul ini
logger = get_logger(__name__)

def get_llm() -> ChatGoogleGenerativeAI:
    """
    Factory function untuk menginisialisasi dan mengembalikan instance model LLM (Gemini).
    Menggunakan parameter konfigurasi dari config.settings.
    
    Returns:
        ChatGoogleGenerativeAI: Instance model LLM yang siap digunakan.
    """
    try:
        logger.info(f"Menginisialisasi LLM dengan model: {settings.LLM_MODEL_NAME}")
        
        # Inisialisasi model Gemini dengan parameter dari settings
        llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL_NAME,
            temperature=settings.LLM_TEMPERATURE,
            max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS,
            google_api_key=settings.GOOGLE_API_KEY,
        )
        
        logger.info("✅ LLM (Gemini) berhasil diinisialisasi dengan sukses.")
        return llm
        
    except Exception as e:
        logger.error(f"❌ GAGAL KRITIS: Tidak dapat menginisialisasi LLM. Error: {e}")
        raise RuntimeError(f"Inisialisasi LLM gagal: {e}")

# ==============================================================================
# BLOK TESTING (Health Check)
# Blok ini hanya akan berjalan jika file ini dieksekusi secara langsung.
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🩺 SEDANG MELAKUKAN HEALTH CHECK KONEKSI GEMINI API...")
    print("="*50 + "\n")
    
    try:
        # 1. Panggil fungsi untuk mendapatkan instance LLM
        test_llm = get_llm()
        
        # 2. Kirim prompt sederhana untuk menguji respons
        test_prompt = "Sebutkan satu masalah umum pada sumur minyak dan jawab dalam satu kalimat bahasa Indonesia."
        response = test_llm.invoke(test_prompt)
        
        # 3. Cetak hasil
        print(f"📥 Prompt Uji: {test_prompt}")
        print(f"📤 Respons AI: {response.content}")
        print("\n✅ SUKSES! Koneksi ke Gemini API berjalan dengan sempurna.")
        
    except Exception as e:
        print(f"\n❌ GAGAL! Terjadi error saat mencoba berkomunikasi dengan Gemini API.")
        print(f"Detail Error: {e}")
        print("\n💡 Diagnosa: Periksa kembali GOOGLE_API_KEY di file .env Anda, atau pastikan koneksi internet stabil.")