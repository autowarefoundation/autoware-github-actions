#!/bin/bash
# Search for packages that have been modified from the base branch.
# Usage: get-modified-packages.sh <base_branch>

set -e

# Parse arguments
args=()
while [ "${1-}" != "" ]; do
    case "$1" in
    *)
        args+=("$1")
        ;;
    esac
    shift
done

# base_branch is like "origin/main"
base_branch="${args[0]}"
echo "base_branch: $base_branch"

# Check args
if [ "$base_branch" = "" ]; then
    echo -e "\e[31mPlease input a valid base_branch as the 1st argument.\e[m"
    exit 1
fi

function find_package_dir() {
    [ "$1" == "" ] && return 1

    target_dir=$(dirname "$1")
    while true; do
        # Output package name if package.xml found
        if [ -f "$target_dir/package.xml" ]; then
            if [ ! -f "$target_dir/COLCON_IGNORE" ]; then
                echo "$target_dir"
                return 0
            fi
        fi

        # Exit if no parent found
        parent_dir=$(dirname "$target_dir")
        if [ "$parent_dir" = "$target_dir" ]; then
            return 0
        fi

        # Move to parent dir
        target_dir=$parent_dir
    done

    return 1
}

# Function to check if the base ref SHA is in the commit history
check_base_ref_in_history() {
    git rev-list HEAD | grep -q "$(git rev-parse "$base_branch")"
}

# Fetch the initial shallow clone depth
depth=1

# Loop to deepen the fetch until the base ref SHA is included
while ! check_base_ref_in_history; do
    depth=$((depth * 2))
    # NOTE: need to specify the bese_branch
    # NG: git fetch origin/main --deepen=1
    # OK: git fetch origin main --deepen=1
    # => $base_branch need to be transformed from "origin/main" to "origin main"
    git fetch --deepen=$depth
done

# Get the modified files between base ref and HEAD
modified_files=$(git diff --name-only $base_branch"...HEAD)

# Find modified packages
modified_package_dirs=()
for modified_file in $modified_files; do
    modified_package_dir=$(find_package_dir "$modified_file")

    if [ "$modified_package_dir" != "" ]; then
        modified_package_dirs+=("$modified_package_dir")
    fi
done

# Get package names from paths
if [ "${#modified_package_dirs[@]}" != "0" ]; then
    modified_packages=$(colcon list --names-only --paths "${modified_package_dirs[@]}")
fi

# Output
# shellcheck disable=SC2086
printf "%s " $modified_packages | sed 's/\s*$//'
