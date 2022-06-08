import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-xml", required=True)
    parser.add_argument("--exclude-packages", required=False, nargs="*", type=str)
    args = parser.parse_args()

    exclude_packages = args.exclude_packages if args.exclude_packages is not None else []
    data_lines = None
    with Path(args.package_xml).open(mode='r') as f:
        data_lines = f.readlines()

    with Path(args.package_xml).open('w') as f:
        for line in data_lines:
            # write without exec depend
            if re.match(r'\s*<exec_depend>\s*[a-zA-Z_0-9\-]+\s*</exec_depend>\n', line) is None:
                f.write(line)
            else:
                # evaluate exclude packages
                for ex in exclude_packages:
                    if ex in line:
                        f.write(line)


if __name__ == "__main__":
    main()
