#!/bin/bash
# UWAY Chatbot - Dual Repo Sync Script
# Pushes to both GitHub and BiGnas (louienas)

set -e

echo "🚀 Pushing to GitHub and BiGnas..."
echo ""

# Push to GitHub (uses SSH key)
echo "📦 Pushing to GitHub..."
git push origin main
echo "   ✅ GitHub: https://github.com/uwayhk/uway-chatbot"
echo ""

# Push to BiGnas (uses password)
echo "📦 Pushing to BiGnas (louienas)..."
GIT_SSH_COMMAND="sshpass -p 'Adminlizhe123!' ssh -o StrictHostKeyChecking=no" git push nas main
echo "   ✅ BiGnas: ssh://louieadmin@100.120.207.119/volume2/homes/louieadmin/git/uway-chatbot.git"
echo ""

echo "✅ Sync complete!"
