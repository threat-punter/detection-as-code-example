# Execute actions in GitHub

import logging
from typing import List, Dict

import requests

LOGGER = logging.getLogger()


def search_issues(github_api_token: str, github_repo_api_url: str, params: Dict) -> List:
    """Search for GitHub issues."""
    url = f"{github_repo_api_url}/issues"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_api_token}",
    }

    LOGGER.info(f"Searching for GitHub issues at {github_repo_api_url} with query params {params}")
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=7)
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        raise e

    if not response.ok:
        msg = (
            f"Error searching for GitHub issues at {github_repo_api_url} with query params {params}\n"
            f"Response Code: {response.status_code} | Response Reason: {response.reason}"
        )
        LOGGER.error(msg)

        raise Exception(msg)

    issues = response.json()

    LOGGER.info(f"Found {len(issues)} GitHub issues at {url} with query params {params}")

    return issues


def update_issue(github_api_token: str, issue_url: str, issue_updates: Dict):
    """Update a GitHub issue."""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_api_token}",
    }

    LOGGER.info(f"Updating GitHub issue {issue_url} with params {issue_updates}")
    try:
        response = requests.patch(url=issue_url, headers=headers, json=issue_updates, timeout=7)
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        raise e

    if not response.ok:
        msg = (
            f"Error Updating GitHub issue {issue_url} with params {issue_updates}\n"
            f"Response Code: {response.status_code} | Response Reason: {response.reason}"
        )
        LOGGER.error(msg)

        raise Exception(msg)
