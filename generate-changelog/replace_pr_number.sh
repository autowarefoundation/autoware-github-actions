#!/bin/bash

while read -r line; do
    if echo "$line" | grep -q "(#"; then
        echo "$line" | awk -F '\(#' -v url="$2" '/#[0-9]+/ { print $1 "(" url "/pull/" $2 }'
    else
        echo "$line"
    fi
done <"$1"
