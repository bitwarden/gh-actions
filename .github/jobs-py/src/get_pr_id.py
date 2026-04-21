import os
import re
import sys

from dotenv import load_dotenv
from github import Auth
from github import Github
from github import GithubException

load_dotenv()

auth = Auth.Token(os.getenv("GITHUB_TOKEN", default=""))
g = Github(auth=auth)
repo = g.get_repo("bitwarden/gh-actions")


def get_pr_id(commit_sha: str) -> int | None:
    try:
        message = repo.get_commit(commit_sha).commit.message
        result = re.search(r"(\(#[0-9]+\))", message)

        if result:
            return int(result.group(0)[2:-1])
        return None

    except GithubException:
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"[!] Please pass in commit hash: {sys.argv}")
        exit(1)

    print(get_pr_id(sys.argv[1]))
