# AWS EC2 Launch Guide (Free Tier)

## Prerequisites
- AWS Account with activated $200 Founders Credit
- SSH key pair (`~/.ssh/aws_hk_key.pem`)

## Step-by-Step Launch

### 1. Launch Instance (CLI or Console)

**Using AWS CLI:**
```bash
# Find correct Ubuntu AMI (must be Canonical official!)
aws ec2 describe-images   --owners 099720109477   --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"   --query "sort_by(Images, &CreationDate)[-1].ImageId"   --region ap-east-1

# Store result
AMI_ID=$(aws ec2 describe-images ... --output text)

# Launch instance
aws ec2 run-instances   --image-id $AMI_ID   --instance-type t3.micro   --key-name YourKeyPairName   --security-group-ids sg-xxxxx   --subnet-id subnet-xxxxx   --region ap-east-1   --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=uway-chatbot}]"   --credit-specification '{"CpuCredits":"Standard"}'  # CRITICAL: Not Unlimited!
```

**Via Console:**
1. EC2 → Launch Instance
2. Name: `uway-chatbot`
3. AMI: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
4. Instance type: `t3.micro` ✅
5. Key pair: Select existing SSH key
6. Network settings: Allow SSH (22), HTTP (80), Custom TCP (8000)
7. Storage: 8 GiB GP3 ✅
8. Advanced details: **DO NOT select "Unlimited" CPU credits**
9. Launch

### 2. Security Group Configuration

Add inbound rules:
| Port | Protocol | Source | Purpose |
|------|----------|--------|---------|
| 22 | TCP | Your IP | SSH |
| 80 | TCP | 0.0.0.0/0 | HTTP (Nginx) |
| 8000 | TCP | HF Spaces IP | FastAPI (restrict if possible) |

### 3. Connect to Instance

```bash
chmod 600 ~/.ssh/aws_hk_key.pem
ssh -i ~/.ssh/aws_hk_key.pem ubuntu@<EC2-Public-IP>
```

### 4. Deploy Application

```bash
# Inside EC2 terminal
wget https://raw.githubusercontent.com/your-repo/uway-chatbot/main/aws_backend/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 5. Configure GCP ADC (if using)

```bash
# Option A: Interactive login
gcloud auth application-default login

# Option B: Upload service account key
scp -i ~/.ssh/aws_hk_key.pem credentials.json ubuntu@<EC2-IP>:~/
mv ~/credentials.json /opt/uway-chatbot/
chmod 600 /opt/uway-chatbot/credentials.json
```

### 6. Verify

```bash
# Check service status
sudo systemctl status uway-chatbot

# Test health endpoint
curl http://localhost:8000/api/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat   -H "Content-Type: application/json"   -d '{"message": "What is AML?", "session_id": "test"}'
```

## Cost Monitoring

To ensure Free Tier eligibility:
1. Do NOT enable "Unlimited" CPU credits
2. Use official Ubuntu AMI (not Ubuntu Pro)
3. Terminate instance after POC if no longer needed
4. Monitor via AWS Billing Dashboard → Cost Explorer

Estimated cost: **$0** within Free Tier (750 hours/month for 12 months)