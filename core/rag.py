# core/rag.py
"""
Modul ini mengelola proses Retrieval-Augmented Generation (RAG) Knowledge Base.
Bertanggung jawab atas: Loading PDF, Chunking, Embedding, dan menyimpan ke FAISS.
"""
import os
from utils.logger import get_logger
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config.settings import settings

logger = get_logger(__name__)

def load_documents():
    """
    Langkah 1: Memuat semua file PDF dari direktori knowledge/pdf.
    """
    logger.info(f"Memuat dokumen PDF dari: {settings.KNOWLEDGE_PDF_DIR}")
    loader = PyPDFDirectoryLoader(settings.KNOWLEDGE_PDF_DIR)
    documents = loader.load()
    logger.info(f"Berhasil memuat {len(documents)} halaman dari PDF.")
    return documents

def split_documents(documents):
    """
    Langkah 2: Memecah dokumen menjadi chunk-chunk teks yang lebih kecil.
    """
    logger.info(f"Melakukan chunking (Size: {settings.CHUNK_SIZE}, Overlap: {settings.CHUNK_OVERLAP})")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Dokumen berhasil dipecah menjadi {len(chunks)} chunks.")
    return chunks

def get_embedding_model():
    """
    Langkah 3: Menginisialisasi model embedding Sentence Transformers.
    """
    logger.info(f"Memuat model embedding: {settings.EMBEDDING_MODEL_NAME}")
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'}, # Memastikan berjalan di CPU
        encode_kwargs={'normalize_embeddings': True} # Normalisasi untuk performa FAISS yang lebih baik
    )
    return embeddings

def build_vector_db():
    """
    Fungsi Utama (Pipeline): Menggabungkan seluruh proses Ingestion dan menyimpannya ke FAISS.
    """
    try:
        # 1. Load PDF
        documents = load_documents()
        if not documents:
            logger.warning("⚠️ Tidak ada dokumen PDF yang ditemukan di folder knowledge/pdf. Proses dibatalkan.")
            return False
            
        # 2. Chunking
        chunks = split_documents(documents)
        
        # 3. Embedding Model
        embeddings = get_embedding_model()
        
        # 4. Create FAISS Vector Store
        logger.info("Membuat FAISS Vector Store dari chunks... (Ini mungkin memakan waktu beberapa saat)")
        vector_db = FAISS.from_documents(chunks, embeddings)
        
        # 5. Save to disk
        os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
        logger.info(f"Menyimpan FAISS index ke: {settings.VECTOR_DB_DIR}")
        vector_db.save_local(settings.VECTOR_DB_DIR)
        
        logger.info("✅ SUKSES! Vector Database (FAISS) berhasil dibangun dan disimpan.")
        return True
        
    except Exception as e:
        logger.error(f"❌ GAGAL membangun Vector Database: {e}")
        return False

# ==============================================================================
# BLOK EKSEKUSI INGESTION (Health Check & Build DB)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏗️ MEMULAI PROSES PEMBANGUNAN KNOWLEDGE BASE (RAG)...")
    print("="*60 + "\n")
    build_vector_db()