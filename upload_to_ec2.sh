#!/bin/bash
# upload_to_ec2.sh - Upload all files to AWS EC2
set -e

EC2_USER="ubuntu"
EC2_HOST="${1:-$EC2_PUB_IP}"  # Default from env var
SSH_KEY="${2:-~/.ssh/aws_hk_key.pem}"

if [ -z "$EC2_HOST" ]; then
    echo "Error: Please provide EC2 IP as argument or set EC2_PUB_IP env var"
    echo "Usage: ./upload_to_ec2.sh <EC2-PUBLIC-IP>"
    exit 1
fi

echo "🚀 Uploading to $EC2_USER@$EC2_HOST..."

# Ensure key permissions
chmod 600 $SSH_KEY

# Create project directory on remote host
ssh -i $SSH_KEY $EC2_USER@$EC2_HOST << 'EOF'
mkdir -p /opt/uway-chatbot
EOF

# Upload backend files
echo "[1/3] Uploading backend files..."
scp -i $SSH_KEY -r /root/workspace/uway-chatbot/aws_backend/* $EC2_USER@$EC2_HOST:/opt/uway-chatbot/

# Upload HF Spaces files (for your local reference)
echo "[2/3] Uploading HF Spaces files..."
scp -i $SSH_KEY -r /root/workspace/uway-chatbot/hf_spaces/* ~/uway-chatbot-hf-spaces-backup/

# Upload docs
echo "[3/3] Uploading documentation..."
scp -i $SSH_KEY -r /root/workspace/uway-chatbot/docs $EC2_USER@$EC2_HOST:~/

# Upload Service Account Key if it exists in current directory
SA_KEY_FILE=$(ls vertex-express-*.json 2>/dev/null | head -1)
if [ -n "$SA_KEY_FILE" ]; then
    echo ""
    echo "🔑 Found Service Account Key: $SA_KEY_FILE"
    echo "Uploading to EC2..."
    scp -i $SSH_KEY $SA_KEY_FILE $EC2_USER@$EC2_HOST:/opt/uway-chatbot/vertex-express-key.json
    
    # Set secure permissions on remote host
    ssh -i $SSH_KEY $EC2_USER@$EC2_HOST "chmod 600 /opt/uway-chatbot/vertex-express-key.json"
    
    echo "✅ Service Account Key uploaded securely (chmod 600)"
else
    echo "⚠️ No Service Account Key found. Place 'vertex-express-xxxxx.json' in project root."
    echo "   Download from GCP Console: IAM & Admin → Service Accounts → vertex-express → Keys"
fi

echo ""
echo "✅ All files uploaded successfully!"
echo ""
echo "Next step: Run deployment script on EC2:"
echo "   ssh -i $SSH_KEY $EC2_USER@$EC2_HOST 'cd /opt/uway-chatbot && chmod +x deploy.sh && ./deploy.sh'"