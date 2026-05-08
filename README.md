# Finance Multi-Agent Research System

一个用于股票研究的多 Agent 金融分析系统 Demo。系统围绕单只股票自动完成行情获取、新闻检索、情绪分析、风险评估和 Markdown 研究报告生成。

## 功能特点

- **MarketDataAgent**：获取股票行情、收益率、波动率和估值指标
- **NewsAgent**：通过 Google News RSS 获取相关新闻
- **SentimentAgent**：基于 VADER 对新闻标题进行情绪分析
- **RiskAgent**：根据波动率、估值、收益率和新闻情绪评估风险
- **ReportAgent**：自动生成 Markdown 格式研究报告
- **FinanceResearchOrchestrator**：总控调度多个 Agent 协同执行任务

## 项目结构

```text
finance-multi-agent-system/
├── finance_multi_agent.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/finance-multi-agent-system.git
cd finance-multi-agent-system
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行程序

```bash
python finance_multi_agent.py
```

输入股票代码，例如：

```text
AAPL
TSLA
MSFT
NVDA
```

程序会在当前目录生成类似下面的报告文件：

```text
AAPL_research_report.md
```

## 示例输出

```text
正在分析：AAPL
金融数据获取完成
新闻数据获取完成
情绪分析完成
风险评估完成
研究报告已生成：AAPL_research_report.md
```

## 系统逻辑

```text
用户输入股票代码
        ↓
MarketDataAgent 获取股票行情和基本面数据
        ↓
NewsAgent 检索相关新闻
        ↓
SentimentAgent 分析新闻情绪
        ↓
RiskAgent 评估投资风险
        ↓
ReportAgent 生成研究报告
```

## 说明

本项目仅用于学习、课程展示和 AI Agent 系统 Demo，不构成任何投资建议。
