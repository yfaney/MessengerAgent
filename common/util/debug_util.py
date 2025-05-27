import os


DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def is_debug_mode() -> bool:
    return DEBUG