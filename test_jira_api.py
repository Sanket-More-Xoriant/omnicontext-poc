from dotenv import load_dotenv
from atlassian import Jira
import os

load_dotenv()

jira = Jira(
    url=os.getenv("JIRA_URL"),
    username=os.getenv("JIRA_USERNAME"),
    password=os.getenv("JIRA_API_TOKEN"),
    cloud=True,
)

issues = jira.jql(
    f'project = "{os.getenv("JIRA_PROJECT_KEY")}"',
    limit=5
)

print("Connected Successfully")
print(f"Issues Found: {len(issues.get('issues', []))}")

for issue in issues.get("issues", []):
    print(
        issue["key"],
        "-",
        issue["fields"]["summary"]
    )
