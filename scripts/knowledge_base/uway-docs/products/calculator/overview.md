---
sidebar_position: 3
---

# Calculator (Invoice Dashboard)

## 📖 Product Overview

**Invoice Dashboard 2.0** is a multi-tenant SaaS billing management system designed for Sumsub resellers and service providers.

### Core Value Proposition

- **Transparent Billing:** Real-time visibility into every KYC/AML consumption with detailed breakdowns
- **Multi-User Support:** Role-based access control (Admin/User) with isolated data views
- **Flexible Pricing:** Different unit prices for the same service across different customers
- **Automated Reporting:** Monthly summaries with cost calculations and service breakdowns
- **Audit-Ready:** Complete data追溯 with timestamped records

---

## 🎯 Target Users

| User Type | Use Case |
|-----------|----------|
| **Sumsub Resellers** | Track consumption across multiple end customers with custom pricing |
| **SaaS Providers** | Manage service usage billing for B2B customers |
| **Compliance Teams** | Generate audit-ready billing reports for regulatory reviews |

---

## ✨ Key Features

### User & Permission Management
- Multi-user system with unlimited accounts
- RBAC: Admin (full access) vs User (own data only)
- Secure password hashing (Werkzeug)
- 7-day session expiry with CSRF protection

### Service & Pricing Management
- Global service directory maintained by admins
- Flexible service assignment per customer
- **Snapshot pricing:** Historical records preserve original unit prices even after pricing changes

### Data Import & Processing
- CSV file upload with drag-and-drop
- Auto-validation for service existence and user permissions
- Batch processing support (max 10MB files)
- Complete file upload history tracking

### Automated Reporting
- Monthly aggregation with cost calculations
- Service-level breakdowns
- Quick filtering by year/month
- CSV export for further analysis

---

## 🏗️ Technical Architecture

| Layer | Technology |
|-------|------------|
| **Frontend** | Bootstrap 5 + Jinja2 |
| **Backend** | Flask 3.0+ |
| **Database** | SQLAlchemy + SQLite |
| **Data Processing** | Pandas |
| **Web Server** | Gunicorn + Nginx |
| **Process Manager** | PM2 |

### Database Schema

| Table | Purpose |
|-------|---------|
| `User` | User accounts with role flags |
| `Service` | Global service directory |
| `UserService` | User-service assignments |
| `ServicePricing` | Per-user pricing configurations |
| `UsageRecord` | Individual usage entries with price snapshots |
| `MonthlySummary` | Pre-aggregated monthly statistics |
| `UploadFile` | File upload tracking |

---

## 🚀 Quick Start

### For Admins

1. Create global services in the Service Directory
2. Create user accounts
3. Assign services to each user
4. Configure unit prices per user-service pair
5. System ready for data ingestion

### For End Users

1. Upload CSV files with columns: `serviceName`, `clientId`, `quantity`, `serviceTime`
2. System auto-validates and processes data
3. View monthly reports with cost breakdowns
4. Export data for further analysis

---

## 🔐 Security Features

- **SQL Injection Protection:** SQLAlchemy ORM with parameterized queries
- **XSS Prevention:** Jinja2 auto-escaping
- **CSRF Protection:** Flask session protection
- **Data Isolation:** Users can only access their own data
- **Environment-Based Secrets:** SECRET_KEY from environment variables

---

## 📊 Performance Metrics

| Operation | Latency |
|-----------|---------|
| User Login | < 100ms |
| CSV Upload (1000 rows) | < 1s |
| Monthly Report Generation | < 500ms |
| Report Query | < 50ms |

---

## 📁 File Structure

```
calculator/
├── invoice_dashboard/
│   ├── app.py                    # Flask application
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── routes_auth.py            # Authentication routes
│   ├── routes_dashboard.py       # Dashboard routes
│   ├── routes_upload.py          # CSV upload routes
│   ├── routes_reports.py         # Report generation routes
│   └── templates/                # Jinja2 templates
├── data/
│   ├── input/                    # Uploaded CSV files
│   └── output/                   # Generated reports
└── requirements.txt              # Python dependencies
```

---

## 🔗 Related Resources

- **Source Code:** Available in internal repository
- **Deployment Guide:** Contact Operations Team
- **API Documentation:** Coming Soon

---

*Last Updated: 2026-05-02 | Version: 2.0 | Status: ✅ Production Ready*
