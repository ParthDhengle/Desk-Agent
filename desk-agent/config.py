# config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Model Configuration ---

# The model string that LiteLLM will use.
# For a local Ollama model, the format is "ollama/model-name".
# We are using Phi-3 as our fast intent parser.
INTENT_MODEL = "ollama/phi3:3.8b"