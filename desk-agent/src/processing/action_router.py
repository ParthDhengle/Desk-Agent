# src/processing/action_router.py

from src.agents.tools import file_system_tools

# A dictionary mapping the 'intent' string to the actual tool function.
TOOL_REGISTRY = {
    "create_file": file_system_tools.create_file,
    "delete_file": file_system_tools.delete_file,
    # Add other intents and their corresponding functions here
}

async def execute_action(command: dict) -> str:
    """
    Executes a single, validated command. Assumes confirmation has already been handled.

    Args:
        command: A dictionary for a single action, from the parser.

    Returns:
        A string indicating the result of the action.
    """
    intent = command.get("intent")
    
    # The new prompt uses 'target', 'source', etc., at the top level,
    # and reserves 'params' for other arguments. We'll combine them.
    arguments = command.get("params", {})
    if "target" in command: arguments["target"] = command["target"]
    if "source" in command: arguments["source"] = command["source"]
    if "destination" in command: arguments["destination"] = command["destination"]
    
    if intent in TOOL_REGISTRY:
        tool_function = TOOL_REGISTRY[intent]
        print(f"⚙️ Executing tool for intent: '{intent}' with args: {arguments}")
        try:
            # Call the tool function, unpacking the arguments dictionary
            return tool_function(**arguments)
        except TypeError as e:
            return f"❌ Error: Missing or incorrect arguments for intent '{intent}'. Details: {e}"
        except Exception as e:
            return f"❌ Error during execution of '{intent}': {e}"
    else:
        return f"❌ Error: Unknown intent '{intent}'. No tool registered."

async def route_action(parsed_command: dict) -> str:
    """
    Routes the parsed command. If it's a sequence, it executes each action.
    If it's a single action, it executes it directly.

    Args:
        parsed_command: The full JSON object from the intent parser.

    Returns:
        A final status message.
    """
    if parsed_command.get("type") == "sequence":
        results = []
        for action in parsed_command.get("actions", []):
            result_msg = await execute_action(action)
            results.append(result_msg)
            # If a step fails, you might want to stop the sequence
            if "❌ Error" in result_msg:
                results.append("Sequence stopped due to an error.")
                break
        return "\n".join(results)
    else:
        # It's a single action
        return await execute_action(parsed_command)