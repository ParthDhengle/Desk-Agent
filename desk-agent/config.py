# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# --- Model Configuration ---
INTENT_MODEL = "ollama/phi3:3.8b"

# --- SDK/External Tool Paths ---
# Add the full path to your Everything64.dll file here.
EVERYTHING_DLL_PATH = r"C:\Users\Parth Dhengle\Desktop\Projects\Gen Ai\Desk-agent\desk-agent\src\search\everything sdk\dll\Everything64.dll"