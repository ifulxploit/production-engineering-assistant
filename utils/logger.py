# utils/logger.py
"""
Modul ini menyediakan konfigurasi logging terpusat untuk seluruh aplikasi.
Menggunakan logging terpusat memastikan konsistensi format dan level log di semua modul.
"""
import logging
import sys
from typing import Optional

def setup_logger(
    name: str = "PEA",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Menginisialisasi dan mengkonfigurasi logger untuk aplikasi.
    
    Args:
        name (str): Nama logger (biasanya nama aplikasi).
        level (int): Level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file (str, optional): Path ke file log. Jika None, hanya log ke console.
        format_string (str, optional): Format string untuk log messages.
        
    Returns:
        logging.Logger: Logger yang sudah dikonfigurasi.
    """
    # Format default jika tidak diberikan
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Buat logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Hapus handlers yang sudah ada (untuk menghindari duplikasi)
    if logger.handlers:
        logger.handlers.clear()
    
    # Buat formatter
    formatter = logging.Formatter(format_string)
    
    # Console Handler (log ke terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler (log ke file) - jika log_file diberikan
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(module_name: str) -> logging.Logger:
    """
    Mendapatkan logger untuk modul tertentu.
    Ini adalah fungsi yang harus dipanggil di setiap modul untuk mendapatkan logger.
    
    Args:
        module_name (str): Nama modul (biasanya __name__).
        
    Returns:
        logging.Logger: Logger untuk modul tersebut.
    """
    return logging.getLogger(module_name)

# Inisialisasi logger global untuk aplikasi
# Panggil fungsi ini sekali di app.py atau entry point utama
app_logger = setup_logger(
    name="PEA",
    level=logging.INFO,
    log_file=None,  # Set ke "app.log" jika ingin log ke file
    format_string='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)