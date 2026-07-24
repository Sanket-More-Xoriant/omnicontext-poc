from agents.github_graph_agent import (
    GitHubGraphAgent
)

agent = GitHubGraphAgent()

graph = agent.build_github_graph()

graph.print_graph()