"""
Application-wide constants.
"""

APP_NAME = "Enterprise AI Assistant"
APP_VERSION = "1.0.0"

DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_TEMPERATURE = 0.3
DEFAULT_TOP_K = 4
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

SUPPORTED_FILE_TYPES = [
    "pdf",
    "docx",
    "txt",
    "csv",
]