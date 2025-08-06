# src/processing/action_router.py

from src.agents.tools import file_system_tools
from src.agents.crew_setup import DeveloperCrew # <-- IMPORT THE CREW

# A dictionary mapping the 'intent' string to the actual tool function.
TOOL_REGISTRY = {
    "create_file": file_system_tools.create_file,
    "delete_file": file_system_tools.delete_file,
}

async def execute_action(command: dict) -> str:
    # ... (this function remains the same as before)
    intent = command.get("intent")
    arguments = command.get("params", {})
    if "target" in command: arguments["target"] = command["target"]
    
    if intent in TOOL_REGISTRY:
        tool_function = TOOL_REGISTRY[intent]
        print(f"⚙️ Executing simple tool for intent: '{intent}' with args: {arguments}")
        try:
            return tool_function(**arguments)
        except Exception as e:
            return f"❌ Error during execution of '{intent}': {e}"
    else:
        return f"❌ Error: Unknown intent '{intent}'. No simple tool registered."


async def route_action(parsed_command: dict) -> str:
    """
    Routes the parsed command. It can execute simple tools, sequences, or kick off a CrewAI crew.
    """
    action_type = parsed_command.get("type")

    if action_type == "sequence":
        # ... (this logic remains the same as before)
        results = []
        for action in parsed_command.get("actions", []):
            result_msg = await execute_action(action)
            results.append(result_msg)
            if "❌ Error" in result_msg:
                results.append("Sequence stopped due to an error.")
                break
        return "\n".join(results)

    elif action_type == "crew":
        # --- NEW: Handle CrewAI tasks ---
        print(" delegating task to CrewAI...")
        inputs = parsed_command.get("arguments", {})
        try:
            crew_result = DeveloperCrew().crew().kickoff(inputs=inputs)
            return f"✅ CrewAI task completed successfully.\n--- Report ---\n{crew_result}"
        except Exception as e:
            return f"❌ CrewAI task failed: {e}"
    
    elif action_type == "os":
        # It's a single, simple OS action
        return await execute_action(parsed_command)

    else:
        return f"❌ Error: Unknown action type '{action_type}'."