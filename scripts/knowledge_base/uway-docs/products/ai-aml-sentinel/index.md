---
sidebar_position: 1
---

# AI-AML-Sentinel

## 下一代反洗钱智能中枢

**AI-AML-Sentinel** 是面向 Web3 / Fintech 企业的下一代反洗钱（AML）智能平台。它不只是一个"告警器"，而是一个能够理解业务语境、解读全球监管动态、并主动输出决策建议的**合规大脑（Compliance Brain）**。

在 MiCA、香港稳定币牌照等新规落地后，市场缺的不是"告警"，而是**可执行的决策**。

---

## 🎯 核心价值

| 传统 AML 工具 | AI-AML-Sentinel |
|---------------|-----------------|
| 规则匹配，高误报率 | AI + 规则双引擎，误报率降低 60%+ |
| 事后告警，被动响应 | 实时监测，主动预警 |
| 数据孤岛，难以关联 | 链上 + 链下数据融合分析 |
| 黑盒决策，难以解释 | LLM 生成可读的合规叙事 |
| 静态规则，更新滞后 | 语义合规映射，自动追踪监管变化 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI-AML-Sentinel                          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   感知层 (Sense)  │   认知层 (Think)  │      决策层 (Decide)         │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ • Data Ingestor │ • AI Anomaly    │ • LLM Auditor               │
│ • Risk Profiler │   Detector      │ • Semantic Regulatory       │
│                 │ • Red Teaming   │   Mapping                   │
│                 │   Engine        │ • SAR / Policy Generator    │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

### 感知层 (Sense)

**Data Ingestor（数据采集器）**
- 对接公开区块链浏览器 API（Etherscan、Tronscan、BscScan 等）
- 支持交易所内部交易流（CSV / API / WebSocket）导入
- 标准化交易数据结构，统一输出为内部 TransactionSchema
- 增量拉取与断点续传

**Risk Profiler（风险画像引擎）**
- 对接 Sumsub API，拉取用户/企业的 KYC、KYB、制裁筛查结果
- 维护地址 ↔ 用户的映射表（Address Mapping）
- 基于规则计算基础风险分（黑名单、高风险国家、PEP 等）
- 输出 RiskProfile（含评分、标签、时间戳、置信度）

---

### 认知层 (Think)

**AI Anomaly Detector（AI 异常检测）**
- **规则层**：快速过滤已知黑名单地址、大额转账、快进快出
- **模型层**：使用无监督/半监督 ML 模型识别：
  - 剥离汇聚（Layering / Peel Chain）
  - 循环转账（Circular Transactions）
  - 异常时间序列行为
- 输出可疑交易聚类与异常置信度

**Red Teaming Engine（对抗性测试）**
- Prompt Injection 模拟测试
- 交易绕过模拟（分片、混币、跨链桥跳跃）
- 政策漏洞探测
- 攻击报告生成

---

### 决策层 (Decide)

**LLM Auditor（LLM 审计官）**
- 交易解释生成：对 AI 标记的可疑交易生成自然语言解释
- SAR 自动生成：根据预设的本地监管模板生成 Suspicious Activity Report
- 审计日志存档：附带原始 Prompt、输入数据哈希与模型版本

**Semantic Regulatory Mapping（语义合规映射）**
- 监管文档解析：自动抓取并解析 PDF/HTML 格式的监管文件
- 向量化知识库：将监管文本切块并嵌入 Vector DB
- 业务风险映射：用户输入业务流程，系统返回适用的法规条文
- 自动文档生成：基于映射结果生成内部合规政策草稿

---

## 📊 技术规格

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| API 框架 | Python + FastAPI | 异步高性能，AI 生态成熟 |
| 任务队列 | Celery + Redis | 异步数据拉取与模型推理 |
| 数据库 | PostgreSQL | 结构化交易与风险数据 |
| 向量库 | Qdrant / Pinecone | 监管文档语义检索 |
| ML | Scikit-learn, PyTorch (GNN) | 异常检测与图分析 |
| LLM | OpenAI GPT-4 / Claude 3 | 高级推理、文档生成、红队测试 |
| 部署 | Docker, PM2 | 容器化与进程管理 |

---

## 🎯 成功指标 (KPIs)

| 指标 | 目标值 | 测量方式 |
|------|--------|---------|
| 交易监控延迟 | < 5 min | 交易上链 → 系统入库时间 |
| 可疑模式召回率 | > 85% | 已知案例测试集 |
| SAR 生成效率 | < 30s / 份 | 平均生成时间 |
| 法规映射准确率 | > 80% | 合规官抽样评估 |
| 红队测试频率 | ≥ 1 次 / 月 | 自动化任务执行记录 |
| 系统可用性 | > 99.5% | Uptime 监控 |

---

## 🗺️ 产品路线图

### Phase 1: Foundation（基础感知层）—— 4 周
- [ ] FastAPI 项目骨架 + Docker 化
- [ ] Data Ingestor：支持 Etherscan / Tronscan 地址监控
- [ ] Risk Profiler：Sumsub API 对接与基础评分规则
- [ ] 基础告警：黑名单匹配 + 大额转账阈值告警

### Phase 2: Intelligence（认知层）—— 6 周
- [ ] AI Anomaly Detector：ML 模型训练与部署
- [ ] LLM Auditor：可疑交易解释 + SAR 草稿生成
- [ ] Dashboard：可视化风险地址、交易链路、评分趋势

### Phase 3: Evolution（决策层 / 合规大脑）—— 8 周
- [ ] Semantic Regulatory Mapping：Vector DB + RAG 架构上线
- [ ] 自动合规 Checklist 与政策文档生成
- [ ] Red Teaming Engine：交易绕过模拟 + Prompt Injection 测试
- [ ] 闭环反馈：将红队测试结果反哺模型训练与规则更新

---

## 🔗 相关资源

- 技术架构详解 (Coming Soon)
- API 文档 (Coming Soon)
- 部署指南 (Coming Soon)
- Sumsub 集成 Playbook (Coming Soon)

---

## 📞 获取演示

想了解 AI-AML-Sentinel 如何帮助您的团队提升合规效率？

- 📧 联系：uway.hk@hkuway.com
- 🤖 试用 AI 合规助手：[chatbot.hkuway.com](https://chatbot.hkuway.com)
- 📚 浏览合规知识库：[docs.hkuway.com](/docs/knowledge-base/ai-compliance)

---

*文档版本：v1.0 | 最后更新：2026-05-01*
