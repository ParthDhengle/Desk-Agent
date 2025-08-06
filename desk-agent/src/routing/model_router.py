# src/routing/model_router.py

import litellm

# Configure LiteLLM to be less verbose in the console
litellm.set_verbose=False

async def get_llm_response(messages: list, model_name: str) -> str | None:
    """
    Gets a response from a specified model via LiteLLM.

    Args:
        messages: A list of message dictionaries (e.g., [{"role": "user", ...}]).
        model_name: The name of the model to use (from config.py).

    Returns:
        The text content of the response, or None if an error occurs.
    """
    try:
        # Asynchronously call the model
        response = await litellm.acompletion(
            model=model_name,
            messages=messages,
        )
        # Extract the content from the first choice in the response
        return response.choices[0].message.content
    except Exception as e:
        # Handle potential exceptions, like connection errors to Ollama
        print(f"❌ Error: LiteLLM failed to get a response from the model.")
        print(f"   Reason: {e}")
        return None