#!/bin/bash
# Search for packages that have been modified from the base branch.
# Usage: get-modified-packages.sh <base_branch>

set -e

# Parse arguments
args=()
while [ "${1:-}" != "" ]; do
    case "$1" in
    *)
        args+=("$1")
        ;;
    esac
    shift
done

base_branch="${args[0]}"

# Check args
if [ "$base_branch" = "" ]; then
    echo -e "\e[31mPlease input a valid base_branch as the 1st argument.\e[m"
    exit 1
fi

function find_package_name() {
    [ "$1" == "" ] && return 1

    target_dir=$(dirname "$1")
    while true; do
        parent_dir=$(dirname "$target_dir")

        # Output package name if package.xml found
        if [ -f "$parent_dir/package.xml" ]; then
            if [ ! -f "$parent_dir/COLCON_IGNORE" ]; then
                xmllint --xpath "package/name/text()" "$parent_dir/package.xml"
                return 0
            fi
        fi

        # Exit if no parent found
        if [ "$parent_dir" = "$target_dir" ]; then
            return 0
        fi

        # Move to parent dir
        target_dir=$parent_dir
    done

    return 1
}

# Find modified files from base branch
modified_files=$(git diff --name-only "$base_branch"...HEAD)
# Find modified packages
modified_package_names=()
for modified_file in $modified_files; do
    modified_package_name=$(find_package_name "$modified_file")
    if [ "$modified_package_name" != "" ]; then
        modified_package_names+=("$modified_package_name")
    fi
done

#
# Output
# shellcheck disable=SC2046
echo ::set-output name=modified-packages::$(printf "%s\n" "${modified_package_names[@]}" | sort -u)
