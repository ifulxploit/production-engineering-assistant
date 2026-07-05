# core/retriever.py
"""
Modul ini bertindak sebagai 'Pustakawan' (Retriever).
Bertugas memuat Vector Database dari disk dan mencari informasi yang paling relevan 
berdasarkan pertanyaan user.
"""
import os
from utils.logger import get_logger
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import settings

logger = get_logger(__name__)

def get_retriever():
    """
    Memuat FAISS Vector Store dari disk dan mengembalikan objek Retriever.
    
    Returns:
        Retriever: Objek yang siap mencari dokumen relevan.
    """
    # Pastikan Vector DB sudah ada
    if not os.path.exists(settings.VECTOR_DB_DIR):
        logger.error(f"❌ Vector DB tidak ditemukan di {settings.VECTOR_DB_DIR}. Jalankan 'python -m core.rag' terlebih dahulu.")
        raise FileNotFoundError("Vector Database belum dibangun. Silakan jalankan script ingestion.")
        
    logger.info("Memuat FAISS Vector Store dari disk...")
    
    # Inisialisasi model embedding yang sama persis dengan saat pembuatan DB
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Load FAISS dari disk
    # allow_dangerous_deserialization=True REQUIRED untuk memuat file .pkl lokal dari FAISS
    vector_db = FAISS.load_local(
        settings.VECTOR_DB_DIR, 
        embeddings, 
        allow_dangerous_deserialization=True 
    )
    
    # Ubah Vector Store menjadi Retriever
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4} # Mengambil 4 chunks paling relevan dari PDF
    )
    
    logger.info("✅ Retriever (Pustakawan) berhasil diinisialisasi dan siap mencari data.")
    return retriever