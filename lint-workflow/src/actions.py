import json
import logging
import os
import urllib3 as urllib

from dataclasses import asdict
from typing import Union, Tuple

from src.utils import Colors, LintFinding, Settings, SettingsError, Action


class Actions:
    def __init__(self, settings: Settings = None) -> None:
        self.settings = settings

    def get_github_api_response(
        self, url: str, action_name: str
    ) -> Union[urllib.response.BaseHTTPResponse, None]:
        """Call GitHub API with error logging without throwing an exception."""

        http = urllib.PoolManager()
        headers = {"user-agent": "bw-linter"}

        if os.getenv("GITHUB_TOKEN", None):
            headers["Authorization"] = f"Token {os.environ['GITHUB_TOKEN']}"

        response = http.request("GET", url, headers=headers)

        if response.status == 403 and response.reason == "rate limit exceeded":
            logging.error(
                f"Failed to call GitHub API for action: {action_name} due to rate limit exceeded."
            )
            return None

        if response.status == 401 and response.reason == "Unauthorized":
            logging.error(
                f"Failed to call GitHub API for action: {action_name}: {response.data}."
            )
            return None

        return response

    def exists(self, action: Action) -> bool:
        """Takes and action id and checks if the action repo exists."""

        url = f"https://api.github.com/repos/{action.name}"
        response = self.get_github_api_response(url, action.name)

        if response is None:
            # Handle github api limit exceed by returning that the action exists without actually checking
            # to prevent false errors on linter output. Only show it as an linter error.
            return True

        if response.status == 404:
            return False

        return True

    def get_latest_version(self, action: Action) -> Tuple[str, str]:
        """Gets the latest version of the Action to compare against."""

        # Get tag from latest release
        response = self.get_github_api_response(
            f"https://api.github.com/repos/{action.name}/releases/latest", action.name
        )
        if not response:
            return None

        tag_name = json.loads(response.data)["tag_name"]

        # Get the URL to the commit for the tag
        response = self.get_github_api_response(
            f"https://api.github.com/repos/{action.name}/git/ref/tags/{tag_name}",
            action.name,
        )
        if not response:
            return None

        if json.loads(response.data)["object"]["type"] == "commit":
            sha = json.loads(response.data)["object"]["sha"]
        else:
            url = json.loads(response.data)["object"]["url"]
            # Follow the URL and get the commit sha for tags
            response = self.get_github_api_response(url, action.name)
            if not response:
                return None

            sha = json.loads(response.data)["object"]["sha"]

        return Action(name=action.name, version=tag_name, sha=sha)

    def add(self, new_action_name: str, filename: str) -> None:
        print("Actions: add")
        updated_actions = self.settings.approved_actions
        proposed_action = Action(name=new_action_name)

        if self.exists(proposed_action):
            latest = self.get_latest_version(proposed_action)
            updated_actions[latest.name] = latest

        with open(filename, "w") as action_file:
            converted_updated_actions = {
                name: asdict(action) for name, action in updated_actions.items()
            }
            action_file.write(
                json.dumps(converted_updated_actions, indent=2, sort_keys=True)
            )

    def update(self, filename: str) -> None:
        print("Actions: update")
        updated_actions = {}
        for action in self.settings.approved_actions.values():
            if self.exists(action):
                latest_release = self.get_latest_version(action)
                if action != latest_release:
                    print(
                        (
                            f" - {action.name} \033[{Colors.yellow}changed\033[0m: "
                            f"({action.version}, {action.sha}) => ({latest_release.version}, {latest_release.sha})"
                        )
                    )
                else:
                    print(f" - {action.name} \033[{Colors.green}ok\033[0m")
                updated_actions[action.name] = latest_release

        with open(filename, "w") as action_file:
            converted_updated_actions = {
                name: asdict(action) for name, action in updated_actions.items()
            }
            action_file.write(
                json.dumps(converted_updated_actions, indent=2, sort_keys=True)
            )
