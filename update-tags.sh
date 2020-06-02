#!/bin/bash
#
# Update associated release commit.
#

for tag in ca fr; do
    git tag -f -a "${tag}" -m "${tag}"
done

git push -f --tags
