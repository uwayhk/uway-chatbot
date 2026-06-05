# UWAY Chatbot - 双仓库同步配置

## ✅ 已配置的远程仓库

| 仓库 | URL | 认证方式 | 状态 |
|------|-----|----------|------|
| **GitHub** | `git@github.com:uwayhk/uway-chatbot.git` | SSH Key | ✅ 正常 |
| **BiGnas** | `ssh://louieadmin@100.120.207.119/volume2/homes/louieadmin/git/uway-chatbot.git` | 密码 | ✅ 正常 |

## 使用方法

### 一键同步到两个仓库

```bash
cd /root/workspace/uway-chatbot
./sync-push.sh
```

输出示例：
```
🚀 Pushing to GitHub and BiGnas...

📦 Pushing to GitHub...
   ✅ GitHub: https://github.com/uwayhk/uway-chatbot

📦 Pushing to BiGnas (louienas)...
   ✅ BiGnas: ssh://louieadmin@100.120.207.119/...

✅ Sync complete!
```

### 手动推送到单个仓库

```bash
# 只推送到 GitHub
git push origin main

# 只推送到 BiGnas
GIT_SSH_COMMAND="sshpass -p 'Adminlizhe123!' ssh -o StrictHostKeyChecking=no" git push nas main
```

## 配置详情

### GitHub
- **Remote 名称**: `origin`
- **SSH Key**: `/root/workspace/uway-chatbot-github-key`
- **公钥**: 已添加到 GitHub (uwayhk 组织)
- **URL**: https://github.com/uwayhk/uway-chatbot

### BiGnas (louienas)
- **Remote 名称**: `nas`
- **主机**: `louienas` (100.120.207.119) via Tailscale
- **用户名**: `louieadmin`
- **密码**: `Adminlizhe123!`
- **仓库路径**: `/volume2/homes/louieadmin/git/uway-chatbot.git`

## 查看远程仓库状态

```bash
cd /root/workspace/uway-chatbot
git remote -v
```

输出：
```
nas     ssh://louieadmin@100.120.207.119/volume2/homes/louieadmin/git/uway-chatbot.git (fetch)
nas     ssh://louieadmin@100.120.207.119/volume2/homes/louieadmin/git/uway-chatbot.git (push)
origin  git@github.com:uwayhk/uway-chatbot.git (fetch)
origin  git@github.com:uwayhk/uway-chatbot.git (push)
```

## 依赖

确保已安装 `sshpass`：
```bash
which sshpass
# 如果未安装：apt-get install sshpass
```

## 安全说明

⚠️ **密码存储**: 
- 密码明文存储在 `sync-push.sh` 脚本中
- 仅限本地使用，不要提交到 Git
- 脚本已加入 `.gitignore`

🔒 **建议改进**:
- 使用 SSH key 替代密码认证
- 或将密码存储在 credential helper 中

---

**Last Updated**: 2026-06-05  
**Status**: ✅ Production Ready
