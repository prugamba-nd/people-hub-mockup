#!/bin/sh
# Publish only this standalone mockup. Requires working GitHub CLI access.
set -eu
cd "$(dirname "$0")"
repository="${1:-prugamba-nd/people-hub-mockup}"
case "$repository" in
  */*) ;;
  *) printf '%s\n' 'Pass the repository as OWNER/NAME.' >&2; exit 1 ;;
esac
python3 build.py
github_identity=$(gh api user --jq '"\(.login):\(.id)"')
github_login=${github_identity%:*}
github_id=${github_identity#*:}
if [ ! -d .git ]; then git init -b main; fi
# Use the authenticated account only when an author has not been configured.
# Keep this identity local to the mockup repository.
if ! git config user.name >/dev/null 2>&1; then
  git config --local user.name "$github_login"
fi
if ! git config user.email >/dev/null 2>&1; then
  git config --local user.email "$github_id+$github_login@users.noreply.github.com"
fi
if gh repo view "$repository" >/dev/null 2>&1; then
  printf 'Repository %s already exists. Use a new name to avoid changing an existing project.\n' "$repository" >&2
  exit 1
fi
git add build.py site .gitignore publish.sh NOTES.txt
git commit -m "Add NDT4 People hub mockup"
gh repo create "$repository" --public --source . --remote origin --description 'Static NDT4 People hub mockup'
git push -u origin main
gh api --method POST "repos/$repository/pages" -f build_type=workflow >/dev/null
git add .github/workflows/pages.yml
git commit -m "Enable GitHub Pages deployment"
git push -u origin main
printf '\nRepository: https://github.com/%s\n' "$repository"
printf 'Deployment: https://github.com/%s/actions\n' "$repository"
printf 'Configured Pages URL: '
gh api "repos/$repository/pages" --jq .html_url
