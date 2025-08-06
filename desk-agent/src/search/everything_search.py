# src/search/everything_search.py

import ctypes
import os
from config import EVERYTHING_DLL_PATH

# --- Everything SDK Integration using ctypes ---

# Check if the DLL path from config exists
if not os.path.exists(EVERYTHING_DLL_PATH):
    raise FileNotFoundError(f"Everything DLL not found at path: {EVERYTHING_DLL_PATH}")

# Load the DLL from the path specified in config.py
try:
    everything_dll = ctypes.WinDLL(EVERYTHING_DLL_PATH)
except OSError as e:
    raise OSError(f"Failed to load Everything DLL. Ensure it is a valid 64-bit DLL. Error: {e}")


# Define function prototypes for type safety and clarity
everything_dll.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
everything_dll.Everything_SetRequestFlags.argtypes = [ctypes.c_uint]
everything_dll.Everything_SetSort.argtypes = [ctypes.c_uint]
everything_dll.Everything_QueryW.argtypes = [ctypes.c_bool]
everything_dll.Everything_GetNumResults.restype = ctypes.c_int
everything_dll.Everything_GetResultFullPathNameW.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int]


# Define helper constants
EVERYTHING_SORT_NAME_ASCENDING = 1
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002

def search_everything(query: str, limit: int = 10) -> list[str]:
    """
    Performs a search using the loaded Everything DLL.

    Args:
        query: The search term.
        limit: The maximum number of results to return.

    Returns:
        A list of full file paths matching the query.
    """
    everything_dll.Everything_SetSearchW(query)
    everything_dll.Everything_SetRequestFlags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH)
    everything_dll.Everything_SetSort(EVERYTHING_SORT_NAME_ASCENDING)
    
    # Execute the query
    everything_dll.Everything_QueryW(True)

    num_results = everything_dll.Everything_GetNumResults()
    # Respect the limit parameter
    results_to_fetch = min(num_results, limit)

    results = []
    for i in range(results_to_fetch):
        # Create a buffer to hold the full path
        buf = ctypes.create_unicode_buffer(260)
        everything_dll.Everything_GetResultFullPathNameW(i, buf, 260)
        results.append(buf.value)

    return results

# This block allows you to test this file directly by running `python src/search/everything_search.py`
if __name__ == '__main__':
    print("Testing Everything search...")
    search_query = "main.py"  # Change this to test a file you know exists
    found_files = search_everything(search_query)
    
    if found_files:
        print(f"Found {len(found_files)} result(s) for '{search_query}':")
        for file_path in found_files:
            print(file_path)
    else:
        print(f"No results found for '{search_query}'. Is the Everything service running?")