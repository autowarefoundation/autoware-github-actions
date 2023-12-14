import argparse
import os
import re
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    args = parser.parse_args()

    with Path(args.config_file).open() as f:
        config = yaml.safe_load(f)

    if config is None:
        return

    for repo_config in config:
        if not re.match(r"^http", repo_config["repository"]):
            repo_config["repository"] = f"https://github.com/{repo_config['repository']}.git"

        if "ref" not in repo_config:
            repo_config["ref"] = ""

        for item in repo_config["files"]:
            if "source" not in item:
                raise RuntimeError(f"'source' is not defined in {item}")

            if "dest" not in item:
                item["dest"] = item["source"]

            if "replace" not in item:
                item["replace"] = True

            if "delete-orphaned" not in item:
                item["delete-orphaned"] = True

            if "pre-commands" not in item:
                item["pre-commands"] = ""

            if "post-commands" not in item:
                item["post-commands"] = ""

            if "source-dir" in repo_config:
                item["source"] = os.path.join(repo_config["source-dir"], item["source"])

    print(yaml.dump(config))


if __name__ == "__main__":
    main()
