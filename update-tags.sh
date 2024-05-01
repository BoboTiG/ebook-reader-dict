#!/bin/bash
#
# Update associated release commit.
#

# XXX_LOCALES
for tag in ca da de el en es fr it no pt ro ru sv; do
    git tag -f -a "${tag}" -m "${tag}"
done

git push -f --tags
