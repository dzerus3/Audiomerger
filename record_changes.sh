#!/bin/sh

# Do the setup if there was no git repo
ls .git 2> /dev/null || git init 2> /dev/null
touch .dirtree
git add .dirtree

files_before=$(wc -l .dirtree)

find * -type f > .dirtree

files_edited=$(wc -l .dirtree)

echo "Previous amount of files: $files_before"
echo "Amount of files now: $files_edited"

# If there are any changes, commit them with whichever message was specifiec as first argument.
git diff --quiet || git commit .dirtree --quiet -m "$1" 2> /dev/null
