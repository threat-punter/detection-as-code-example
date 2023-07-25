# Create an Okta user, assign an admin role to the user, and delete the user.

import logging

from decouple import config

from detections_cli.okta import create_user, assign_admin_role, deactivate_user, delete_user

LOGGER = logging.getLogger()

TRIGGER_METADATA = {
    "name": "Assign Admin Role to Okta User",
    "trigger_id": "a17971ab-3980-4936-92e0-d65d9f448204",
    "description": "Create an Okta user, assign an admin role to the user, and delete the user.",
    "test_indicators": [config("TEST_OKTA_USER_EMAIL")],
    "rules": [
        {
            "rule_id": "97d6c856-93e8-40e3-9af7-f797a5c1435b",
            "name": "Administrator Role Assigned to Non-Admin User Account",
        }
    ],
}

OKTA_API_BASE_URL = f"{config('OKTA_DEV_URL')}/api/v1"
OKTA_DEV_API_TOKEN = config("OKTA_DEV_API_TOKEN")


def main():
    """Create an Okta user, assign an admin role to the user, and delete the user."""
    LOGGER.info(f"Executing trigger '{TRIGGER_METADATA['name']}' (Trigger ID: {TRIGGER_METADATA['trigger_id']})")

    # Create new Okta user account without the admin.* prefix in the username
    okta_user_id = create_user(
        okta_api_url=OKTA_API_BASE_URL,
        api_token=OKTA_DEV_API_TOKEN,
        user={
            "first_name": config("TEST_OKTA_USER_FIRST_NAME"),
            "last_name": config("TEST_OKTA_USER_LAST_NAME"),
            "email": config("TEST_OKTA_USER_EMAIL"),
            "login": config("TEST_OKTA_USER_EMAIL"),
            "password": config("TEST_OKTA_USER_PASSWORD"),
        },
    )

    # Assign an admin role to the new Okta user account
    assign_admin_role(
        okta_api_url=OKTA_API_BASE_URL,
        okta_api_token=OKTA_DEV_API_TOKEN,
        user_id=okta_user_id,
        admin_role="READ_ONLY_ADMIN",
    )

    # Deactivate the Okta user account
    deactivate_user(okta_api_url=OKTA_API_BASE_URL, okta_api_token=OKTA_DEV_API_TOKEN, user_id=okta_user_id)

    # Delete the Okta user account
    delete_user(okta_api_url=OKTA_API_BASE_URL, okta_api_token=OKTA_DEV_API_TOKEN, user_id=okta_user_id)

    LOGGER.info(f"Ending trigger '{TRIGGER_METADATA['name']}' (Trigger ID: {TRIGGER_METADATA['trigger_id']})")


if __name__ == "__main__":
    main()
