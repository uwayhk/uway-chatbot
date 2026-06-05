# UWAY Chatbot - GCP 前端部署指南

## 问题诊断

chatbot.hkuway.com 目前有三个 provider 错误，我们决定使用**方案 C**：调用已修复的 EC2 后端。

- ✅ EC2 后端 (16.163.147.170:8000) 已修复并正常工作
- ❌ GCP 前端 (34.96.220.45) 需要更新

---

## 部署方案

### 方案 1: 手动上传到 GCP (推荐)

如果您有 GCP 控制台访问权限：

1. **SSH 到 GCP 实例**
   ```bash
   # 通过 GCP 控制台获取 SSH 访问
   # 或使用：gcloud compute ssh uway-chatbot --zone=asia-east1-b --project=uway-hq-493308
   ```

2. **创建应用目录**
   ```bash
   sudo mkdir -p /opt/uway-chatbot-frontend
   cd /opt/uway-chatbot-frontend
   ```

3. **上传文件**
   ```bash
   # 从本地上传
   scp -i [SSH_KEY] app.py requirements.txt [USER]@34.96.220.45:/opt/uway-chatbot-frontend/
   ```

4. **安装依赖**
   ```bash
   sudo pip3 install -r requirements.txt
   ```

5. **创建 systemd 服务**
   ```bash
   sudo tee /etc/systemd/system/uway-chatbot-frontend.service > /dev/null << 'EOF'
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
   EOF
   ```

6. **启动服务**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable uway-chatbot-frontend
   sudo systemctl restart uway-chatbot-frontend
   sudo systemctl status uway-chatbot-frontend
   ```

7. **配置 nginx**
   ```bash
   sudo tee /etc/nginx/sites-available/chatbot > /dev/null << 'EOF'
   server {
       listen 80;
       server_name chatbot.hkuway.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # WebSocket support for Streamlit
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   EOF

   sudo ln -sf /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/chatbot
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **测试**
   ```bash
   curl http://localhost:8501
   # 访问 https://chatbot.hkuway.com
   ```

---

### 方案 2: 使用自动化部署脚本

```bash
cd /root/workspace/uway-chatbot/gcp_frontend
chmod +x deploy.sh

# 如果有 SSH 密钥
./deploy.sh /path/to/gcp_ssh_key

# 或使用默认密钥
./deploy.sh
```

---

### 方案 3: 部署到 Hugging Face Spaces (备选)

如果 GCP 无法访问，可以部署到 HF Spaces：

1. **创建 Space**
   - 访问 https://huggingface.co/new-space
   - Owner: uway
   - Space name: chatbot
   - SDK: Streamlit
   - Visibility: Private

2. **上传代码**
   ```bash
   cd /root/workspace/uway-chatbot/gcp_frontend
   git init
   git remote add origin https://huggingface.co/spaces/uway/chatbot
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

3. **更新 DNS**
   - 将 chatbot.hkuway.com 的 CNAME 指向 uway-chatbot.hf.space

---

## 文件清单

```
gcp_frontend/
├── app.py              # Streamlit 前端应用
├── requirements.txt    # Python 依赖
├── deploy.sh          # 自动化部署脚本
└── DEPLOYMENT.md      # 本文件
```

---

## 验证

部署后测试：

1. **健康检查**
   ```bash
   curl http://34.96.220.45:8501/health
   ```

2. **功能测试**
   - 访问 https://chatbot.hkuway.com
   - 发送消息："What is AML compliance?"
   - 应该收到回复

3. **后端连接**
   - 检查侧边栏显示 "✅ Backend Connected"
   - 确认 IP: 16.163.147.170:8000

---

## 故障排除

### 问题 1: 无法连接后端
- 检查 EC2 安全组是否允许 8000 端口
- 确认 EC2 服务运行：`ssh ubuntu@16.163.147.170 "systemctl status uway-chatbot.service"`

### 问题 2: Streamlit 无法启动
- 检查日志：`journalctl -u uway-chatbot-frontend -f`
- 确认依赖安装：`pip3 list | grep streamlit`

### 问题 3: nginx 502 错误
- 检查 Streamlit 是否运行：`netstat -tlnp | grep 8501`
- 重启 nginx：`systemctl restart nginx`

---

## 回滚方案

如果新部署有问题，可以回滚到旧版本：

```bash
# 停止新服务
sudo systemctl stop uway-chatbot-frontend

# 恢复旧配置
sudo cp /etc/nginx/sites-available/chatbot.backup /etc/nginx/sites-available/chatbot
sudo systemctl restart nginx
```

---

创建时间：2026-04-30
状态：准备部署
