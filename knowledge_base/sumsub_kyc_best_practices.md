# Sumsub KYC Best Practices

## Overview
Sumsub is a leading identity verification and KYC/AML compliance platform used by financial institutions, fintechs, and crypto businesses worldwide.

## Key Components of an Effective KYC Program (Sumsub Framework)

### 1. Customer Identification Program (CIP)
- **Collect and verify identifying information**: name, date of birth, address, nationality
- **Use reliable, independent documents or electronic verification methods**
- **Match against sanctions lists**: OFAC, UN, HKMA/SMAS lists for Hong Kong, EU sanctions
- **Document types accepted**:
  - Government-issued ID (passport, national ID, driver's license)
  - Proof of address (utility bill, bank statement < 3 months old)
  - Selfie/liveness check for identity verification

### 2. Risk-Based Approach (RBA)

| Risk Level | Enhanced Due Diligence (EDD) | Simplified Measures |
|------------|------------------------------|---------------------|
| High | Enhanced verification, ongoing monitoring, source of wealth verification | Not applicable |
| Medium | Standard procedures + periodic review (annual) | Not applicable |
| Low | Basic CDD | Streamlined verification |

**Risk Factors to Consider**:
- Customer type (individual vs. corporate, PEP status)
- Geographic location (high-risk jurisdictions)
- Product/service type (crypto, remittance, high-value transactions)
- Transaction patterns and volumes
- Delivery channel (face-to-face vs. non-face-to-face)

### 3. Core Documentation Requirements

**For Individuals**:
- Government-issued ID (passport/HKID/national ID)
- Proof of address (utility bill, bank statement < 3 months)
- Selfie/liveness verification
- Source of funds documentation (for high-risk/high-value)

**For Corporate Entities**:
- Certificate of incorporation
- Business registration certificate
- Memorandum & Articles of Association
- Register of directors and shareholders
- Beneficial ownership declaration (UBO > 25%)
- Proof of business address
- Source of wealth documentation for UBOs

### 4. Recommended Implementation Steps

1. **Define scope** based on your business type and regulatory obligations (HKMA, SFC, MAS, etc.)
2. **Establish policies** with clear procedures and escalation paths
3. **Implement technology** for document verification and screening (e.g., Sumsub API)
4. **Train staff** on identification and suspicious activity reporting
5. **Conduct ongoing monitoring** and periodic reviews
6. **Maintain records** for statutory retention periods (typically 5-7 years in HK)

### 5. Jurisdiction-Specific Notes

**Hong Kong**:
- HKMA AML/CFT guidelines apply to licensed institutions
- SFC requirements for registered entities (Type 1, 4, 7, 9 licenses)
- Suspicious Transaction Reports (STRs) to JFIU (Joint Financial Intelligence Unit)
- AMLO (Anti-Money Laundering Ordinance Cap. 615) requirements
- Minimum retention period: 5 years after relationship ends

**Singapore**:
- MAS Notice 626 (Prevention of Money Laundering and Countering the Financing of Terrorism)
- CDIC (Credit Deposits Insurance Corporation) for deposit-taking institutions
- STRs to CAD (Commercial Affairs Department)
- Minimum retention period: 5 years

**Cross-Border Considerations**:
- FATF (Financial Action Task Force) recommendations
- Correspondent banking due diligence
- Sanctions screening (OFAC, UN, EU, HKMA)

### 6. Technology Integration (Sumsub API)

**Key Features**:
- Automated document verification with AI-powered fraud detection
- Real-time sanctions and PEP screening
- Liveness detection and facial recognition
- Ongoing monitoring and periodic review automation
- Audit trail and compliance reporting

**Implementation Workflow**:
1. Customer onboarding → Document capture
2. Automated verification → Risk scoring
3. Manual review (if flagged) → Approval/rejection
4. Ongoing monitoring → Periodic review triggers
5. Record keeping → Regulatory reporting

### 7. Red Flags to Watch

**Shell Company Characteristics**:
- Minimal physical presence
- Nominee directors/shareholders
- No clear business purpose
- Complex ownership structures

**Documentation Issues**:
- Inconsistent or unverifiable documentation
- Altered/forged documents
- Reluctance to provide required information
- Unusual ownership structures

**Behavioral Indicators**:
- Transactions inconsistent with customer profile
- Rapid movement of funds
- Use of multiple accounts to avoid thresholds
- Negative news/regulatory actions

### 8. Sumsub-Specific Best Practices

**Optimization Tips**:
- Configure verification levels based on risk tiers
- Set up custom workflows for different customer segments
- Enable ongoing monitoring for high-risk customers
- Use webhooks for real-time status updates
- Integrate with your existing CRM/compliance systems

**Compliance Metrics to Track**:
- Average verification time
- False positive/negative rates
- Manual review rate
- Customer drop-off rate
- Regulatory audit findings

---

## References
- FATF Recommendations (2012, updated 2023)
- HKMA Supervisory Policy Manual (SPM) Section 12
- MAS Notice 626
- EU AMLD5/AMLD6
- FinCEN Guidance
