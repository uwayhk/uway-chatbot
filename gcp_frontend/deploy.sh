#!/bin/bash
# 部署 UWAY Chatbot 前端到 GCP 实例 (34.96.220.45)
# 使用方法：./deploy_to_gcp.sh

set -e

GCP_IP="34.96.220.45"
SSH_KEY="${1:-/root/workspace/test.pem}"
REMOTE_DIR="/opt/uway-chatbot-frontend"

echo "🚀 Deploying UWAY Chatbot Frontend to GCP ($GCP_IP)"
echo "================================================"

# 检查 SSH 密钥
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    echo "Usage: ./deploy_to_gcp.sh [path_to_ssh_key]"
    exit 1
fi

# 创建远程目录
echo "📁 Creating remote directory..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no root@$GCP_IP "mkdir -p $REMOTE_DIR"

# 上传文件
echo "📤 Uploading files..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no app.py requirements.txt root@$GCP_IP:$REMOTE_DIR/

# 安装依赖
echo "📦 Installing dependencies..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no root@$GCP_IP << 'EOF'
cd /opt/uway-chatbot-frontend
pip3 install -r requirements.txt
EOF

# 创建 systemd 服务
echo "⚙️ Creating systemd service..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no root@$GCP_IP << 'EOF'
cat > /etc/systemd/system/uway-chatbot-frontend.service << 'SERVICE'
[Unit]
Description=UWAY Chatbot Streamlit Frontend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/uway-chatbot-frontend
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable uway-chatbot-frontend
systemctl restart uway-chatbot-frontend
EOF

# 检查状态
echo "✅ Checking service status..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no root@$GCP_IP "systemctl status uway-chatbot-frontend --no-pager | head -10"

echo ""
echo "================================================"
echo "🎉 Deployment complete!"
echo "📍 Frontend: http://$GCP_IP:8501"
echo "🔗 Backend: http://16.163.147.170:8000"
echo ""
echo "Next steps:"
echo "1. Configure nginx to proxy chatbot.hkuway.com -> $GCP_IP:8501"
echo "2. Or test directly at http://$GCP_IP:8501"
