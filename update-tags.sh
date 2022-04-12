#!/bin/bash
#
# Update associated release commit.
#

for tag in ca de el en es fr it no pt sv ru; do
    git tag -f -a "${tag}" -m "${tag}"
done

git push -f --tags
