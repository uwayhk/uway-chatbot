# Chatbot.hkuway.com 修复方案

## 问题诊断

访问 https://chatbot.hkuway.com 时发现三个 provider 错误：

```
⚠️ nvidia failed: Client.init() got an unexpected keyword argument 'proxies'
⚠️ gemini failed: GEMINI_API_KEY not configured
⚠️ openrouter failed: Cannot render template. Please install minijinja using pip install minijinja.
❌ All providers failed: All providers unavailable
```

## 根本原因

1. **NVIDIA NIM SDK 兼容性问题**: 代码中使用了 `proxies` 参数，但新版 SDK 不再支持
2. **Gemini API Key 缺失**: 环境变量 `GEMINI_API_KEY` 未配置
3. **OpenRouter 依赖缺失**: `minijinja` 包未安装

## 修复方案

### 方案 A: 直接修复 GCP 实例 (34.96.220.45)

如果您有 GCP 实例的 SSH 访问权限：

```bash
# 1. SSH 到服务器
ssh root@34.96.220.45

# 2. 找到 Streamlit 应用代码位置
ps aux | grep streamlit
# 或者
find / -name "app.py" -path "*/streamlit*" 2>/dev/null

# 3. 修复 NVIDIA 代码 - 移除 proxies 参数
# 在代码中找到类似这行：
# client = Client(api_key=..., proxies=...)
# 改为：
# client = Client(api_key=...)

# 4. 安装 minijinja
pip install minijinja

# 5. 配置环境变量
export GEMINI_API_KEY="your-gemini-api-key"
export NVIDIA_API_KEY="your-nvidia-api-key"
export OPENROUTER_API_KEY="your-openrouter-api-key"

# 6. 重启 Streamlit 应用
pkill -f streamlit
streamlit run app.py &
```

### 方案 B: 部署修复后的版本到 Hugging Face Spaces

1. 创建新的 Hugging Face Space:
   - 访问 https://huggingface.co/new-space
   - Space name: `uway-chatbot`
   - SDK: `Streamlit`
   - Hardware: `CPU Basic` (免费)

2. 上传修复后的代码:
   ```bash
   cd /root/workspace/uway-chatbot/streamlit_fixed
   git init
   git remote add origin https://huggingface.co/spaces/uway/uway-chatbot
   git add .
   git commit -m "Fixed provider errors"
   git push -u origin main
   ```

3. 配置 Secrets (在 HF Space 设置中):
   - `NVIDIA_API_KEY`: 您的 NVIDIA API Key
   - `GEMINI_API_KEY`: 您的 Gemini API Key
   - `OPENROUTER_API_KEY`: 您的 OpenRouter API Key

4. 更新域名 DNS:
   - 将 `chatbot.hkuway.com` 的 CNAME 指向 `uway-uway-chatbot.hf.space`

### 方案 C: 使用已修复的 EC2 后端

我们之前修复的 EC2 后端 (16.163.147.170) 已经可以正常工作，可以通过以下方式连接：

1. 更新 Streamlit 前端调用 EC2 API:
   ```python
   API_BASE_URL = "http://16.163.147.170:8000"
   response = requests.post(f"{API_BASE_URL}/api/chat", json={"message": prompt})
   ```

2. 部署到 GCP 实例或 Hugging Face Spaces

## API Key 获取方式

### NVIDIA NIM
1. 访问 https://build.nvidia.com
2. 注册/登录
3. 创建 API Key
4. 免费额度：$500 测试额度

### Google Gemini
1. 访问 https://aistudio.google.com/app/apikey
2. 创建 API Key
3. 免费额度：每分钟 60 次请求

### OpenRouter
1. 访问 https://openrouter.ai/keys
2. 创建 API Key
3. 需要预充值（最低$5）

## 验证修复

修复后，访问 https://chatbot.hkuway.com 并测试：

1. 发送消息："What is AML compliance?"
2. 检查是否收到回复
3. 检查页面底部是否显示 "✅ Powered by [provider]"

## 下一步

请告诉我您希望使用哪个方案：
- 方案 A: 需要 GCP SSH 权限
- 方案 B: 需要 Hugging Face 账号
- 方案 C: 最快的方案，使用已修复的 EC2 后端

## 相关文件

- 修复后的代码：`/root/workspace/uway-chatbot/streamlit_fixed/app.py`
- 依赖文件：`/root/workspace/uway-chatbot/streamlit_fixed/requirements.txt`

---
创建时间：2026-04-30
状态：等待用户选择部署方案
