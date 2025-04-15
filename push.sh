#!/bin/bash

if [ -z "$1" ]; then
  msg="File(s) updated"
else
  msg="$1"
fi

git add .
git commit -m "$msg"
git push
