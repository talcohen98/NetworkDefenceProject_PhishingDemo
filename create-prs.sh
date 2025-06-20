#!/bin/bash

for i in {1..10}; do
  BRANCH="auto-pr-branch-$i"
  FILE="test-file-$i.txt"

  # צור ענף חדש
  git checkout -b "$BRANCH"

  # צור קובץ חדש
  echo "Auto-generated test content #$i" > "$FILE"

  # בצע commit
  git add "$FILE"
  git commit -m "Test PR #$i"

  # בצע push
  git push origin "$BRANCH"

  # פתח Pull Request
  gh pr create --title "Test PR #$i" --body "This is test PR number $i" --base master --head "$BRANCH"
done

# חזור לענף הראשי
git checkout master
