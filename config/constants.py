# config/constants.py
"""
Modul ini menyimpan konstanta aplikasi yang stabil (tidak sering berubah).
Untuk prompt template, lihat config/prompt.py
"""

# Import prompt dari prompt.py agar bisa diakses dari satu tempat
from config.prompt import SYSTEM_PROMPT, PROFESSIONAL_RESPONSE_FORMAT

# Anda bisa menambahkan konstanta lain di sini, misalnya:
# APP_VERSION = "1.0.0"
# SUPPORTED_FILE_TYPES = [".pdf"]
# MAX_CHAT_HISTORY = 50