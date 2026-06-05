# UWAY Chatbot Deployment Guide

Complete guide for deploying the UWAY Compliance Chatbot to AWS EC2 (backend) and GCP (frontend).

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  User → HTTPS (chatbot.hkuway.com) → GCP nginx → Streamlit  │
│                                                ↓            │
│                              EC2 nginx → FastAPI → Vertex AI│
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### AWS EC2 (Backend)
- Ubuntu 22.04 LTS instance
- Public IP: `16.163.147.170`
- SSH key: `/root/workspace/test.pem`
- User: `ubuntu`
- Security group: Allow ports 22 (SSH), 80 (HTTP)

### GCP Instance (Frontend)
- Ubuntu 22.04 LTS instance
- Public IP: `34.96.220.45`
- SSH key: `/root/.ssh/gcp_hk_key`
- User: `louie`
- Firewall: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

### Google Cloud
- Project ID: `uway-hq-493308`
- Service account key: `vertex-express-key.json`
- Vertex AI API enabled

---

## Part 1: Backend Deployment (AWS EC2)

### Step 1: Prepare Files

```bash
# On your local machine
cd /root/workspace/uway-chatbot

# Copy service account key
cp /path/to/vertex-express-key.json aws_backend/

# Create deployment package
cd aws_backend
tar -czf ../aws_backend_deploy.tar.gz \
  main.py \
  provider_manager.py \
  requirements.txt \
  .env.example \
  deploy.sh \
  nginx.conf \
  vertex-express-key.json
```

### Step 2: Upload to EC2

```bash
# SSH to EC2
ssh -i /root/workspace/test.pem ubuntu@16.163.147.170

# Create directory
sudo mkdir -p /opt/uway-chatbot
sudo chown ubuntu:ubuntu /opt/uway-chatbot
cd /opt/uway-chatbot

# Exit SSH and upload from local
exit

# From local machine
scp -i /root/workspace/test.pem \
  aws_backend_deploy.tar.gz \
  ubuntu@16.163.147.170:/home/ubuntu/

# SSH back and extract
ssh -i /root/workspace/test.pem ubuntu@16.163.147.170
cd /opt/uway-chatbot
tar -xzf ~/aws_backend_deploy.tar.gz
```

### Step 3: Configure Environment

```bash
# Create .env file
cat > /opt/uway-chatbot/.env << EOF
# GCP Authentication
GOOGLE_APPLICATION_CREDENTIALS=/opt/uway-chatbot/vertex-express-key.json

# Model Settings
GEMINI_MODEL=gemini-2.5-pro

# Server Settings
HOST=0.0.0.0
PORT=8000
EOF

# Set permissions
chmod 600 /opt/uway-chatbot/.env
chmod 600 /opt/uway-chatbot/vertex-express-key.json
```

### Step 4: Install Dependencies

```bash
cd /opt/uway-chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Nginx

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-enabled/uway-chatbot

# Test config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 6: Create Systemd Service

```bash
# Create service file
sudo tee /etc/systemd/system/uway-chatbot.service > /dev/null << 'EOF'
[Unit]
Description=UWAY Chatbot Backend API
After=network.target

[Service]
Type=exec
User=ubuntu
WorkingDirectory=/opt/uway-chatbot
Environment="PATH=/opt/uway-chatbot/venv/bin"
ExecStart=/opt/uway-chatbot/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable uway-chatbot
sudo systemctl start uway-chatbot
```

### Step 7: Verify Backend

```bash
# Check service status
sudo systemctl status uway-chatbot

# Test health endpoint
curl http://localhost:8000/api/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is AML?", "session_id": "test"}'
```

Expected response:
```json
{
  "status": "healthy",
  "service": "uway-chatbot-backend",
  "version": "1.0.0"
}
```

---

## Part 2: Frontend Deployment (GCP)

### Step 1: Prepare Files

```bash
# On your local machine
cd /root/workspace/uway-chatbot/gcp_frontend

# Create deployment package
tar -czf ../gcp_frontend_deploy.tar.gz app.py requirements.txt deploy.sh
```

### Step 2: Upload to GCP

```bash
# SSH to GCP
ssh -i /root/.ssh/gcp_hk_key louie@34.96.220.45

# Create directory
sudo mkdir -p /opt/uway-chatbot-frontend
sudo chown louie:louie /opt/uway-chatbot-frontend
cd /opt/uway-chatbot-frontend

# Exit SSH and upload from local
exit

# From local machine
scp -i /root/.ssh/gcp_hk_key \
  gcp_frontend_deploy.tar.gz \
  louie@34.96.220.45:/home/louie/

# SSH back and extract
ssh -i /root/.ssh/gcp_hk_key louie@34.96.220.45
cd /opt/uway-chatbot-frontend
tar -xzf ~/gcp_frontend_deploy.tar.gz
```

### Step 3: Install Dependencies

```bash
cd /opt/uway-chatbot-frontend

# Install system dependencies (if needed)
sudo apt-get update
sudo apt-get install -y python3-pip

# Install Python packages
pip3 install --break-system-packages -r requirements.txt
```

### Step 4: Create Systemd Service

```bash
# Create service file
sudo tee /etc/systemd/system/uway-chatbot-frontend.service > /dev/null << 'EOF'
[Unit]
Description=UWAY Chatbot Streamlit Frontend
After=network.target

[Service]
Type=exec
User=louie
WorkingDirectory=/opt/uway-chatbot-frontend
ExecStart=/home/louie/.local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable uway-chatbot-frontend
sudo systemctl start uway-chatbot-frontend
```

### Step 5: Configure Nginx

```bash
# Create nginx config
sudo tee /etc/nginx/sites-enabled/chatbot.hkuway.com > /dev/null << 'EOF'
server {
    server_name chatbot.hkuway.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
        proxy_buffering off;
        proxy_cache off;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/chatbot.hkuway.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/chatbot.hkuway.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = chatbot.hkuway.com) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name chatbot.hkuway.com;
    return 404;
}
EOF

# Remove any duplicate configs
sudo rm -f /etc/nginx/sites-enabled/chatbot.hkuway.com.backup

# Test and reload
sudo nginx -t
sudo nginx -s reload
```

### Step 6: Verify Frontend

```bash
# Check service status
sudo systemctl status uway-chatbot-frontend

# Test locally
curl http://localhost:8501

# Test via HTTPS
curl https://chatbot.hkuway.com
```

---

## Part 3: End-to-End Testing

### Test Chat Functionality

1. Open https://chatbot.hkuway.com in browser
2. Verify "Backend Connected" status in sidebar
3. Send test message: "What is Sumsub?"
4. Verify response with sources and confidence score

### Verify Backend Connection from Frontend

```bash
# From GCP instance
ssh -i /root/.ssh/gcp_hk_key louie@34.96.220.45
curl http://16.163.147.170/api/health
```

Expected: `{"status":"healthy",...}`

---

## Maintenance

### Update Backend

```bash
# SSH to EC2
ssh -i /root/workspace/test.pem ubuntu@16.163.147.170

# Update code
cd /opt/uway-chatbot
# (upload new files or git pull)

# Restart service
sudo systemctl restart uway-chatbot
```

### Update Frontend

```bash
# SSH to GCP
ssh -i /root/.ssh/gcp_hk_key louie@34.96.220.45

# Update code
cd /opt/uway-chatbot-frontend
# (upload new app.py)

# Restart service
sudo systemctl restart uway-chatbot-frontend
```

### View Logs

```bash
# Backend logs
sudo journalctl -u uway-chatbot -f

# Frontend logs
tail -f /tmp/streamlit.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## Troubleshooting

### Backend Issues

| Problem | Solution |
|---------|----------|
| Service won't start | Check `journalctl -u uway-chatbot` for errors |
| 502 Bad Gateway | Verify backend is running: `curl localhost:8000/api/health` |
| Gemini API errors | Check service account key permissions |

### Frontend Issues

| Problem | Solution |
|---------|----------|
| Streamlit won't start | Check port 8501: `sudo netstat -tlnp \| grep 8501` |
| Backend Unavailable | Verify EC2 security group allows port 80 |
| SSL certificate error | Renew with `sudo certbot renew` |

---

## Cost Monitoring

### AWS Free Tier Checklist
- [ ] Instance type: t3.micro
- [ ] OS: Ubuntu Server 22.04 LTS (not Pro)
- [ ] Storage: ≤30GB GP3
- [ ] Data transfer: ≤100GB/month

### GCP Free Tier Checklist
- [ ] Instance type: e2-micro
- [ ] Region: us-central1 (or free tier eligible)

### Vertex AI Quotas
- Free tier: 60 requests/minute
- Monitor: https://console.cloud.google.com/vertex-ai/quotas

---

**Last Updated**: 2026-05-09  
**Version**: 2.0.0
