'''
Description:

    In this script, we create a PR to update the version of the repository specified by the URL in autoware.repos.
    The steps are as follows:
        1. Get the repositories with semantic version tags
            1-1. Currently we only support the semantic version pattern of r'\b(?<![^\s])\d+\.\d+\.\d+(?![-\w.+])\b'.
                This pattern matches/mismatches for the following examples:

                    "0.0.1",                # match
                    "0.1.0",                # match
                    "1.0.0",                # match
                    "2.1.1",                # match
                    "v0.0.1",               # mismatch
                    "ros2-v0.0.4",          # mismatch
                    "xxx-1.0.0-yyy",        # mismatch
                    "v1.2.3-beta",          # mismatch
                    "v1.0",                 # mismatch
                    "v2",                   # mismatch
                    "1.0.0-alpha+001",      # mismatch
                    "v1.0.0-rc1+build.1",   # mismatch
                    "2.0.0+build.1848",     # mismatch
                    "2.0.1-alpha.1227",     # mismatch
                    "1.0.0-alpha.beta",     # mismatch
                    "ros_humble-v0.10.2"    # mismatch

        2. Get the latest tag
        3. If the latest tag is newer than the current version, create a PR to update the version in autoware.repos
            3-1. We can create PRs for major, minor, or patch updates
                For example, if you want to create a PR only for major updates, you can use the --major option as follows:

                ```
                python create_prs_to_update_vcs_repositories.py --major
                ```

                If you want to create PRs for major and minor updates, you can use both the --major and --minor options as follows:

                ```
                python create_prs_to_update_vcs_repositories.py --major --minor
                ```

Example usage:

    Example 1: Create PRs for major updates
    ```
    python create_prs_to_update_vcs_repositories.py --autoware_repos_file_name autoware.repos --targets major
    ```

    Example 2: Create PRs for minor updates
    ```
    python create_prs_to_update_vcs_repositories.py --autoware_repos_file_name autoware.repos --targets minor
    ```

    Example 3: Create PRs for patch updates
    ```
    python create_prs_to_update_vcs_repositories.py --autoware_repos_file_name autoware.repos --targets patch
    ```

    Example 4: Create PRs for major and minor updates
    ```
    python create_prs_to_update_vcs_repositories.py --autoware_repos_file_name files.repos/autoware.repos --targets major minor
    ```

    Example 5: Create PRs for any updates
    ```
    python create_prs_to_update_vcs_repositories.py --autoware_repos_file_name autoware.repos --targets any
    ```
'''


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


# Define the semantic version pattern here
SUPPORTED_SEMANTIC_VERSION_PATTERN = r'\b(?<![^\s])\d+\.\d+\.\d+(?![-\w.+])\b'


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

    def pickup_semver_repositories(self, semantic_version_pattern: str) -> dict[str, str]:
        """
        pick up repositories with semantic version tags

        Args:
            semantic_version_pattern (str): a regular expression pattern for semantic version. e.g. r'(v\d+\.\d+\.\d+)'

        Returns:
            repositories_url_semantic_version_dict (dict[str, str]): a dictionary of GitHub repository URLs and semantic versions. e.g. {'https://github.com/tier4/glog.git': 'v0.6.0'}

        """
        repository_url_version_dict = self._parse_repos()

        repositories_url_semantic_version_dict: dict[str, Optional[str]] = {
            url: (version if re.fullmatch(semantic_version_pattern, version) else None)
            for url, version in repository_url_version_dict.items()
        }
        return repositories_url_semantic_version_dict

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


def parse_args() -> argparse.Namespace:

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

    # Define an argument to specify which version components to check
    args_repo.add_argument(
        '--targets',
        choices=['major', 'minor', 'patch', 'any'],  # Restrict choices to 'major', 'minor', 'patch', and 'any'
        nargs='+',  # Allow multiple values
        default=['any'],  # Default is 'any': in this case, consider any version newer than the current
        help='Specify the version component targets to check for updates (e.g., --targets major minor)'
    )

    # For the Autoware
    args_aw = parser.add_argument_group("Autoware")
    args_aw.add_argument("--autoware_repos_file_name", type=str, default="autoware.repos", help="The path to autoware.repos")

    return parser.parse_args()


def get_logger(verbose: int) -> logging.Logger:

    # Initialize logger depending on the verbosity level
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)

    return logging.getLogger(__name__)


def get_latest_tag(tags: list[str], current_version: str, target_release: str) -> Optional[str]:
    '''
    Description:
        Get the latest tag from the list of tags based on the specified target release type.

    Args:
        tags (list[str]): A list of tags.
        current_version (str): The current version of the repository.
        target_release (str): The type of release to check for updates. Can be 'major', 'minor', 'patch', or 'any'.

    Returns:
        Optional[str]: The latest tag that matches the target release type, or None if not found.

    Raises:
        ValueError: If an invalid target_release is specified.
    '''

    valid_releases = {'major', 'minor', 'patch', 'any'}
    if target_release not in valid_releases:
        raise ValueError(f"Invalid target_release '{target_release}'. Valid options are: {valid_releases}")

    current_ver = version.parse(current_version)
    latest_tag = None

    for tag in tags:
        try:
            parsed_tag = version.parse(tag)
        except (version.InvalidVersion, TypeError):
            continue

        # Skip pre-releases or development versions if not needed
        if parsed_tag.is_prerelease or parsed_tag.is_devrelease:
            continue

        # Determine if the tag matches the required update type
        if target_release == 'major':
            if parsed_tag.major > current_ver.major:
                # Only consider tags with a higher major version
                if latest_tag is None or parsed_tag < version.parse(latest_tag):
                    latest_tag = tag

        elif target_release == 'minor':
            if parsed_tag.major == current_ver.major and parsed_tag.minor > current_ver.minor:
                # Only consider tags with the same major but higher minor version
                if latest_tag is None or parsed_tag < version.parse(latest_tag):
                    latest_tag = tag

        elif target_release == 'patch':
            if (parsed_tag.major == current_ver.major and
                parsed_tag.minor == current_ver.minor and
                parsed_tag.micro > current_ver.micro):
                # Only consider tags with the same major and minor but higher patch version
                if latest_tag is None or parsed_tag < version.parse(latest_tag):
                    latest_tag = tag

        elif target_release == 'any':
            # Consider any version newer than the current version
            if parsed_tag > current_ver:
                if latest_tag is None or parsed_tag < version.parse(latest_tag):
                    latest_tag = tag

    return latest_tag


def create_one_branch(repo: git.Repo, branch_name: str, logger: logging.Logger) -> bool:

    # Check if the branch already exists
    if branch_name in repo.heads:
        logger.info(f"Branch '{branch_name}' already exists.")
        return False
    else:
        # Create a new branch and checkout
        repo.create_head(branch_name)
        logger.info(f"Created a new branch '{branch_name}'")
        return True


def main(args: argparse.Namespace) -> None:

    # Get logger
    logger = get_logger(args.verbose)

    # Get GitHub token
    github_token: str = os.getenv("GITHUB_TOKEN", default=None)
    if github_token == "None":
        raise ValueError("Please set GITHUB_TOKEN as an environment variable")
    github_interface = GitHubInterface(token = github_token)    # cspell: ignore Github

    autoware_repos: AutowareRepos = AutowareRepos(autoware_repos_file_name = args.autoware_repos_file_name)

    # Get the repositories with semantic version tags
    # e.g. {
    #     'https://github.com/user/repo.git': '0.0.1',    # Pattern matched
    #     'https://github.com/user/repo2.git': None,      # Pattern not matched
    # }
    repositories_url_semantic_version_dict: dict[str, str] = autoware_repos.pickup_semver_repositories(semantic_version_pattern = SUPPORTED_SEMANTIC_VERSION_PATTERN)

    # Get reference to the repository
    repo = git.Repo(args.parent_dir)

    # Get all the existing branches
    existing_branches = [r.remote_head for r in repo.remote().refs]

    # Check for each target release type (e.g., major, minor, patch, any)
    for target in args.targets:
        # Check for each repository
        for url, current_version in repositories_url_semantic_version_dict.items():
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

            # Skip if the current version has an invalid format
            if current_version is None:
                logger.debug(f"The current version ({current_version}) format has a mismatched pattern. Skip for this repository:\n    {url}")
                continue

            # get tags of the repository
            tags: list[str] = github_interface.get_tags_by_url(url)

            latest_tag: Optional[str] = get_latest_tag(tags, current_version, target_release=target)

            # Skip if the expected format is not found
            if latest_tag is None:
                logger.debug(f"The latest tag ({latest_tag}) format has a mismatched pattern. Skip for this repository:\n    {url}")
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
                # If the current version is not a valid version, skip this repository
                continue

            # Get repository name
            repo_name: str = github_interface.url_to_repository_name(url)

            # Set branch name
            branch_name: str = f"{args.new_branch_prefix}{repo_name}/{latest_tag}"

            # Skip if the remote branch already exists
            if branch_name in existing_branches:
                logger.info(f"Branch '{branch_name}' already exists on the remote.")
                continue

            # First, create a branch
            create_one_branch(repo, branch_name, logger)

            # Switch to the branch
            repo.heads[branch_name].checkout()

            # Change version in autoware.repos
            autoware_repos.update_repository_version(url, latest_tag)

            # Add
            repo.index.add([args.autoware_repos_file_name])

            # Commit
            title = f"feat({args.autoware_repos_file_name}): {"version" if target == 'any' else target} update {repo_name} to {latest_tag}"
            repo.git.commit(m=title, s=True)

            # Push
            origin = repo.remote(name='origin')
            origin.push(branch_name)

            # Switch back to base branch
            repo.heads[args.base_branch].checkout()

            # Create a PR
            github_interface.create_pull_request(
                repo_name = args.repo_name,
                title = title,
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

    main(parse_args())
