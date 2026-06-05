#!/bin/bash
# Sync Docusaurus docs to Chatbot Knowledge Base
# Run this after each docs.hkuway.com deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHATBOT_KB="$SCRIPT_DIR/../knowledge_base"
DOCUSAURUS_DOCS="/home/tmp/docs-website/docs"

echo "============================================================"
echo "Uway Docs → Chatbot Knowledge Base Sync"
echo "============================================================"
echo "Source: $DOCUSAURUS_DOCS"
echo "Target: $CHATBOT_KB/uway-docs"
echo ""

# Create/update uway-docs directory
mkdir -p "$CHATBOT_KB/uway-docs"

# Remove old docs (clean sync)
rm -rf "$CHATBOT_KB/uway-docs"/*

# Copy all docs
cp -r "$DOCUSAURUS_DOCS"/* "$CHATBOT_KB/uway-docs/"

# Count synced files
doc_count=$(find "$CHATBOT_KB/uway-docs" -name "*.md" -o -name "*.mdx" | wc -l)

echo "✅ Synced $doc_count documents to $CHATBOT_KB/uway-docs"
echo ""
echo "Knowledge Base Structure:"
echo "  - uway-docs/: $doc_count files (from Docusaurus)"
echo "  - sumsub/: $(find "$CHATBOT_KB/sumsub" -name "*.md" 2>/dev/null | wc -l) files (from Sumsub scraper)"
echo "  - root: $(find "$CHATBOT_KB" -maxdepth 1 -name "*.md" | wc -l) files (legacy)"
echo ""
echo "============================================================"
echo "Next: Restart chatbot to load updated knowledge base"
echo "      docker restart uway-chatbot  # or however it's managed"
echo "============================================================"
