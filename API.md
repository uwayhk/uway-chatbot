# UWAY Chatbot API Documentation

REST API reference for the UWAY Compliance Chatbot backend.

## Base URL

```
Production: http://16.163.147.170/api
```

## Authentication

Currently, the API does not require authentication. For production use, implement API key or OAuth2 authentication.

---

## Endpoints

### Health Check

Verify the backend service is running and healthy.

**Request**
```http
GET /api/health
```

**Response**
```json
{
  "status": "healthy",
  "service": "uway-chatbot-backend",
  "version": "1.0.0"
}
```

**Status Codes**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is degraded

---

### Chat

Send a message and receive an AI-powered response with citations.

**Request**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is Sumsub?",
  "session_id": "user_123"
}
```

**Request Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User's question or message |
| `session_id` | string | No | Session identifier for conversation history |

**Response**
```json
{
  "answer": "Sumsub (short for \"Sum and Substance\") is a global RegTech company that provides an all-in-one identity verification, compliance, and anti-fraud platform...",
  "sources": [
    "sumsub_overview.md",
    "kyc_requirements.md",
    "aml_screening.md"
  ],
  "confidence_score": 0.92
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | AI-generated response text |
| `sources` | array | List of knowledge base documents referenced |
| `confidence_score` | float | Model confidence (0.0 - 1.0) |

**Status Codes**
- `200 OK` - Successful response
- `400 Bad Request` - Invalid request body
- `500 Internal Server Error` - Backend processing error
- `503 Service Unavailable` - LLM provider unavailable

**Example (curl)**
```bash
curl -X POST http://16.163.147.170/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the HKMA AML requirements for customer onboarding?",
    "session_id": "compliance_officer_001"
  }'
```

---

### Knowledge Base Stats

Get statistics about the loaded knowledge base.

**Request**
```http
GET /api/kb/stats
```

**Response**
```json
{
  "total_documents": 67,
  "categories": {
    "hkmaguidelines": 23,
    "sfc_rules": 18,
    "sumsub": 15,
    "aml_cft": 11
  },
  "last_updated": "2026-05-09T04:00:00Z"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | `Invalid request body` | Missing required fields or malformed JSON |
| 422 | `Validation Error` | Request validation failed |
| 500 | `Internal server error` | Unexpected server error |
| 503 | `Service unavailable` | LLM provider or database unavailable |

---

## Rate Limiting

Current deployment does not enforce rate limiting. For production:

- Recommended: 60 requests/minute per IP
- Vertex AI free tier: 60 requests/minute total

Implement rate limiting in nginx or application layer.

---

## Streaming Support

The API supports streaming responses via Server-Sent Events (SSE).

**Request**
```http
POST /api/chat/stream
Content-Type: application/json

{
  "message": "What is KYC?",
  "session_id": "user_123"
}
```

**Response**
```
data: {"token": "KYC"}
data: {"token": " stands"}
data: {"token": " for"}
data: {"token": " Know"}
data: {"token": " Your"}
data: {"token": " Customer"}
data: {"done": true}
```

---

## LLM Provider Fallback

The backend uses a provider router with automatic failover:

1. **Primary**: Google Gemini 2.5 Pro (Vertex AI)
2. **Fallback**: Configurable secondary providers

Provider selection is automatic based on availability.

---

## Knowledge Base

### Supported Document Formats

- Markdown (.md)
- Plain text (.txt)

### Document Structure

Documents should include:
- Clear headings (## Section)
- Bullet points for lists
- Bold text for emphasis

### Ingestion

Documents are automatically loaded from `/opt/uway-chatbot/knowledge_base/` on service start.

To update the knowledge base:
```bash
# Copy new documents
sudo cp new_doc.md /opt/uway-chatbot/knowledge_base/

# Restart service
sudo systemctl restart uway-chatbot
```

---

## Session Management

Sessions are stored in memory (non-persistent). For production:

- Use Redis for session storage
- Implement session expiration (default: 30 minutes)
- Add user authentication

---

## Monitoring

### Metrics to Track

- Request latency (p50, p95, p99)
- Error rate by endpoint
- LLM provider response time
- Token usage per request

### Logging

Logs are written to systemd journal:
```bash
sudo journalctl -u uway-chatbot -f
```

---

## Security Recommendations

1. **Authentication**: Implement API key or JWT authentication
2. **Rate Limiting**: Add nginx or application-level rate limiting
3. **Input Validation**: Sanitize all user inputs
4. **HTTPS**: Use TLS for all API communications
5. **Audit Logging**: Log all requests for compliance

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-29 | Initial release |
| 2.0.0 | 2026-05-09 | Production deployment with Vertex AI |

---

**Last Updated**: 2026-05-09  
**API Version**: 2.0.0
