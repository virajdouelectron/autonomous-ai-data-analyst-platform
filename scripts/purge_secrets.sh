#!/usr/bin/env bash
set -euo pipefail

echo "This script shows recommended commands to purge the removed .github/workflows/.env from git history using git-filter-repo or BFG."
echo "DO NOT RUN THIS IN A CI; run locally where you have credentials and backups."

echo
echo "Option A: git-filter-repo (recommended)"
echo "Install: pip install git-filter-repo"
echo
echo "Run the following in a cloned repo (backup first):"
cat <<'EOF'
# remove the specific file from all history
git filter-repo --path .github/workflows/.env --invert-paths

# cleanup and force-push to origin
git push --force --all
git push --force --tags
EOF

echo
echo "Option B: BFG Repo-Cleaner"
echo "Install: https://rtyley.github.io/bfg-repo-cleaner/"
cat <<'EOF'
# mirror the repo
git clone --mirror git@github.com:yourname/yourrepo.git
cd yourrepo.git
# remove the file
bfg --delete-files .github/workflows/.env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
EOF

echo
echo "After purging history: rotate any exposed credentials immediately (Gemini API key, Supabase anon key)."
echo "Also add the new credentials to your GitHub repository Secrets (Settings → Secrets) as GEMINI_API_KEY, SUPABASE_URL, and SUPABASE_ANON_KEY."

echo
echo "Script finished. Review the steps above and run them manually after taking a backup."
