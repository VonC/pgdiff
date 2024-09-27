import sys
from github import Github, Auth
import urllib.parse


def get_changed_files_pygithub(owner, repo, base_commit, head_commit):
    try:
        with open("access_token.txt", "r") as f:
            access_token = f.read().strip()
    except FileNotFoundError:
        print(
            "Error: 'access_token.txt' not found. Please create this file and add your GitHub access token."
        )
        sys.exit(1)  # Exit with an error code

    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    repo = g.get_repo(f"{owner}/{repo}")

    all_changed_files = {}

    comparison = repo.compare(base_commit, head_commit)
    for commit in comparison.commits:
        for file in commit.files:  # Note: This is limited to 300 files per commit
            filename = file.filename
            status = file.status

            if status == "renamed":
                previous_filename = file.previous_filename
                all_changed_files[previous_filename] = "deleted"
                all_changed_files[filename] = "added"
            else:
                all_changed_files[filename] = status

    # Sort and remove duplicates (if needed)
    sorted_changed_files = dict(sorted(all_changed_files.items()))

    return sorted_changed_files


# Example usage
owner = "YOUR_GITHUB_USERNAME"
owner = "git"
repo = "YOUR_REPO_NAME"
repo = "git"
base_commit = "COMMIT_SHA_1"
base_commit = "7ffcbafbf32185da7dccb4b3f49b871f24ab58c4"
head_commit = "COMMIT_SHA_2"
head_commit = "a116aba5d54bf44c6fc27fa1a4c2431d53cf8ff5"

changed_files = get_changed_files_pygithub(owner, repo, base_commit, head_commit)
print(changed_files)
