# src/agents/tools/file_system_tools.py

import os
import shutil
# Import our new ctypes-based search function
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
            # Use the new search function
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