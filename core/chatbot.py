# core/chatbot.py
"""
Modul ini mengelola logika percakapan RAG (Retrieval-Augmented Generation).
Menggabungkan LLM, Memory, dan Retriever untuk menghasilkan jawaban berbasis dokumen.
"""
from langchain_core.messages import SystemMessage, HumanMessage
from core.llm import get_llm
from core.memory import format_chat_history
from core.retriever import get_retriever
from config.constants import SYSTEM_PROMPT
from utils.logger import get_logger

logger = get_logger(__name__)

def get_response(session_history: list) -> str:
    """
    Memproses pertanyaan user dengan mengambil konteks dari PDF (RAG), 
    menggabungkannya dengan memori percakapan, lalu memintanya ke LLM.
    """
    try:
        # 1. Ekstrak pertanyaan terbaru user dari history
        user_input = session_history[-1]["content"]
        
        # 2. Panggil Retriever untuk mencari informasi relevan di PDF
        logger.info(f"Mencari konteks di Knowledge Base untuk: '{user_input}'")
        retriever = get_retriever()
        retrieved_docs = retriever.invoke(user_input)
        
        # 3. Gabungkan chunks yang ditemukan menjadi satu string teks (Context)
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        
        # 4. Dapatkan instance LLM
        llm = get_llm()
        
        # 5. Format riwayat chat menjadi objek pesan LangChain
        history_messages = format_chat_history(session_history[:-1]) # Exclude pesan terakhir (user_input) karena akan dimasukkan manual
        
        # 6. SUSUN PROMPT FINAL (The Magic Happens Here)
        # Kita suntikkan Konteks PDF langsung ke dalam System Prompt
        system_content = f"""{SYSTEM_PROMPT}

--- KNOWLEDGE BASE CONTEXT ---
Gunakan informasi di bawah ini sebagai rujukan utama Anda untuk menjawab. Jika informasinya tidak ada di bawah ini, gunakan pengetahuan umum Anda namun nyatakan secara eksplisit.

{context}
----------------------------"""
        
        # Susun urutan pesan: [System + Context] -> [Riwayat Chat] -> [Pertanyaan User Terbaru]
        messages = [SystemMessage(content=system_content)] + history_messages + [HumanMessage(content=user_input)]
        
        # 7. Invoke LLM dan kembalikan responsnya
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        logger.error(f"Error fatal pada RAG Chain: {e}")
        return "Maaf, terjadi kesalahan internal saat memproses dokumen Knowledge Base. Silakan coba lagi."