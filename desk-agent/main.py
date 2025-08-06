# main.py

import asyncio
import pprint  # Used for printing dictionaries nicely

from src.processing.intent_parser import parse_intent

async def main():
    """
    Main asynchronous loop for the DeskAgent.
    For Step 1, it's a simple command-line interface to test the parser.
    """
    print("🚀 DeskAgent Parser Initialized. Type 'exit' to quit.")
    print("-" * 30)

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() == "exit":
            break

        if not user_input.strip():
            continue

        # Call our asynchronous parser
        parsed_command = await parse_intent(user_input)

        if parsed_command:
            print("✅ Parsed Command:")
            pprint.pprint(parsed_command)
        else:
            print("❌ Could not parse command.")
        
        print("-" * 30)

if __name__ == "__main__":
    # Ensure Ollama is running with the 'phi3' model before starting.
    # To run: `ollama run phi3` in your terminal.
    
    # Run the main async function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting DeskAgent.")