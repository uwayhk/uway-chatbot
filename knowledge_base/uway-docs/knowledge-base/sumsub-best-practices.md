---
sidebar_position: 5
---

# Sumsub Best Practices

**Implementation guide for Sumsub KYC/AML verification platform.**

## Overview

Sumsub is a leading identity verification and compliance platform providing KYC, AML, and fraud prevention services. This guide covers best practices for integrating Sumsub into your compliance workflow.

## Core Features

### 1. Identity Verification

- **Document Verification**: 5,000+ document types from 220+ countries
- **Selfie Verification**: Facial recognition with liveness detection
- **Data Extraction**: OCR for automatic data capture
- **Authenticity Checks**: Security feature validation

### 2. AML Screening

- **Sanctions Lists**: OFAC, UN, EU, HKSAR, MAS
- **PEP Database**: Global politically exposed persons
- **Adverse Media**: Negative news screening
- **Watchlists**: Custom and third-party lists

### 3. Risk Scoring

- Automated risk assessment based on:
  - Document authenticity
  - Geographic risk
  - PEP/sanctions matches
  - Behavioral patterns

## Implementation Guide

### API Integration

```python
# Example: Create applicant
import requests

response = requests.post(
    'https://api.sumsub.com/resources/applicants',
    headers={
        'X-App-Token': 'YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    json={
        'externalUserId': 'user_123',
        'levelName': 'basic-kyc-level'
    }
)
```

### Webhook Configuration

Configure webhooks for real-time status updates:
- `applicantReviewed`: Verification complete
- `applicantPending`: Manual review required
- `applicantCreated`: New applicant created

### Level Configuration

**Recommended Levels:**

| Level | Use Case | Requirements |
|-------|----------|--------------|
| Basic | Low-risk users | ID + Selfie |
| Standard | Most users | ID + Selfie + Address |
| Enhanced | High-risk | Full DD + Source of funds |

## Best Practices

### 1. User Experience

- Progressive verification (start with basic, upgrade as needed)
- Clear instructions for document capture
- Mobile-optimized flow
- Retry logic for failed attempts

### 2. Compliance

- Document retention per local regulations
- Audit trail for all verification attempts
- Manual review queue for edge cases
- Regular level configuration reviews

### 3. Fraud Prevention

- Enable liveness detection
- Set up duplicate detection
- Monitor for synthetic identities
- Implement velocity checks

### 4. Performance Optimization

- Use SDK for mobile apps
- Implement retry with exponential backoff
- Cache applicant status
- Monitor API rate limits

## Hong Kong Specific

**AMLO Compliance:**
- Ensure document types meet CIP requirements
- Retain verification records for 5+ years
- Implement ongoing monitoring workflows

## Singapore Specific

**MAS Notice 626:**
- Risk-based level assignment
- Enhanced DD for high-risk customers
- Regular sanctions re-screening

## Troubleshooting

### Common Issues

**Document Rejection:**
- Check document expiry date
- Verify document type is supported
- Ensure image quality meets requirements

**False Positive PEP Matches:**
- Review matching criteria
- Implement manual review workflow
- Document decision rationale

---

*Last updated: May 2025*
