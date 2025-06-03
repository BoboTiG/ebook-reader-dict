#!/bin/bash
#
# Update associated release commit.
#

for folder in $(find wikidict/lang/* -maxdepth 0 -type d); do
    locale="${folder##*/}"
    [ "${locale}" != "__pycache__" ] && git tag -f -a "${locale}" -m "${locale}"
done

git push -f --tags
