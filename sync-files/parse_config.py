import argparse
import re
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()

    with Path(args.config_file).open() as f:
        config = yaml.safe_load(f)

    for repo_config in config:
        if not re.match(r"^http", repo_config["repository"]):
            repo_config["repository"] = f"https://github.com/{repo_config['repository']}.git"

        if not repo_config.get("ref"):
            repo_config["ref"] = ""

        for item in repo_config["files"]:
            if not item.get("source"):
                raise RuntimeError(f"'source' is not defined in {item}")

            if not item.get("dest"):
                item["dest"] = item["source"]

            if not item.get("replace"):
                item["replace"] = True

            if not item.get("delete-orphaned"):
                item["delete-orphaned"] = True

    print(yaml.dump(config))


if __name__ == "__main__":
    main()
