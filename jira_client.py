import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

JIRA_URL = os.getenv("JIRA_BASE_URL")
JIRA_USER = os.getenv("JIRA_USERNAME")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_jira_ticket(ticket_id):
    issue_url = f"{JIRA_URL}/rest/api/2/issue/{ticket_id}"
    auth = (JIRA_USER, JIRA_TOKEN)
    headers = {"Accept": "application/json"}

    issue_response = requests.get(issue_url, auth=auth, headers=headers)
    if issue_response.status_code != 200:
        raise Exception(f" Failed to fetch issue: {issue_response.status_code} - {issue_response.text}")

    fields = issue_response.json().get("fields", {})

    created_on = fields.get("created", "")
    created_on = datetime.strptime(created_on, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M") if created_on else ""

    components = [comp["name"] for comp in fields.get("components", [])]

    ticket_summary = {
        "ticket_id": ticket_id,
        "title": fields.get("summary", "(No summary provided)"),
        "description": fields.get("description", "(No description provided)"),
        "status": fields.get("status", {}).get("name", ""),
        "labels": fields.get("labels", []),
        "created_by": fields.get("creator", {}).get("displayName", "Unknown"),
        "created_on": created_on,
        "assignee": fields.get("assignee", {}).get("displayName", "Unassigned"),
        "reporter": fields.get("reporter", {}).get("displayName", "Unknown"),
        "components": components,
        "comments": [],
        "attachments": []
    }

    comments_url = f"{issue_url}/comment"
    comments_response = requests.get(comments_url, auth=auth, headers=headers)

    if comments_response.ok:
        comments = comments_response.json().get("comments", [])
        ticket_summary["comments"] = [
            (datetime.strptime(c["created"][:19], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M") + f" – {c['author']['displayName']}", c["body"])
            for c in comments
        ]

    for att in fields.get("attachment", []):
        ticket_summary["attachments"].append({
            "filename": att.get("filename"),
            "author": att.get("author", {}).get("displayName"),
            "created": att.get("created")[:10],
            "url": att.get("content")
        })

    return ticket_summary