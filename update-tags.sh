#!/bin/bash
#
# Update associated release commit.
#

for tag in fr; do
    git tag -f -a "${tag}" -m "${tag}"
done

git push -f --tags
