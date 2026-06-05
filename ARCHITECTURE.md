# UWAY Chatbot Architecture

Technical architecture documentation for the UWAY Compliance Chatbot system.

## System Overview

The UWAY Compliance Chatbot is a RAG (Retrieval-Augmented Generation) powered AI assistant that helps users understand financial compliance regulations in Hong Kong, including AML/KYC requirements, HKMA guidelines, and SFC rules.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                              USERS                                   │
│         (Compliance Officers, Relationship Managers, Clients)        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              │ HTTPS (443)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  GCP Instance (34.96.220.45)                                 │    │
│  │                                                              │    │
│  │  ┌─────────────┐    ┌─────────────┐                         │    │
│  │  │   nginx     │───▶│  Streamlit  │                         │    │
│  │  │  (SSL/TLS)  │    │   :8501     │                         │    │
│  │  └─────────────┘    └─────────────┘                         │    │
│  │       ▲                    │                                 │    │
│  │       │ Certbot            │ HTTP (80)                       │    │
│  └───────┼────────────────────┼─────────────────────────────────┘    │
└──────────┼────────────────────┼──────────────────────────────────────┘
           │                    │
           │                    ▼
           │         ┌─────────────────────────────────────────────┐
           │         │              APPLICATION LAYER               │
           │         │  ┌─────────────────────────────────────┐    │
           │         │  │  AWS EC2 (16.163.147.170)            │    │
           │         │  │                                      │    │
           │         │  │  ┌─────────┐    ┌───────────────┐   │    │
           │         │  │  │  nginx  │───▶│   FastAPI     │   │    │
           │         │  │  │  :80    │    │   :8000       │   │    │
           │         │  │  └─────────┘    └───────┬───────┘   │    │
           │         │  └─────────────────────────┼───────────┘    │
           │         └────────────────────────────┼────────────────┘
           │                                      │
           │                                      │ Python
           │                                      ▼
           │         ┌─────────────────────────────────────────────┐
           │         │              BUSINESS LOGIC LAYER            │
           │         │  ┌─────────────────────────────────────┐    │
           │         │  │         Provider Manager             │    │
           │         │  │  ┌─────────────┐  ┌──────────────┐  │    │
           │         │  │  │   Gemini    │  │   Fallback   │  │    │
           │         │  │  │  Provider   │  │   Provider   │  │    │
           │         │  │  └──────┬──────┘  └──────────────┘  │    │
           │         │  └─────────┼───────────────────────────┘    │
           │         └────────────┼────────────────────────────────┘
           │                      │
           │                      │ HTTPS
           ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Google Cloud Platform                                       │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Vertex AI API                                       │    │    │
│  │  │  gemini-2.5-pro                                      │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │                                                              │    │
│  │  Service Account: vertex-express@uway-hq-493308             │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Presentation Layer (GCP)

#### nginx (SSL Termination)
- **Port**: 443 (HTTPS), 80 (HTTP redirect)
- **SSL**: Certbot managed certificates
- **Function**: Reverse proxy to Streamlit
- **Config**: `/etc/nginx/sites-enabled/chatbot.hkuway.com`

#### Streamlit Frontend
- **Port**: 8501
- **Framework**: Streamlit 1.57+
- **Features**:
  - Chat interface with message history
  - Backend health monitoring
  - Knowledge base viewer
  - Session statistics

**Key Files**:
```
/opt/uway-chatbot-frontend/
├── app.py                 # Main Streamlit application
└── requirements.txt       # Python dependencies
```

### 2. Application Layer (AWS EC2)

#### nginx (API Proxy)
- **Port**: 80
- **Function**: Reverse proxy to FastAPI
- **Config**: `/etc/nginx/sites-enabled/uway-chatbot`

#### FastAPI Backend
- **Port**: 8000
- **Framework**: FastAPI + Uvicorn
- **Endpoints**:
  - `GET /api/health` - Health check
  - `POST /api/chat` - Chat completion
  - `GET /api/kb/stats` - Knowledge base stats

**Key Files**:
```
/opt/uway-chatbot/
├── main.py               # FastAPI application
├── provider_manager.py   # LLM provider abstraction
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
└── knowledge_base/       # Compliance documents
```

### 3. Business Logic Layer

#### Provider Manager

Abstracts LLM provider interactions with automatic failover.

**Supported Providers**:
1. **GeminiProvider** (Primary)
   - Model: `gemini-2.5-pro`
   - Auth: Service Account (OAuth 2.0)
   - Endpoint: Vertex AI API

2. **FallbackProvider** (Secondary)
   - Configurable backup providers
   - Activated on primary failure

**Provider Router**:
```python
class ProviderRouter:
    def __init__(self):
        self.providers = [
            GeminiProvider(),  # Primary
            # FallbackProvider("VENDOR1"),  # Secondary
        ]
    
    def chat(self, messages, system_prompt=None):
        for provider in self.providers:
            try:
                return provider.chat(messages)
            except Exception as e:
                continue  # Try next provider
        raise RuntimeError("All providers failed")
```

### 4. External Services

#### Google Vertex AI

**Configuration**:
- **Project**: `uway-hq-493308`
- **Service Account**: `vertex-express@uway-hq-493308.iam.gserviceaccount.com`
- **Model**: `gemini-2.5-pro`
- **Region**: `us-central1`
- **API Endpoint**: `https://us-central1-aiplatform.googleapis.com/v1/...`

**Authentication Flow**:
```
1. Load service account key (JSON)
2. Generate OAuth 2.0 access token
3. Include token in API request headers
4. Vertex AI validates and processes request
5. Return generated content
```

## Data Flow

### Chat Request Flow

```
User Message
    │
    ▼
┌─────────────────┐
│  Streamlit UI   │  (GCP)
└────────┬────────┘
         │ HTTP POST /api/chat
         ▼
┌─────────────────┐
│  FastAPI        │  (AWS EC2)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ProviderRouter │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GeminiProvider │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Vertex AI API  │  (Google Cloud)
└────────┬────────┘
         │
         │ Generated Response
         ▼
┌─────────────────┐
│  FastAPI        │  + Source citations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit UI   │  Display to user
└─────────────────┘
```

## Knowledge Base

### Structure

```
knowledge_base/
├── hkmaguidelines/
│   ├── aml_cft_guideline.md
│   ├── cdd_requirements.md
│   └── ...
├── sfc_rules/
│   ├── licensing_requirements.md
│   ├── conduct_requirements.md
│   └── ...
├── sumsub/
│   ├── overview.md
│   ├── kyc_services.md
│   └── ...
└── general/
    ├── aml_basics.md
    └── kyc_checklist.md
```

### Document Format

Documents are stored in Markdown with:
- Clear section headings (`##`, `###`)
- Bullet points for lists
- Bold text for emphasis
- Code blocks for examples

### Retrieval Process

1. User sends question
2. System embeds question (implicit via LLM)
3. LLM retrieves relevant context from knowledge base
4. LLM generates response with citations
5. Response includes source document names

## Security Architecture

### Network Security

```
┌─────────────────────────────────────────────────────────┐
│  AWS Security Group (EC2)                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Inbound Rules:                                  │    │
│  │  - Port 22 (SSH): Trusted IPs only              │    │
│  │  - Port 80 (HTTP): 0.0.0.0/0 (API access)       │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  GCP Firewall Rules                                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Inbound Rules:                                  │    │
│  │  - Port 22 (SSH): Trusted IPs only              │    │
│  │  - Port 80 (HTTP): 0.0.0.0/0 (redirect)         │    │
│  │  - Port 443 (HTTPS): 0.0.0.0/0 (main access)    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Authentication & Authorization

**Current State**:
- No API authentication (internal use only)
- Service account for GCP access
- SSH key-based access for servers

**Production Recommendations**:
- Implement API key authentication
- Add OAuth2 for user login
- Rotate service account keys quarterly
- Enable VPC Service Controls

### Data Protection

- **In Transit**: TLS 1.3 (HTTPS)
- **At Rest**: Encrypted disk volumes
- **Secrets**: Environment variables with restricted permissions

## Deployment Architecture

### Infrastructure as Code

Current deployment uses manual setup. Future improvements:
- Terraform for infrastructure provisioning
- Ansible for configuration management
- GitHub Actions for CI/CD

### Service Management

Both backend and frontend use systemd for process management:

```bash
# Backend
sudo systemctl status uway-chatbot
sudo journalctl -u uway-chatbot -f

# Frontend
sudo systemctl status uway-chatbot-frontend
sudo tail -f /tmp/streamlit.log
```

### High Availability

**Current**: Single instance for each component

**Future Improvements**:
- Multi-AZ deployment for EC2
- Load balancer for frontend
- Database for session persistence
- Redis for caching

## Monitoring & Observability

### Metrics to Track

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| API Latency (p95) | CloudWatch | > 5s |
| Error Rate | CloudWatch | > 1% |
| CPU Usage | CloudWatch | > 80% |
| Memory Usage | CloudWatch | > 80% |
| Vertex AI Quota | GCP Console | > 80% |

### Logging

- **Application**: systemd journal
- **Access**: nginx access logs
- **Errors**: nginx error logs

### Alerting

Configure alerts for:
- Service downtime
- High error rates
- Resource exhaustion
- API quota limits

## Cost Analysis

### Current Deployment (Free Tier)

| Resource | Provider | Monthly Cost |
|----------|----------|--------------|
| EC2 t3.micro | AWS | $0 (Free Tier) |
| e2-micro | GCP | $0 (Free Tier) |
| Vertex AI | Google | $0 (60 req/min free) |
| **Total** | | **~$0** |

### Production Scaling

| Resource | Provider | Estimated Cost |
|----------|----------|----------------|
| EC2 t3.small | AWS | $15/month |
| e2-small | GCP | $10/month |
| Vertex AI (paid) | Google | $0.00025/1K tokens |
| **Total** | | **~$25-50/month** |

## Future Enhancements

### Planned Features

1. **User Authentication**
   - OAuth2 login
   - Role-based access control
   - Session management

2. **Advanced RAG**
   - Vector database (Pinecone/Weaviate)
   - Semantic search
   - Multi-document retrieval

3. **Analytics Dashboard**
   - Usage statistics
   - Popular questions
   - User feedback

4. **Multi-Model Support**
   - Claude (Anthropic)
   - GPT-4 (OpenAI)
   - Local models (Llama via vLLM)

5. **Compliance Features**
   - Audit logging
   - Data retention policies
   - Export capabilities

---

**Last Updated**: 2026-05-09  
**Version**: 2.0.0  
**Maintainer**: UWAY Engineering Team
