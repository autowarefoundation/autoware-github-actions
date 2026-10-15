#!/bin/bash
# Refuse a built site that is not plain static files.
# The site comes from the code of a pull request, so treat it as untrusted data.
# Usage: check-site.sh <site_dir>

set -euo pipefail

site_dir="${1:?Please input the site directory as the 1st argument.}"

fail() {
    echo "::error::The preview was not published: $1"
    exit 1
}

if [ ! -d "$site_dir" ] || [ -L "$site_dir" ]; then
    fail "the site is not a directory"
fi

if [ ! -f "$site_dir/index.html" ]; then
    fail "the site has no index.html"
fi

# Links can point outside the site, and hidden files are not part of an MkDocs site.
bad_path=$(find "$site_dir" -mindepth 1 \( -type l -o -name '.*' -o \( ! -type f ! -type d \) \) -print -quit)
if [ -n "$bad_path" ]; then
    fail "the site contains a link, a hidden file, or a special file: ${bad_path#"$site_dir"/}"
fi

# Cloudflare Pages reads these files at the root of a deployment.
# _worker.js runs as server code, and the others change headers, redirects, and routes.
for name in _worker.js _routes.json _headers _redirects; do
    if [ -e "$site_dir/$name" ]; then
        fail "the site contains the Cloudflare Pages control file $name"
    fi
done

echo "The site passed the checks."
