#!/bin/bash
# Create the comment body for publish-docs-preview.
# The changed files are read from standard input, one path per line.
# Usage: create-comment.sh <base_url> <commit> [deployment_url] [left_out_files_list]

set -euo pipefail

base_url="${1:?Please input the preview URL as the 1st argument.}"
commit="${2:?Please input the commit as the 2nd argument.}"
deployment_url="${3:-}"
left_out_files_list="${4:-}"

comment_lines=("Documentation URL: <$base_url>")
comment_lines+=("Commit: $commit")
if [ -n "$deployment_url" ]; then
    comment_lines+=("URL of this commit: <$deployment_url>")
fi
comment_lines+=("Modified URLs:")

while IFS= read -r modified_file; do
    if ! [[ $modified_file =~ \.md$ ]]; then
        continue
    fi

    # The same mapping from a file to a page as in deploy-docs/create-doc-comment.sh.
    markdown_path="${modified_file//docs\//}"
    lang=""
    if [[ $markdown_path =~ .*\..*\.md$ ]]; then
        lang=$(echo "$markdown_path" | sed -r 's|.*\.(\w+)\.md|\1|')/
        markdown_path=$(echo "$markdown_path" | sed -r 's|(.*)\.\w+(\.md)|\1\2|')
    fi

    if [[ $markdown_path =~ README\.md$ ]]; then
        url_path=${markdown_path/README.md/}
    elif [[ $markdown_path =~ index\.md$ ]]; then
        url_path=${markdown_path/index.md/}
    else
        url_path=${markdown_path/.md/\/}
    fi

    # The file names come from the pull request. An autolink keeps them from adding Markdown,
    # and a URL with characters that can end the autolink is left out.
    url="$base_url$url_path$lang"
    if [[ $url =~ [[:space:]\<\>\(\)] ]]; then
        continue
    fi
    comment_lines+=("- <$url>")
done

# The site comes from the pull request, so each path is written as code.
if [ -n "$left_out_files_list" ] && [ -s "$left_out_files_list" ]; then
    comment_lines+=("Files larger than 25 MiB, left out of the preview:")
    while IFS= read -r path; do
        if [[ $path =~ [\`[:cntrl:]] ]]; then
            continue
        fi
        comment_lines+=("- \`$path\`")
    done <"$left_out_files_list"
fi

printf "%s\n" "${comment_lines[@]}"
