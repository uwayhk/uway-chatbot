#!/bin/bash
# deploy.sh - One-click deployment to AWS EC2
set -e

echo "=========================================="
echo " UWAY Chatbot Backend Deployment Script"
echo "=========================================="

# 1. Update system
echo "[1/6] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install Python & dependencies
echo "[2/6] Installing Python and dependencies..."
sudo apt install -y python3-pip python3-venv redis-server nginx

# 3. Create project directory
echo "[3/6] Creating project directory..."
mkdir -p /opt/uway-chatbot
cd /opt/uway-chatbot

# 4. Setup virtual environment
echo "[4/6] Setting up Python venv..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# 5. Copy application files
echo "[5/6] Installing application..."
pip install -r requirements.txt

# 6. Configure GCP ADC (if using Google Cloud authentication)
echo "[6/6] Configuring GCP ADC..."
# Place your service account key at /opt/uway-chatbot/key.json
# Or run: gcloud auth application-default login

# Create systemd service
cat > /etc/systemd/system/uway-chatbot.service << 'EOF'
[Unit]
Description=UWAY Chatbot Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/uway-chatbot
Environment="GOOGLE_APPLICATION_CREDENTIALS=/opt/uway-chatbot/vertex-express-key.json"
Environment="PATH=/opt/uway-chatbot/venv/bin"
ExecStart=/opt/uway-chatbot/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable uway-chatbot
sudo systemctl start uway-chatbot

echo ""
echo "✅ Deployment complete!"
echo "   Backend running at: http://localhost:8000"
echo "   Health check: http://localhost:8000/api/health"
echo ""
echo "Next steps:"
echo "1. Configure firewall/security group for port 8000"
echo "2. Set up Nginx reverse proxy (optional)"
echo "3. Update HF Spaces secret AWS_API_URL"