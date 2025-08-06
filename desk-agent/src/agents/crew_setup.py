# src/agents/crew_setup.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms import Ollama

from src.agents.tools.file_system_tools import create_file # Example of importing a local tool

# To use local models through Ollama, we need to instantiate them
# In a real scenario, you'd likely configure this more dynamically
ollama_llama3 = Ollama(model="llama3")

@CrewBase
class DeveloperCrew:
    """A crew of agents designed to handle software development tasks."""
    agents_config = 'src/agents/config/agents.yaml'
    tasks_config = 'src/agents/config/tasks.yaml'

    @agent
    def project_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['project_planner'],
            llm=ollama_llama3,
            verbose=True
        )

    @agent
    def code_generator(self) -> Agent:
        # Giving the code generator a file creation tool
        # In a real scenario, you would pass all relevant tools
        # from your tools directory here.
        create_file_tool = create_file 
        return Agent(
            config=self.agents_config['code_generator'],
            tools=[create_file_tool],
            llm=ollama_llama3,
            verbose=True
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_task'],
            agent=self.project_planner()
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
            agent=self.code_generator(),
            context=[self.planning_task()] # This task depends on the planning_task
        )

    @crew
    def crew(self) -> Crew:
        """Creates and configures the developer crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )