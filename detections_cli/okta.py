# Execute actions in an Okta organization

import logging
from typing import Dict

import requests

LOGGER = logging.getLogger()


def create_user(okta_api_url: str, api_token: str, user: Dict):
    """Create an Okta user account."""
    url = f"{okta_api_url}/users"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"SSWS {api_token}",
    }

    payload = {
        "profile": {
            "firstName": user["first_name"],
            "lastName": user["last_name"],
            "email": user["email"],
            "login": user["login"],
        },
        "credentials": {"password": {"value": user["password"]}},
    }

    LOGGER.info(f"Attempting to create new Okta user {user['login']}")
    try:
        response = requests.post(url=url, headers=headers, json=payload, timeout=7)
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        raise e

    response_json = response.json()

    if response.ok:
        LOGGER.info(f"Created new Okta user {user['login']} (ID: {response_json['id']})")
        return response_json["id"]
    else:
        msg = (
            f"Error creating new Okta user {user['login']}\n"
            f"Response Code: {response.status_code} | Response Reason: {response.reason}\n"
            f'Error Code: {response_json.get("errorCode")} | Error Summary: {response_json.get("errorSummary")}\n'
            f'Error Causes: {response_json.get("errorCauses")}'
        )
        LOGGER.error(msg)

        raise Exception(msg)


def assign_admin_role(okta_api_url: str, okta_api_token: str, user_id: str, admin_role: str):
    """Assign an admin role to an Okta user account."""
    url = f"{okta_api_url}/users/{user_id}/roles"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"SSWS {okta_api_token}",
    }

    payload = {"type": admin_role}

    LOGGER.info(f"Attempting to assign admin role '{admin_role}' to Okta user ID {user_id}")
    try:
        response = requests.post(url=url, headers=headers, json=payload, timeout=7)
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        raise e

    response_json = response.json()

    if response.ok:
        LOGGER.info(f"Assigned admin role '{admin_role}' to Okta user ID {user_id}")
        return
    else:
        msg = (
            f"Error assigning Okta admin role '{admin_role}' to Okta user ID {user_id}\n"
            f"Response Code: {response.status_code} | Response Reason: {response.reason}\n"
            f'Error Code: {response_json.get("errorCode")} | Error Summary: {response_json.get("errorSummary")}\n'
            f'Error Causes: {response_json.get("errorCauses")}'
        )
        LOGGER.error(msg)

        raise Exception(msg)


def deactivate_user(okta_api_url: str, okta_api_token: str, user_id: str):
    """Deactivate an Okta user account.

    Note that an Okta user account much be deactivated before it can be deleted.
    """
    url = f"{okta_api_url}/users/{user_id}/lifecycle/deactivate"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"SSWS {okta_api_token}",
    }

    LOGGER.info(f"Attempting to deactivate Okta user ID {user_id}")
    try:
        response = requests.post(url=url, headers=headers, timeout=7)
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        raise e

    response_json = response.json()

    if response.ok:
        LOGGER.info(f"Deactivated Okta user ID {user_id}")
        return
    else:
        msg = (
            f"Error deactivating Okta user ID {user_id}\n"
            f"Response Code: {response.status_code} | Response Reason: {response.reason}\n"
            f'Error Code: {response_json.get("errorCode")} | Error Summary: {response_json.get("errorSummary")}\n'
            f'Error Causes: {response_json.get("errorCauses")}'
        )
        LOGGER.error(msg)

        raise Exception(msg)


def delete_user(okta_api_url: str, okta_api_token: str, user_id: str):
    """Delete an Okta user account.

    Note that an Okta user account much be deactivated before it can be deleted.
    """
    url = f"{okta_api_url}/users/{user_id}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"SSWS {okta_api_token}",
    }

    LOGGER.info(f"Attempting to delete Okta user ID {user_id}")
    try:
        response = requests.delete(url=url, headers=headers, timeout=7)
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        raise e

    if response.ok:
        LOGGER.info(f"Deleted Okta user ID {user_id}")
        return
    else:
        response_json = response.json()
        msg = (
            f"Error deleting Okta user ID {user_id}\n"
            f"Response Code: {response.status_code} | Response Reason: {response.reason}\n"
            f'Error Code: {response_json.get("errorCode")} | Error Summary: {response_json.get("errorSummary")}\n'
            f'Error Causes: {response_json.get("errorCauses")}'
        )
        LOGGER.error(msg)

        raise Exception(msg)
