# utils/helpers.py
"""
Modul ini menyediakan utility functions umum yang digunakan di seluruh aplikasi.
Fungsi-fungsi ini bersifat reusable dan tidak spesifik pada satu modul.
"""
import os
import json
from typing import List, Dict, Any
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Memuat file JSON dan mengembalikannya sebagai dictionary.
    
    Args:
        file_path (str): Path ke file JSON.
        
    Returns:
        Dict[str, Any]: Konten JSON sebagai dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File tidak ditemukan: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON di {file_path}: {e}")
        return {}

def get_sample_questions() -> List[Dict]:
    """
    Memuat daftar pertanyaan contoh dari data/sample_questions.json.
    
    Returns:
        List[Dict]: Daftar kategori dan pertanyaan.
    """
    data = load_json_file("data/sample_questions.json")
    return data.get("categories", [])

def format_timestamp(dt: datetime = None) -> str:
    """
    Memformat datetime menjadi string yang mudah dibaca.
    
    Args:
        dt (datetime, optional): Datetime object. Jika None, menggunakan waktu sekarang.
        
    Returns:
        str: Timestamp dalam format "YYYY-MM-DD HH:MM:SS".
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_file_exists(file_path: str) -> bool:
    """
    Memvalidasi apakah file ada di path yang diberikan.
    
    Args:
        file_path (str): Path ke file.
        
    Returns:
        bool: True jika file ada, False jika tidak.
    """
    return os.path.exists(file_path)

def get_file_size_mb(file_path: str) -> float:
    """
    Mendapatkan ukuran file dalam megabytes.
    
    Args:
        file_path (str): Path ke file.
        
    Returns:
        float: Ukuran file dalam MB.
    """
    if not os.path.exists(file_path):
        return 0.0
    
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Memotong teks jika melebihi panjang maksimum.
    
    Args:
        text (str): Teks asli.
        max_length (int): Panjang maksimum.
        
    Returns:
        str: Teks yang sudah dipotong (dengan ellipsis jika perlu).
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def convert_pressure_unit(value: float, from_unit: str, to_unit: str) -> float:
    """
    Konversi satuan tekanan (psi, bar, kPa, MPa).
    
    Args:
        value (float): Nilai tekanan.
        from_unit (str): Satuan asal (psi, bar, kPa, MPa).
        to_unit (str): Satuan tujuan.
        
    Returns:
        float: Nilai tekanan setelah konversi.
    """
    # Konversi ke psi sebagai base unit
    to_psi = {
        'psi': 1.0,
        'bar': 14.5038,
        'kPa': 0.145038,
        'MPa': 145.038
    }
    
    if from_unit not in to_psi or to_unit not in to_psi:
        raise ValueError(f"Satuan tidak didukung: {from_unit} atau {to_unit}")
    
    # Konversi: from_unit -> psi -> to_unit
    value_in_psi = value * to_psi[from_unit]
    return value_in_psi / to_psi[to_unit]

def convert_temperature_unit(value: float, from_unit: str, to_unit: str) -> float:
    """
    Konversi satuan temperatur (C, F, K).
    
    Args:
        value (float): Nilai temperatur.
        from_unit (str): Satuan asal (C, F, K).
        to_unit (str): Satuan tujuan.
        
    Returns:
        float: Nilai temperatur setelah konversi.
    """
    # Konversi ke Celsius sebagai base unit
    if from_unit == 'C':
        celsius = value
    elif from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    else:
        raise ValueError(f"Satuan tidak didukung: {from_unit}")
    
    # Konversi dari Celsius ke target
    if to_unit == 'C':
        return celsius
    elif to_unit == 'F':
        return celsius * 9/5 + 32
    elif to_unit == 'K':
        return celsius + 273.15
    else:
        raise ValueError(f"Satuan tidak didukung: {to_unit}")

def sanitize_filename(filename: str) -> str:
    """
    Membersihkan nama file dari karakter yang tidak valid.
    
    Args:
        filename (str): Nama file asli.
        
    Returns:
        str: Nama file yang sudah dibersihkan.
    """
    # Hapus karakter yang tidak valid untuk nama file
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()