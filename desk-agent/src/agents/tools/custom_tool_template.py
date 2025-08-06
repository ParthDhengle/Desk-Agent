# src/agents/tools/custom_tool_template.py

from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "A Useful Tool Name"
    description: str = "A clear description of what this tool does and when an agent should use it."

    def _run(self, argument: str) -> str:
        # The logic for your tool goes here.
        # For example, you could call an API, interact with a database,
        # or perform a complex calculation.
        print(f"Executing MyCustomTool with argument: {argument}")
        return f"Result for '{argument}'"