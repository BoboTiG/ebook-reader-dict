#!/bin/bash
#
# Update associated release commit.
#

for tag in ca en es fr it no pt sv; do
    git tag -f -a "${tag}" -m "${tag}"
done

git push -f --tags
