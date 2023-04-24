#!/usr/bin/env python3

# Copyright 2023 The Autoware Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree


class CodeOwners:

    def __init__(self):
        self.maintainers = []
        self.users = []
        self.groups = []
        self.parent = None

    def load_package_xml(self, path: Path):
        maintainers = ElementTree.parse(path).getroot().findall("maintainer")
        self.maintainers = [maintainer.attrib["email"] for maintainer in maintainers]

    def load_codeowners_yaml(self, path: Path):
        data = yaml.safe_load(path.read_text())
        self.users.extend(data.get("users", []))
        self.groups.extend(data.get("groups", []))

    def update_groups(self, groups):
        for group in self.groups:
            self.users.extend(groups[group])

    def update_parent(self, owners, path):
        for parent in path.parents:
            if parent in owners:
                self.parent = owners[parent]
                return

    def resolve_codeowners(self):
        users = self.parent.resolve_codeowners() if self.parent else []
        return users + self.users


parser = ArgumentParser()
parser.add_argument("path")
parser.add_argument("--groups")
args = parser.parse_args()
root = Path(args.path)

groups = yaml.safe_load(Path(args.groups).read_text()) if args.groups else {}
owners = defaultdict(CodeOwners)

for path in root.glob("**/package.xml"):
    owners[path.parent].load_package_xml(path)
for path in root.glob("**/codeowners.yaml"):
    owners[path.parent].load_codeowners_yaml(path)

for path in owners:
    owners[path].update_groups(groups)
for path in owners:
    owners[path].update_parent(owners, path)

for path in sorted(owners.keys()):
    owner = owners[path]
    if not owner.maintainers:
        continue
    users = set(owner.maintainers + owner.resolve_codeowners())
    print(path.relative_to(root) / "**", " ".join(users))
