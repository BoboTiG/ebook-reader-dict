#!/bin/bash
#
# Update associated release commit.
#

for tag in ca en es fr pt sv; do
    git tag -f -a "${tag}" -m "${tag}"
done

git push -f --tags
