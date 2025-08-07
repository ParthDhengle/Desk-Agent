# src/processing/action_router.py

from src.agents.tools import file_system_tools
from src.agents.crew_setup import DeveloperCrew, gemini_llm # <-- IMPORT THE CREW and gemini_llm

# A dictionary mapping the 'intent' string to the actual tool function.
TOOL_REGISTRY = {
    "create_file": file_system_tools.create_file,
    "delete_file": file_system_tools.delete_file,
    "open_application": file_system_tools.open_application, # <-- ADD NEW TOOL
}

async def execute_action(command: dict) -> str:
    intent = command.get("intent")
    
    arguments = command.get("params", {})
    if "target" in command: arguments["target"] = command["target"]
    if "source" in command: arguments["source"] = command["source"]
    if "destination" in command: arguments["destination"] = command["destination"]
    
    if intent in TOOL_REGISTRY:
        tool_function = TOOL_REGISTRY[intent]
        print(f"⚙️ Executing simple tool for intent: '{intent}' with args: {arguments}")
        try:
            return tool_function(**arguments)
        except TypeError as e:
            return f"❌ Error: Missing or incorrect arguments for intent '{intent}'. Details: {e}"
        except Exception as e:
            return f"❌ Error during execution of '{intent}': {e}"
    else:
        return f"❌ Error: Unknown intent '{intent}'. No simple tool registered."

async def route_action(parsed_command: dict) -> str:
    """
    Routes the parsed command. It can execute simple tools, sequences, or kick off a CrewAI crew.
    """
    # --- PRIMARY FIX: Use 'action_type' instead of 'type' ---
    action_type = parsed_command.get("action_type")

    if action_type == "sequence":
        results = []
        for action in parsed_command.get("actions", []):
            result_msg = await execute_action(action)
            results.append(result_msg)
            if "❌ Error" in result_msg:
                results.append("Sequence stopped due to an error.")
                break
        return "\n".join(results)

    elif action_type == "crew":
        print(" delegating task to CrewAI...")
        inputs = parsed_command.get("arguments", {})
        try:
            crew_result = DeveloperCrew().crew().kickoff(inputs=inputs)
            return f"✅ CrewAI task completed successfully.\n--- Report ---\n{crew_result}"
        except Exception as e:
            return f"❌ CrewAI task failed: {e}"
    
    elif action_type == "os":
        return await execute_action(parsed_command)

    # --- NEW: Handle 'chat' action type ---
    elif action_type == "chat":
        print("💬 Handling general chat query...")
        query = parsed_command.get("arguments", {}).get("query", "")
        if not query:
             query = parsed_command.get("target") # Fallback to target if query is not in args
        if not query:
            return "It seems you wanted to chat, but I didn't understand your question."
        
        try:
            # Use the powerful Gemini model for a conversational response
            response = await gemini_llm.ainvoke(query)
            return response.content
        except Exception as e:
            return f"❌ Error during chat: {e}"

    else:
        # This error message is now accurate
        return f"❌ Error: Unknown action type '{action_type}'."