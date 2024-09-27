import sys
from github import Github, Auth
import urllib.parse
from tqdm import tqdm


def get_changed_files_pygithub(owner, repo, base_commit, head_commit):
    try:
        with open("access_token.txt", "r") as f:
            access_token = f.read().strip()
    except FileNotFoundError:
        print(
            "Error: 'access_token.txt' not found. Please create this file and add your GitHub access token."
        )
        sys.exit(1)

    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    repo = g.get_repo(f"{owner}/{repo}")

    all_changed_files = {}

    comparison = repo.compare(base_commit, head_commit)
    commits_list = list(comparison.commits)
    total_commits = len(commits_list)
    print(f"Total commits found: {total_commits}")
    with tqdm(
        total=total_commits, desc="Processing commits", position=0
    ) as pbar_commits:
        for commit in commits_list:
            pbar_commits.update(1)
            files_list = list(commit.files)
            total_files = len(files_list)
            pbar_commits.write(
                f"Total files found for commit '{commit.sha}': {total_files}"
            )
            for file in files_list:  # Note: This is limited to 300 files per commit
                filename = file.filename
                status = file.status

                if status == "renamed":
                    previous_filename = file.previous_filename
                    all_changed_files[previous_filename] = "deleted"
                    all_changed_files[filename] = "added"
                else:
                    all_changed_files[filename] = status

    sorted_changed_files = dict(sorted(all_changed_files.items()))

    return sorted_changed_files


def categorize_files(changed_files):
    added_files = [file for file, status in changed_files.items() if status == "added"]
    removed_files = [
        file
        for file, status in changed_files.items()
        if status in ["deleted", "removed"]
    ]
    modified_files = [
        file for file, status in changed_files.items() if status == "modified"
    ]

    if added_files:
        print("\nAdded files:")
        for file in added_files:
            print(file)

    if removed_files:
        print("\nRemoved files:")
        for file in removed_files:
            print(file)

    if modified_files:
        print("\nModified files:")
        for file in modified_files:
            print(file)


# YOUR_GITHUB_USERNAME
owner = "git"
# YOUR_REPO_NAME
repo = "git"
# COMMIT_SHA_1
base_commit = "7ffcbafbf32185da7dccb4b3f49b871f24ab58c4"
# COMMIT_SHA_2
head_commit = "a116aba5d54bf44c6fc27fa1a4c2431d53cf8ff5"

changed_files = get_changed_files_pygithub(owner, repo, base_commit, head_commit)
# print(changed_files)
categorize_files(changed_files)
