# GCP Application Default Credentials (ADC) Setup

## Why ADC?
Your organization prohibits API Keys due to security policy. ADC is the recommended alternative.

## Step-by-Step Instructions

### Option A: Using gcloud CLI (Recommended for EC2)

1. **Install gcloud CLI**
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL  # Reload shell
   ```

2. **Login and generate credentials**
   ```bash
   gcloud auth application-default login
   ```
   This creates `~/.config/gcloud/application_default_credentials.json`

3. **Set environment variable**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json
   ```

4. **Verify it works**
   ```bash
   gcloud auth application-default print-access-token
   ```

### Option B: Service Account Key JSON (Alternative)

1. **Create Service Account in GCP Console**
   - Go to IAM & Admin → Service Accounts
   - Create new SA: `uway-chatbot-sa`
   - Add roles: `Vertex AI User`, `Cloud Platform`

2. **Generate and download JSON key**

3. **Upload to EC2**
   ```bash
   scp -i ~/.ssh/aws_hk_key key.json ubuntu@<EC2-IP>:~/
   mv ~/key.json /opt/uway-chatbot/credentials.json
   chmod 600 /opt/uway-chatbot/credentials.json
   ```

4. **Set environment variable in systemd service**
   ```bash
   # Edit: /etc/systemd/system/uway-chatbot.service
   Environment="GOOGLE_APPLICATION_CREDENTIALS=/opt/uway-chatbot/credentials.json"
   sudo systemctl daemon-reload
   sudo systemctl restart uway-chatbot
   ```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ADC failed` | Check that `gcloud auth application-default login` completed successfully |
| `Permission denied` | Ensure file permissions are 600 |
| `Quota exceeded` | Gemini free tier limits (~15 RPM). Upgrade project quota if needed |
| `Organization policy violation` | You must use Service Account Key, contact your GCP admin |

## Token Refresh

ADC tokens expire after 1 hour. The `google-auth` library handles refresh automatically. No action needed.