#!/bin/bash
# UWAY Chatbot - Dual Repo Sync Script
# Pushes to both GitHub and BiGnas Git

set -e

echo "🚀 Pushing to GitHub and BiGnas..."
echo ""

# Push to all remotes
git push --all origin

echo ""
echo "✅ Sync complete!"
echo ""
echo "Repositories:"
echo "  - GitHub:  https://github.com/uwayhk/uway-chatbot"
echo "  - BiGnas:  ssh://louie@100.120.207.119/git/uway-chatbot.git"
