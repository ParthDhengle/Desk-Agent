# src/agents/tools/file_system_tools.py

import os
import shutil
import subprocess
from src.search.everything_search import search_everything

def create_file(target: str) -> str:
    """Creates an empty file."""
    try:
        parent_dir = os.path.dirname(target)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(target, 'w') as f:
            pass
        return f"✅ Successfully created file: {target}"
    except IOError as e:
        return f"❌ Error creating file: {e}"

def delete_file(target: str) -> str:
    """Deletes the specified file, using Everything to find it if needed."""
    try:
        if not os.path.exists(target):
            print(f"File '{target}' not found directly, searching with Everything...")
            results = search_everything(target, limit=1)
            if not results:
                return f"❌ Error: File '{target}' not found."
            file_to_delete = results[0]
        else:
            file_to_delete = target
        os.remove(file_to_delete)
        return f"✅ Successfully deleted file: {file_to_delete}"
    except Exception as e:
        return f"❌ An unexpected error occurred while deleting: {e}"

# --- NEW FUNCTION ---
def open_application(target: str) -> str:
    """Opens an application by name or opens a URL in the default web browser."""
    target_lower = target.lower()
    try:
        # Handle common web URLs
        if target_lower.startswith(('http', 'www.')) or '.com' in target_lower:
            # For convenience, let's treat "youtube" as a URL
            if target_lower == "youtube":
                target = "https://www.youtube.com"
            print(f"Opening URL: {target}")
            # Use startfile on Windows, which is like double-clicking the URL
            os.startfile(target)
            return f"✅ Opened {target} in your web browser."
        
        # Handle local applications
        else:
            print(f"Attempting to open application: {target}")
            # Append .exe for common cases if not present
            if not target_lower.endswith('.exe'):
                target += ".exe"
            # Use subprocess.Popen for non-blocking launch
            subprocess.Popen(target, shell=True)
            return f"✅ Started application: {target}"
            
    except FileNotFoundError:
        return f"❌ Error: Application '{target}' not found. Make sure it's in your system's PATH."
    except Exception as e:
        return f"❌ An unexpected error occurred while trying to open '{target}': {e}"