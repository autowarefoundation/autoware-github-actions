import os
import re
import argparse
import logging
from typing import Optional

from ruamel.yaml import YAML
from packaging import version
import git
import github
from github import Github    # cspell: ignore Github


# Parse arguments
parser = argparse.ArgumentParser(description="Create a PR to update version in autoware.repos")

# Verbosity count
parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbosity level")

# Repository information
args_repo = parser.add_argument_group("Repository information")
args_repo.add_argument("--parent_dir", type=str, default="./", help="The parent directory of the repository")
args_repo.add_argument("--repo_name", type=str, default="autowarefoundation/autoware_dummy_repository", help="The repository name to create a PR")
args_repo.add_argument("--base_branch", type=str, default="main", help="The base branch of autoware.repos")
args_repo.add_argument("--new_branch_prefix", type=str, default="feat/update-", help="The prefix of the new branch name")

'''
Following default pattern = r'\b(v?\d+\.\d+(?:\.\d+)?(?:-\w+)?(?:\+\w+(\.\d+)?)?)\b'
can parse the following example formats:
    "0.0.1",
    "v0.0.1",
    "ros2-v0.0.4",
    "xxx-1.0.0-yyy",
    "2.3.4",
    "v1.2.3-beta",
    "v1.0",
    "v2",
    "1.0.0-alpha+001",
    "v1.0.0-rc1+build.1",
    "2.0.0+build.1848",
    "2.0.1-alpha.1227",
    "1.0.0-alpha.beta",
    "ros_humble-v0.10.2"
'''
args_repo.add_argument("--semantic_version_pattern",
                       type=str,
                       default=r'\b(v?\d+\.\d+(?:\.\d+)?(?:-\w+)?(?:\+\w+(\.\d+)?)?)\b',
                       help="The pattern of semantic version"
)

# For the Autoware
args_aw = parser.add_argument_group("Autoware")
args_aw.add_argument("--autoware_repos_file_name", type=str, default="autoware.repos", help="The path to autoware.repos")

args = parser.parse_args()


# Initialize logger depending on the verbosity level
if args.verbose == 0:
    logging.basicConfig(level=logging.WARNING)
elif args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose >= 2:
    logging.basicConfig(level=logging.DEBUG)


logger = logging.getLogger(__name__)


class AutowareRepos:
    """
    This class gets information from autoware.repos and updates it

    Attributes:
        autoware_repos_file_name (str): the path to autoware.repos. e.g. "./autoware.repos"
        autoware_repos (dict): the content of autoware.repos
    """
    def __init__(self, autoware_repos_file_name: str):
        self.autoware_repos_file_name: str = autoware_repos_file_name

        self.yaml = YAML()

        # Keep comments in the file
        self.yaml.preserve_quotes = True

        with open(self.autoware_repos_file_name, "r") as file:
            self.autoware_repos = self.yaml.load(file)

    def _parse_repos(self) -> dict[str, str]:
        """
        parse autoware.repos and return a dictionary of GitHub repository URLs and versions

        Returns:
            repository_url_version_dict (dict[str, str]): a dictionary of GitHub repository URLs and versions. e.g. {'https://github.com/tier4/glog.git': 'v0.6.0'}
        """
        repository_url_version_dict: dict[str, str] = {
            repository_info["url"]: repository_info["version"]
            for repository_info in self.autoware_repos["repositories"].values()
        }
        return repository_url_version_dict

    def pickup_semver_respositories(self, semantic_version_pattern: str) -> dict[str, str]:
        """
        pick up repositories with semantic version tags

        Args:
            semantic_version_pattern (str): a regular expression pattern for semantic version. e.g. r'(v\d+\.\d+\.\d+)'

        Returns:
            repository_url_semantic_version_dict (dict[str, str]): a dictionary of GitHub repository URLs and semantic versions. e.g. {'https://github.com/tier4/glog.git': 'v0.6.0'}

        """
        repository_url_version_dict = self._parse_repos()

        repository_url_semantic_version_dict: dict[str, Optional[str]] = {
            url: (match.group(1) if (match := re.search(semantic_version_pattern, version)) else None)
            for url, version in repository_url_version_dict.items()
        }
        return repository_url_semantic_version_dict

    def update_repository_version(self, url: str, new_version: str) -> None:
        """
        update the version of the repository specified by the URL

        Args:
            url (str): the URL of the repository to be updated
            new_version (str): the new version to be set
        """
        for repository_relative_path, repository_info in self.autoware_repos["repositories"].items():
            if repository_info["url"] == url:
                target_repository_relative_path: str = repository_relative_path

        self.autoware_repos["repositories"][target_repository_relative_path]["version"] = new_version

        with open(self.autoware_repos_file_name, "w") as file:
            self.yaml.dump(self.autoware_repos, file)


class GitHubInterface:

    # Pattern for GitHub repository URL
    URL_PATTERN = r'https://github.com/([^/]+)/([^/]+?)(?:\.git)?$'

    def __init__(self, token: str):
        self.g = Github(token)    # cspell: ignore Github

    def url_to_repository_name(self, url:str) -> str:
        # Get repository name from url
        match = re.search(GitHubInterface.URL_PATTERN, url)    # cspell: ignore Github
        assert match is not None, f"URL {url} is invalid"
        user_name = match.group(1)
        repo_name = match.group(2)

        return str(f'{user_name}/{repo_name}')

    def get_tags_by_url(self, url: str) -> list[str]:
        # Extract repository's name from URL
        repo_name = self.url_to_repository_name(url)

        # Get tags
        tags: github.PaginatedList.PaginatedList = self.g.get_repo(repo_name).get_tags()

        return [tag.name for tag in tags]

    def create_pull_request(self, repo_name: str, title: str, body: str, head: str, base: str) -> None:
        # Create a PR from head to base
        self.g.get_repo(repo_name).create_pull(
            title=title,
            body=body,
            head=head,
            base=base,
        )


def get_latest_tag(tags: list[str], current_version: str) -> Optional[str]:
    '''
    Description:
        Get the latest tag from the list of tags

    Args:
        tags (list[str]): a list of tags
        current_version (str): the current version of the repository
    '''
    latest_tag = None
    for tag in tags:
        # Exclude parse failed ones such as 'tier4/universe', 'main', ... etc
        try:
            version.parse(tag)
        except (version.InvalidVersion, TypeError):
            continue

        # OK, it's a valid version
        if latest_tag is None:
            latest_tag = tag
        else:
            if version.parse(tag) > version.parse(latest_tag):
                latest_tag = tag

    return latest_tag


def create_one_branch(repo: git.Repo, branch_name: str) -> bool:

    # Check if the branch already exists
    if branch_name in repo.heads:
        logger.info(f"Branch '{branch_name}' already exists.")
        return False
    else:
        # Create a new branch and checkout
        repo.create_head(branch_name)
        logger.info(f"Created a new branch '{branch_name}'")
        return True


def create_version_update_pr(args: argparse.Namespace) -> None:

    # Get GitHub token
    github_token: str = os.getenv("GITHUB_TOKEN", default=None)
    if github_token == "None":
        raise ValueError("Please set GITHUB_TOKEN as an environment variable")
    github_interface = GitHubInterface(token = github_token)    # cspell: ignore Github

    autoware_repos: AutowareRepos = AutowareRepos(autoware_repos_file_name = args.autoware_repos_file_name)

    # Get the repositories with semantic version tags
    repository_url_semantic_version_dict: dict[str, str] = autoware_repos.pickup_semver_respositories(semantic_version_pattern = args.semantic_version_pattern)

    # Get reference to the repository
    repo = git.Repo(args.parent_dir)

    # Get all the branches
    branches = [r.remote_head for r in repo.remote().refs]

    for url, current_version in repository_url_semantic_version_dict.items():
        '''
        Description:
            In this loop, the script will create a PR to update the version of the repository specified by the URL.
            The step is as follows:
                1. Get tags of the repository
                2. Check if the current version is the latest
                3. Get the latest tag
                4. Create a new branch
                5. Update autoware.repos
                6. Commit and push
                7. Create a PR
        '''

        # get tags of the repository
        tags: list[str] = github_interface.get_tags_by_url(url)

        latest_tag: Optional[str] = get_latest_tag(tags, current_version)

        # Skip if the expected format is not found
        if latest_tag is None:
            logger.debug(f"The latest tag with expected format is not found in the repository {url}. Skip for this repository.")
            continue

        # Exclude parse failed ones such as 'tier4/universe', 'main', ... etc
        try:
            # If current version is a valid version, compare with the current version
            logger.debug(f"url: {url}, latest_tag: {latest_tag}, current_version: {current_version}")
            if version.parse(latest_tag) > version.parse(current_version):
                # OK, the latest tag is newer than the current version
                pass
            else:
                # The current version is the latest
                logger.debug(f"Repository {url} has the latest version {current_version}. Skip for this repository.")
                continue
        except (version.InvalidVersion, TypeError):
            # If the current version is not a valid version and the latest tag is a valid version, let's update
            pass

        # Get repository name
        repo_name: str = github_interface.url_to_repository_name(url)

        # Set branch name
        branch_name: str = f"{args.new_branch_prefix}{repo_name}/{latest_tag}"

        # Check if the remote branch already exists
        if branch_name in branches:
            logger.info(f"Branch '{branch_name}' already exists on the remote.")
            continue

        # First, create a branch
        create_one_branch(repo, branch_name)

        # Switch to the branch
        repo.heads[branch_name].checkout()

        # Change version in autoware.repos
        autoware_repos.update_repository_version(url, latest_tag)

        # Add
        repo.index.add([args.autoware_repos_file_name])

        # Commit
        commit_message = f"feat(autoware.repos): update {repo_name} to {latest_tag}"
        repo.git.commit(m=commit_message, s=True)

        # Push
        origin = repo.remote(name='origin')
        origin.push(branch_name)

        # Switch back to base branch
        repo.heads[args.base_branch].checkout()

        # Create a PR
        github_interface.create_pull_request(
            repo_name = args.repo_name,
            title = f"feat(autoware.repos): update {repo_name} to {latest_tag}",
            body = f"This PR updates the version of the repository {repo_name} in autoware.repos",
            head = branch_name,
            base = args.base_branch
        )

        # Switch back to base branch
        repo.heads[args.base_branch].checkout()

        # Reset any changes
        repo.git.reset('--hard', f'origin/{args.base_branch}')

        # Clean untracked files
        repo.git.clean('-fd')

        # Restore base's autoware.repos
        autoware_repos: AutowareRepos = AutowareRepos(autoware_repos_file_name = args.autoware_repos_file_name)

    # Loop end


if __name__ == "__main__":

    create_version_update_pr(args)
