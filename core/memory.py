# core/memory.py
"""
Modul ini mengelola memori percakapan (Conversation Memory).
Bertugas menjembatani riwayat chat dari UI (Streamlit) dengan format yang dipahami oleh LangChain LLM.
"""
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

def format_chat_history(session_history: List[Dict[str, str]]) -> List[BaseMessage]:
    """
    Mengonversi riwayat chat dari format dictionary Streamlit 
    menjadi format pesan LangChain (HumanMessage, AIMessage).
    
    Args:
        session_history (List[Dict]): Riwayat chat dari st.session_state.messages.
        
    Returns:
        List[BaseMessage]: Daftar pesan dalam format LangChain.
    """
    langchain_messages = []
    
    # Iterasi melalui setiap pesan di riwayat
    for msg in session_history:
        role = msg.get("role")
        content = msg.get("content")
        
        # Konversi ke objek pesan LangChain yang sesuai
        if role == "user":
            langchain_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            langchain_messages.append(AIMessage(content=content))
            
    return langchain_messages