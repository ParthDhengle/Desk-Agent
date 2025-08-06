# src/agents/crew_setup.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# NEW: Import the ChatGoogleGenerativeAI class
from langchain_google_genai import ChatGoogleGenerativeAI

from src.agents.tools.file_system_tools import create_file

# Instantiate the Gemini model.
# By default, it will look for the GOOGLE_API_KEY in your environment variables.
# We'll use the powerful Gemini 1.5 Pro model.
gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

@CrewBase
class DeveloperCrew:
    """A crew of agents designed to handle software development tasks."""
    agents_config = 'src/agents/config/agents.yaml'
    tasks_config = 'src/agents/config/tasks.yaml'

    @agent
    def project_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['project_planner'],
            # Use the new Gemini LLM instance
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def code_generator(self) -> Agent:
        create_file_tool = create_file
        return Agent(
            config=self.agents_config['code_generator'],
            tools=[create_file_tool],
            # Use the new Gemini LLM instance here as well
            llm=gemini_llm,
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
            context=[self.planning_task()]
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