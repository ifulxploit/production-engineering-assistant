# core/formatter.py
"""
Modul ini menyediakan utility functions untuk memformat dan memproses respons AI.
Bertugas memastikan respons selalu rapi, terstruktur, dan siap untuk ditampilkan di UI.
"""
import re
"""
Modul ini menyediakan utility functions untuk memformat dan memproses respons AI.
"""
import re
from typing import List, Dict, Tuple

# TAMBAHKAN BARIS INI:
from utils.logger import get_logger
logger = get_logger(__name__)
from typing import List, Dict, Tuple

def extract_references(response_text: str) -> Tuple[str, List[str]]:
    """
    Mengekstrak bagian References dari respons AI.
    
    Args:
        response_text (str): Respons lengkap dari AI.
        
    Returns:
        Tuple[str, List[str]]: 
            - response_without_refs: Respons tanpa bagian References
            - references: Daftar referensi yang diekstrak
    """
    # Cari bagian References menggunakan regex
    ref_pattern = r'\*\*References\*\*\s*(.*?)(?=\n\n\*\*|$)'
    match = re.search(ref_pattern, response_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        references_text = match.group(1).strip()
        # Pisahkan menjadi list berdasarkan bullet points atau baris baru
        references = [ref.strip() for ref in re.split(r'[\n•\-]', references_text) if ref.strip()]
        
        # Hapus bagian References dari respons asli
        response_without_refs = response_text[:match.start()].strip()
        
        return response_without_refs, references
    
    return response_text, []

def format_response_with_sources(response_text: str, sources: List[Dict]) -> str:
    """
    Memformat respons AI dengan menambahkan sumber referensi di bagian bawah.
    
    Args:
        response_text (str): Respons dari AI.
        sources (List[Dict]): Daftar sumber dengan metadata (filename, page, dll).
        
    Returns:
        str: Respons yang sudah diformat dengan sumber.
    """
    if not sources:
        return response_text
    
    # Tambahkan header Sources
    formatted = response_text + "\n\n---\n**📚 Sumber Referensi:**\n"
    
    for i, source in enumerate(sources, 1):
        filename = source.get('filename', 'Unknown')
        page = source.get('page', 'N/A')
        formatted += f"{i}. {filename} (halaman {page})\n"
    
    return formatted

def clean_response(response_text: str) -> str:
    """
    Membersihkan respons dari artefak yang tidak diinginkan.
    
    Args:
        response_text (str): Respons mentah dari AI.
        
    Returns:
        str: Respons yang sudah dibersihkan.
    """
    # Hapus multiple blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', response_text)
    
    # Hapus trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned

def extract_section(response_text: str, section_name: str) -> str:
    """
    Mengekstrak bagian tertentu dari respons AI (misal: "Possible Causes").
    
    Args:
        response_text (str): Respons lengkap dari AI.
        section_name (str): Nama section yang ingin diekstrak.
        
    Returns:
        str: Konten dari section yang diekstrak, atau string kosong jika tidak ditemukan.
    """
    pattern = rf'\*\*{section_name}\*\*\s*(.*?)(?=\n\n\*\*|$)'
    match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    return ""

def validate_response_format(response_text: str) -> bool:
    """
    Memvalidasi apakah respons AI mengikuti format profesional yang ditentukan.
    
    Args:
        response_text (str): Respons dari AI.
        
    Returns:
        bool: True jika format valid, False jika tidak.
    """
    required_sections = [
        "Problem Summary",
        "Possible Causes",
        "Engineering Explanation",
        "Recommended Inspection",
        "Recommended Action"
    ]
    
    for section in required_sections:
        if f"**{section}**" not in response_text:
            return False
    
    return True