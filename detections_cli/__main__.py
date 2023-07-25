import argparse
import importlib
import logging
from pathlib import Path
from typing import Dict, List

from decouple import config

from detections_cli.github import search_issues as search_github_issues, update_issue as update_github_issue

LOGGER = logging.getLogger()

TRIGGERS_DIR = Path(__file__).parent / "triggers"
TRIGGER_FILES = list(TRIGGERS_DIR.rglob("*.py"))


def run_all_triggers():
    """Run all available rule triggers."""
    for trigger_file in TRIGGER_FILES:
        trigger = importlib.import_module(f"detections_cli.triggers.{trigger_file.stem}")
        if getattr(trigger, "TRIGGER_METADATA", None) is not None:
            trigger.main()


def check_for_matching_alerts(trigger_metadata: Dict, rule: Dict, alerts: List[Dict]) -> List[Dict]:
    """Check if any alerts were created for the rule that was triggered."""
    # Keep a count of the number of alerts that match the rule
    matching_alerts = []

    for alert in alerts:
        # Check if the title of the alert (GitHub issue) matches the rule name
        if alert["title"] == f"[Alert] {rule['name']}":
            LOGGER.info(f"Found alert for rule '{rule['name']}' (Rule ID: {rule['rule_id']})")

            # Check if the issue body contains the indicator(s) from the rule trigger metadata
            alert_match = check_alert_for_indicators(alert=alert, trigger_metadata=trigger_metadata)
            if alert_match:
                LOGGER.info(
                    f"Found test indicators in alert for rule '{rule['name']}' (Rule ID: {rule['rule_id']}). "
                    f"GitHub issue: {alert['html_url']}"
                )
                matching_alerts.append(alert)
            else:
                LOGGER.info(
                    f"Test indicators not found in alert for rule '{rule['name']}' "
                    f"(Rule ID: {rule['rule_id']}). GitHub issue: {alert['html_url']}"
                )

    return matching_alerts


def check_alert_for_indicators(alert: Dict, trigger_metadata: Dict) -> bool:
    """Check if an alert contains any of the indicators that were tested."""
    for indicator in trigger_metadata["test_indicators"]:
        if indicator not in alert["body"]:
            return False
    return True


def close_alerts(github_api_token: str, alerts: List[Dict]):
    """Close alerts that were created from the rules that were triggered."""
    for alert in alerts:
        labels = ["test"]
        for label in alert["labels"]:
            labels.append(label["name"])

        update_github_issue(
            github_api_token=github_api_token,
            issue_url=alert["url"],
            issue_updates={"state": "closed", "labels": labels},
        )


def validate_alerts():
    """Check that alerts were created from the rules that were triggered."""
    github_dac_repo_api_url = config("GITHUB_DAC_REPO_API_URL")
    github_dac_repo_api_token = config("GITHUB_DAC_REPO_API_TOKEN")

    # For the purposes of this experiment, we'll retrieve the most recently created issues from the GitHub repo
    # For prod, we'll want to use specific queries to search for GitHub issues created by the rules that were triggered
    issues = search_github_issues(
        github_api_token=github_dac_repo_api_token,
        github_repo_api_url=github_dac_repo_api_url,
        params={
            "state": "open",
            # Uncomment the following line to search for issues created during the last 1d. Time is in ISO 8601 format
            # "since": f"{(datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat()}Z",
            "per_page": 100,
        },
    )

    if len(issues) == 0:
        raise Exception(f"No open issues found in GitHub repo {github_dac_repo_api_url}")

    # Import each trigger and its metadata
    for trigger_file in TRIGGER_FILES:
        trigger = importlib.import_module(f"detections_cli.triggers.{trigger_file.stem}")
        # Load the metadata from each trigger
        if getattr(trigger, "TRIGGER_METADATA", None) is not None:
            trigger_metadata = trigger.TRIGGER_METADATA
        else:
            continue

        logging.info(f"Checking for alerts created by trigger '{trigger_metadata['name']}'")

        # Validate that alerts were created from the rules that were triggered
        for rule in trigger_metadata["rules"]:
            LOGGER.info(f"Checking for alerts created for rule '{rule['name']}' (Rule ID: {rule['rule_id']})")
            matching_alerts = check_for_matching_alerts(trigger_metadata=trigger_metadata, rule=rule, alerts=issues)

            if len(matching_alerts) == 0:
                msg = (
                    f"No matching alerts found for trigger '{trigger_metadata['name']}' "
                    f"and indicators for rule '{rule['name']}' (Rule ID: {rule['rule_id']})"
                )
                LOGGER.error(msg)
                raise Exception(msg)

            LOGGER.info(
                f"Found {len(matching_alerts)} matching alerts for trigger '{trigger_metadata['name']}' and "
                f"indicators for rule '{rule['name']}' (Rule ID: {rule['rule_id']})"
            )

            # Close matching alerts
            close_alerts(github_api_token=github_dac_repo_api_token, alerts=matching_alerts)


if __name__ == "__main__":
    LOGGER.info("detections_cli started")

    # TODO Raise an error if the run_all_triggers argument is used with the check_for_alerts argument
    # TODO Add argument to print a table of all available triggers
    # TODO Add argument to run a specific trigger

    parser = argparse.ArgumentParser(description="detections_cli")
    parser.add_argument("--run-all-triggers", action="store_true", help="Run all rule triggers.")
    parser.add_argument("--validate-alerts", action="store_true", help="Validate alerts were created by rule triggers.")
    args = parser.parse_args()

    if args.run_all_triggers:
        LOGGER.info("Running all rule triggers")
        run_all_triggers()

    if args.validate_alerts:
        LOGGER.info("Validating alerts created by rule triggers")
        validate_alerts()
