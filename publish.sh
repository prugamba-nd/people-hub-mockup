#!/bin/sh
# Publish the static site from gh-pages without custom workflow permissions.
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
repository_exists=false
if gh repo view "$repository" >/dev/null 2>&1; then repository_exists=true; fi
if git remote get-url origin >/dev/null 2>&1; then
  origin_url=$(git remote get-url origin)
  case "$origin_url" in
    "https://github.com/$repository"|"https://github.com/$repository.git"|"git@github.com:$repository.git") ;;
    *) printf 'Origin points to a different repository: %s\n' "$origin_url" >&2; exit 1 ;;
  esac
fi
git add build.py site .gitignore publish.sh NOTES.txt
# Stage the removal of the previous, unused workflow if it is tracked.
if git ls-files --error-unmatch .github/workflows/pages.yml >/dev/null 2>&1; then
  git add -u -- .github/workflows/pages.yml
fi
if ! git diff --cached --quiet; then
  git commit -m "Prepare People hub for branch-based publication"
fi
if [ "$repository_exists" = false ]; then
  gh repo create "$repository" --public --source . --remote origin --description 'Static NDT4 People hub mockup'
elif ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/$repository.git"
fi

# Only the generated site enters gh-pages. Source history and the rejected
# workflow commit stay off the publishing branch. No history is force-pushed.
site_tree=$(git rev-parse HEAD:site)
if git ls-remote --exit-code origin refs/heads/gh-pages >/dev/null 2>&1; then
  git fetch origin refs/heads/gh-pages
  pages_parent=$(git rev-parse FETCH_HEAD)
  if [ "$(git rev-parse "$pages_parent^{tree}")" != "$site_tree" ]; then
    pages_commit=$(printf '%s\n' 'Update static People hub' | git commit-tree "$site_tree" -p "$pages_parent")
    git push origin "$pages_commit:refs/heads/gh-pages"
  fi
else
  pages_commit=$(printf '%s\n' 'Publish static People hub' | git commit-tree "$site_tree")
  git push origin "$pages_commit:refs/heads/gh-pages"
fi

pages_method=POST
if gh api "repos/$repository/pages" >/dev/null 2>&1; then pages_method=PUT; fi
gh api --method "$pages_method" "repos/$repository/pages" \
  -f build_type=legacy -f 'source[branch]=gh-pages' -f 'source[path]=/' >/dev/null
printf '\nRepository: https://github.com/%s\n' "$repository"
printf 'Configured Pages URL: '
gh api "repos/$repository/pages" --jq .html_url
