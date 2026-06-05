#!/usr/bin/env python3
"""
Sumsub Documentation Scraper

Scrapes docs.sumsub.com and converts to markdown format for chatbot knowledge base.
Uses Jina Reader API for clean content extraction.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
import requests

# Jina Reader API - clean content extraction
JINA_READER_BASE = "https://r.jina.ai/"

# Sumsub docs base URL
SUMSUB_DOCS_BASE = "https://docs.sumsub.com"

# Output directory
OUTPUT_DIR = "/root/workspace/uway-chatbot/knowledge_base/sumsub"

# Sitemap - main sections to scrape
SUMSUB_SECTIONS = [
    # Get Started
    {"title": "overview", "url": "/docs/overview"},
    {"title": "key-concepts", "url": "/docs/key-concepts"},
    
    # User Verification
    {"title": "identity-verification", "url": "/docs/identity-verification"},
    {"title": "liveness", "url": "/docs/liveness"},
    {"title": "address-verification", "url": "/docs/address-verification"},
    {"title": "document-verification", "url": "/docs/document-verification"},
    {"title": "reusable-kyc", "url": "/docs/reusable-kyc"},
    
    # Business Verification (KYB)
    {"title": "business-verification", "url": "/docs/business-verification"},
    {"title": "kyb-overview", "url": "/docs/kyb-overview"},
    
    # Transaction Monitoring
    {"title": "transaction-monitoring", "url": "/docs/transaction-monitoring"},
    {"title": "aml-screening", "url": "/docs/aml-screening"},
    {"title": "travel-rule", "url": "/docs/travel-rule-overview"},
    
    # Fraud Prevention
    {"title": "fraud-prevention", "url": "/docs/about-fraud-prevention"},
    {"title": "device-intelligence", "url": "/docs/device-intelligence"},
    {"title": "email-phone-verification", "url": "/docs/email-and-phone-verification"},
    
    # Case Management
    {"title": "case-management", "url": "/docs/case-management"},
    {"title": "applicant-review", "url": "/docs/applicant-review"},
    {"title": "workflow-builder", "url": "/docs/workflow-builder"},
    
    # Account Management
    {"title": "account-management", "url": "/docs/account"},
    {"title": "users-roles", "url": "/docs/users-and-roles"},
    
    # Developer
    {"title": "api-overview", "url": "/docs/api-overview"},
    {"title": "webhooks", "url": "/docs/webhooks"},
    {"title": "sdks", "url": "/docs/sdks"},
]

def fetch_with_jina(url: str) -> str:
    """Fetch URL content using Jina Reader"""
    try:
        full_url = f"{JINA_READER_BASE}{SUMSUB_DOCS_BASE}{url}"
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  ⚠️  Failed to fetch {url}: {e}")
        return ""

def clean_content(content: str, title: str) -> str:
    """Clean and format content for knowledge base"""
    # Add frontmatter
    frontmatter = f"""---
source: sumsub
original_url: {SUMSUB_DOCS_BASE}/docs/{title}
scraped_at: {datetime.now().isoformat()}
---

"""
    # Add title if not present
    if not content.startswith("#"):
        content = f"# Sumsub: {title.replace('-', ' ').title()}\n\n" + content
    
    return frontmatter + content

def scrape_section(section: dict) -> bool:
    """Scrape a single section"""
    title = section["title"]
    url = section["url"]
    
    print(f"📄 Scraping: {title}")
    
    content = fetch_with_jina(url)
    if not content or len(content) < 100:
        print(f"  ⚠️  Empty or too short, skipping")
        return False
    
    cleaned = clean_content(content, title)
    
    # Save to file
    output_path = Path(OUTPUT_DIR) / f"{title}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    
    print(f"  ✅ Saved: {output_path}")
    return True

def generate_index():
    """Generate index.json for quick reference"""
    index = {
        "source": "sumsub-docs",
        "scraped_at": datetime.now().isoformat(),
        "total_docs": 0,
        "sections": []
    }
    
    for md_file in Path(OUTPUT_DIR).glob("*.md"):
        index["total_docs"] += 1
        index["sections"].append({
            "title": md_file.stem,
            "file": md_file.name,
            "size": md_file.stat().st_size
        })
    
    index_path = Path(OUTPUT_DIR) / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
    print(f"\n📑 Generated index: {index_path}")
    return index

def main():
    """Main scraping function"""
    print("=" * 60)
    print("Sumsub Documentation Scraper")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR}")
    print(f"Sections to scrape: {len(SUMSUB_SECTIONS)}")
    print()
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Scrape each section
    success_count = 0
    for section in SUMSUB_SECTIONS:
        if scrape_section(section):
            success_count += 1
    
    # Generate index
    index = generate_index()
    
    print()
    print("=" * 60)
    print(f"✅ Complete: {success_count}/{len(SUMSUB_SECTIONS)} sections scraped")
    print(f"📊 Total docs: {index['total_docs']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
