# agent-engineer-starter

AI Agent 工程化参考实现，覆盖结构化输出、模型路由、安全护栏、失败降级、记忆压缩和审计日志。

默认使用离线 Stub Model，不需要模型 API Key。代码中的模型价格仅作为路由算法演示参数，不代表当前厂商报价。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m examples.demo_ticket_classification
python -m examples.demo_troubleshooting
pytest -v
```

这是工程化教学/验证项目，不是生产级 Agent 框架。