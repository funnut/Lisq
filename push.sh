#!/bin/bash

if [ -z "$1" ]; then
  echo "Użycie: ./push.sh \"wiadomość commita\""
  exit 1
fi

git add .
git commit -m "$1"
git push
