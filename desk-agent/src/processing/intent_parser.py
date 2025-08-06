# src/processing/intent_parser.py

from config import INTENT_MODEL
from src.routing.model_router import get_llm_response
from src.utils.json_parser import extract_json_from_response

# This is the master prompt that guides the LLM to act as an intent parser.
SYSTEM_PROMPT = """
You are an expert command parser for a voice-controlled desktop assistant named Spark.
Your primary function is to analyze the user's request and convert it into a structured, machine-readable JSON object.
You must return **VALID JSON ONLY**. Do not add explanations or any text outside the JSON structure.

### JSON Output Rules:
1.  **`action_type`**: Must be one of: ["os", "git", "code", "crew", "chat", "clarify"].
2.  **`intent`**: A specific, snake_case string representing the core action.
3.  **`requires_confirmation`**: Set to `true` for destructive actions (e.g., deleting files, shutting down).
4.  **`message`**: Always include a concise, user-facing summary of the action.
5.  **Ambiguity**: If a command is unclear, use `action_type: "clarify"` and ask a clarifying question in the `message` field.

### Supported Action Types & Examples:

**1. OS Actions (`action_type: "os"`)**
   - "create a file called api.py" -> `{"action_type": "os", "intent": "create_file", "target": "api.py", "message": "Creating file api.py."}`
   - "delete the image screenshot.png" -> `{"action_type": "os", "intent": "delete_file", "target": "screenshot.png", "requires_confirmation": true, "message": "Deleting screenshot.png."}`

**2. Git Actions (`action_type: "git"`)**
   - "commit my work with the message 'fix: update parser'" -> `{"action_type": "git", "intent": "commit_changes", "params": {"message": "fix: update parser"}, "message": "Committing changes."}`

**3. Code Generation (`action_type: "code"`)**
   - "write a python function for a fibonacci sequence" -> `{"action_type": "code", "intent": "generate_code", "params": {"description": "python function for a fibonacci sequence"}, "message": "Generating code for a fibonacci function."}`

**4. Crew Delegation (`action_type: "crew"`)**
   - Use for complex, multi-step tasks that require planning or research.
   - "set up a new flask project for a blog" -> `{"action_type": "crew", "arguments": {"topic": "a new flask project for a blog"}, "message": "Delegating project setup to the developer crew."}`
   - "research the latest trends in AI agents" -> `{"action_type": "crew", "arguments": {"topic": "latest trends in AI agents"}, "message": "Starting a research task with the crew."}`

**5. Clarification (`action_type: "clarify"`)**
   - "delete the file" -> `{"action_type": "clarify", "message": "Which file would you like me to delete?"}`

---
CONTEXT FOR THIS REQUEST:
- User's OS Context: {os_context}
- Conversation Summary: {summary}
- Recent Messages: {recent}
---

Now, parse the following user request into a single JSON object.

User Request: "{query}"
"""

async def parse_intent(user_text: str) -> dict | None:
    """
    Parses the user's text to determine their intent and returns a structured command.
    """
    # In a future step, we will populate these context variables dynamically.
    # For now, we'll use placeholders.
    context = {
        "summary": "No summary available.",
        "recent": "No recent messages.",
        "os_context": "Current directory: C:\\Users\\Parth...",
        "query": user_text
    }

    # Format the prompt with the user's query and context
    formatted_prompt = SYSTEM_PROMPT.format(**context)

    messages = [
        # Note: We are putting the entire formatted prompt into the "system" role
        # as it provides all context and instructions at once.
        {"role": "system", "content": formatted_prompt}
    ]

    print("🤖 Parsing intent with improved prompt...")
    llm_response = await get_llm_response(messages=messages, model_name=INTENT_MODEL)

    if not llm_response:
        return None

    parsed_json = extract_json_from_response(llm_response)
    print(f"✅ Parsed intent: {parsed_json}")
    return parsed_json