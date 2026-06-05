#!/bin/bash
# UWAY Chatbot - GitHub Repository Setup Script
# Run this after creating the repository on GitHub

set -e

REPO_URL="${1:-git@github.com:louiezhelee/uway-chatbot.git}"

echo "🚀 Setting up GitHub repository..."
echo ""

# Remove existing remote if any
git remote remove origin 2>/dev/null || true

# Add new remote
git remote add origin "$REPO_URL"

# Rename branch to main
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "Repository: $REPO_URL"
echo "View at: ${REPO_URL%.git}"
echo ""
echo "Next steps:"
echo "1. Add repository description on GitHub"
echo "2. Add topics: ai, chatbot, compliance, fintech, hong-kong"
echo "3. Enable GitHub Pages if needed"
echo "4. Add LICENSE file if needed"
