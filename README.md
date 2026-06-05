# UWAY Compliance Chatbot

🛡️ AI-powered financial compliance assistant for AML/KYC regulations in Hong Kong

![Status](https://img.shields.io/badge/status-production-green)
![License](https://img.shields.io/badge/license-proprietary-blue)
![Model](https://img.shields.io/badge/model-Gemini%202.5%20Pro-orange)

## Live Demo

- **Production**: https://chatbot.hkuway.com
- **Backend API**: http://16.163.147.170/api/health

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                    │
│                          │                                      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  https://chatbot.hkuway.com                               │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTPS (443)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  GCP Instance (34.96.220.45) - Frontend                         │
│  ┌─────────────────┐                                            │
│  │  nginx          │ SSL termination (Certbot)                  │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  Streamlit :8501│ Chat UI + Knowledge Base                   │
│  └────────┬────────┘                                            │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTP (80)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  AWS EC2 (16.163.147.170) - Backend                             │
│  ┌─────────────────┐                                            │
│  │  nginx :80      │ API proxy                                  │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  FastAPI :8000  │ REST API                                   │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  Provider Mgr   │ LLM Router                                 │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  Vertex AI      │ Gemini 2.5 Pro                             │
│  └─────────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Features

- ✅ **RAG-powered responses** - 67 compliance documents in knowledge base
- ✅ **Multi-provider LLM** - Gemini 2.5 Pro via Vertex AI with failover support
- ✅ **Source citations** - Every answer includes document references
- ✅ **Confidence scoring** - Response reliability indicators
- ✅ **Session management** - Conversation history per user
- ✅ **HKMA/SFC compliant** - Aligned with Hong Kong financial regulations

## Tech Stack

| Component | Technology | Provider |
|-----------|-----------|----------|
| Frontend | Streamlit 1.57+ | Python |
| Backend | FastAPI + Uvicorn | Python |
| LLM | Gemini 2.5 Pro | Google Vertex AI |
| Auth | Service Account JWT | Google Cloud |
| Knowledge Base | Markdown + Redis | Local + Cache |
| Frontend Hosting | GCP + nginx | Google Cloud |
| Backend Hosting | EC2 t3.micro | AWS |

## Project Structure

```
uway-chatbot/
├── aws_backend/              # Backend API (AWS EC2)
│   ├── main.py              # FastAPI application
│   ├── provider_manager.py  # LLM provider abstraction
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   ├── deploy.sh           # Deployment script
│   └── nginx.conf          # Nginx proxy config
│
├── gcp_frontend/            # Frontend UI (GCP)
│   ├── app.py              # Streamlit application
│   ├── requirements.txt    # Python dependencies
│   ├── deploy.sh          # Deployment script
│   └── DEPLOYMENT.md      # Deployment guide
│
├── knowledge_base/          # Compliance documents
│   ├── hkmaguidelines/     # HKMA guidelines
│   ├── sfc_rules/         # SFC regulations
│   └── sumsub/            # KYC vendor docs
│
├── scripts/                # Utility scripts
│   └── ingest_kb.py       # Knowledge base ingestion
│
├── README.md              # This file
├── DEPLOYMENT.md          # Full deployment guide
├── API.md                 # API documentation
└── ARCHITECTURE.md        # Architecture details
```

## Quick Start

### Prerequisites

- AWS Account with EC2 access
- GCP Project with Vertex AI enabled
- SSH keys for both instances

### Backend Deployment (AWS EC2)

```bash
# 1. SSH to EC2
ssh -i /path/to/key.pem ubuntu@16.163.147.170

# 2. Clone and setup
cd /opt/uway-chatbot
sudo systemctl restart uway-chatbot

# 3. Verify
curl http://localhost:8000/api/health
```

### Frontend Deployment (GCP)

```bash
# 1. SSH to GCP
ssh -i /path/to/gcp_key louie@34.96.220.45

# 2. Restart Streamlit
sudo systemctl restart uway-chatbot-frontend

# 3. Verify
curl http://localhost:8501
```

## API Reference

### Health Check

```bash
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "uway-chatbot-backend",
  "version": "1.0.0"
}
```

### Chat Endpoint

```bash
POST /api/chat
Content-Type: application/json

{
  "message": "What is Sumsub?",
  "session_id": "user123"
}
```

Response:
```json
{
  "answer": "Sumsub is a global RegTech company...",
  "sources": ["sumsub_overview.md", "kyc_requirements.md"],
  "confidence_score": 0.92
}
```

## Configuration

### Environment Variables (Backend)

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account key | `/opt/uway-chatbot/vertex-key.json` |
| `GEMINI_MODEL` | Model name | `gemini-2.5-pro` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### GCP Service Account

The backend uses a GCP service account for Vertex AI access:

- **Email**: `vertex-express@uway-hq-493308.iam.gserviceaccount.com`
- **Project**: `uway-hq-493308`
- **Required IAM Role**: `roles/aiplatform.user`

## Monitoring

### Service Status

```bash
# Backend (EC2)
sudo systemctl status uway-chatbot

# Frontend (GCP)
sudo systemctl status uway-chatbot-frontend
```

### Logs

```bash
# Backend logs
sudo journalctl -u uway-chatbot -f

# Frontend logs
tail -f /tmp/streamlit.log
```

## Security

- ✅ Service account keys stored with 600 permissions
- ✅ HTTPS enforced via Certbot SSL
- ✅ API rate limiting configured
- ✅ No API keys in source code
- ✅ Security group restricts SSH access

## Cost

| Resource | Tier | Monthly Cost |
|----------|------|--------------|
| AWS EC2 t3.micro | Free Tier | $0 |
| GCP e2-micro | Free Tier | $0 |
| Vertex AI | Free Tier (60 req/min) | $0 |
| **Total** | | **~$0** |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend connection failed | Check EC2 security group allows port 80 |
| Gemini API error | Verify service account has `aiplatform.user` role |
| Streamlit not loading | Restart systemd service on GCP |
| 502 Bad Gateway | Check nginx config and backend health |

## Contributing

This is an internal UWAY project. For access requests, contact the development team.

## License

Proprietary - UWAY Innovation Limited © 2026

---

**Last Updated**: 2026-05-09  
**Version**: 2.0.0 (Production Deployment)  
**Maintainer**: UWAY Engineering Team
