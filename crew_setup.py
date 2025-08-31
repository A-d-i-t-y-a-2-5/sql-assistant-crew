from crewai import LLM, Agent, Task, Crew
from typing import List
import yaml

from classes import ReviewedSQLQuery, SQLQuery

files = {
    "agents": "config/agents.yaml",
    "tasks": "config/tasks.yaml",
}

configs = {}
for config_type, file_path in files.items():
    with open(file_path, "r") as file:
        configs[config_type] = yaml.safe_load(file)

agents_config = configs["agents"]
tasks_config = configs["tasks"]

llm = LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434")

# Creating Agents
query_generator_agent = Agent(config=agents_config["query_generator_agent"], llm=llm)

query_reviewer_agent = Agent(config=agents_config["query_reviewer_agent"], llm=llm)

# Creating Tasks
query_task = Task(
    config=tasks_config["query_task"],
    agent=query_generator_agent,
    output_pydantic=SQLQuery,
)

review_task = Task(
    config=tasks_config["review_task"],
    agent=query_reviewer_agent,
    output_pydantic=ReviewedSQLQuery,
)

# Creating Crew objects for import
sql_generator_crew = Crew(
    agents=[query_generator_agent], tasks=[query_task], verbose=True
)

sql_reviewer_crew = Crew(
    agents=[query_reviewer_agent], tasks=[review_task], verbose=True
)
