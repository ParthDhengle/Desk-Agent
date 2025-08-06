# src/utils/json_parser.py

import json
import re

def extract_json_from_response(text: str) -> dict | None:
    """
    Finds and parses a JSON object from a string, even if it's embedded in other text.
    
    Args:
        text: The string potentially containing a JSON object.

    Returns:
        A dictionary if JSON is found and parsed, otherwise None.
    """
    # Look for a JSON block within markdown ```json ... ```
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # If no markdown block, assume the whole string might be JSON or contain it
        json_str = text

    try:
        # Attempt to parse the extracted string as JSON
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"⚠️ Warning: Could not decode JSON from the model's response.")
        return None