import yfinance as yf
import numpy as np
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime


class MarketDataAgent:
    """金融数据 Agent：获取股票行情与基础指标"""

    def get_stock_data(self, ticker: str, period: str = "6mo"):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            raise ValueError(f"无法获取 {ticker} 的行情数据，请检查股票代码是否正确。")

        info = stock.info

        latest_price = hist["Close"].iloc[-1]
        start_price = hist["Close"].iloc[0]
        return_rate = (latest_price - start_price) / start_price * 100

        hist["Daily Return"] = hist["Close"].pct_change()
        volatility = hist["Daily Return"].std() * np.sqrt(252) * 100

        return {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "sector": info.get("sector", "未知"),
            "industry": info.get("industry", "未知"),
            "latest_price": round(float(latest_price), 2),
            "market_cap": info.get("marketCap", "未知"),
            "pe_ratio": info.get("trailingPE", "未知"),
            "forward_pe": info.get("forwardPE", "未知"),
            "return_6m": round(float(return_rate), 2),
            "volatility": round(float(volatility), 2),
            "history": hist,
        }


class NewsAgent:
    """新闻检索 Agent：从 Google News RSS 获取相关新闻"""

    def get_news(self, query: str, max_news: int = 8):
        rss_url = (
            f"https://news.google.com/rss/search?"
            f"q={query}+stock+finance&hl=en-US&gl=US&ceid=US:en"
        )
        feed = feedparser.parse(rss_url)

        news_list = []
        for entry in feed.entries[:max_news]:
            news_list.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
            })

        return news_list


class SentimentAgent:
    """情绪分析 Agent：分析新闻标题情绪"""

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, news_list):
        if not news_list:
            return {"average_score": 0, "sentiment_label": "中性", "details": []}

        results = []
        scores = []

        for news in news_list:
            score = self.analyzer.polarity_scores(news["title"])["compound"]
            scores.append(score)

            if score > 0.05:
                label = "积极"
            elif score < -0.05:
                label = "消极"
            else:
                label = "中性"

            results.append({
                "title": news["title"],
                "score": round(float(score), 3),
                "label": label,
            })

        avg_score = float(np.mean(scores))

        if avg_score > 0.05:
            final_label = "整体偏积极"
        elif avg_score < -0.05:
            final_label = "整体偏消极"
        else:
            final_label = "整体中性"

        return {
            "average_score": round(avg_score, 3),
            "sentiment_label": final_label,
            "details": results,
        }


class RiskAgent:
    """风险评估 Agent：基于波动率、估值、收益率生成风险判断"""

    def assess(self, market_data, sentiment_data):
        risks = []
        score = 0

        volatility = market_data["volatility"]
        pe_ratio = market_data["pe_ratio"]
        return_6m = market_data["return_6m"]
        sentiment_score = sentiment_data["average_score"]

        if volatility > 45:
            risks.append("股价年化波动率较高，短期价格不确定性较强")
            score += 2
        elif volatility > 30:
            risks.append("股价存在一定波动，需要关注回撤风险")
            score += 1

        if isinstance(pe_ratio, (int, float)):
            if pe_ratio > 60:
                risks.append("市盈率较高，存在估值偏贵风险")
                score += 2
            elif pe_ratio > 35:
                risks.append("估值水平偏高，需要关注业绩增长是否匹配")
                score += 1

        if return_6m > 50:
            risks.append("近半年涨幅较大，存在短期获利回吐风险")
            score += 1
        elif return_6m < -30:
            risks.append("近半年跌幅较大，市场信心可能偏弱")
            score += 1

        if sentiment_score < -0.15:
            risks.append("近期新闻情绪偏负面，可能影响市场预期")
            score += 1

        if score >= 4:
            risk_level = "高风险"
        elif score >= 2:
            risk_level = "中等风险"
        else:
            risk_level = "低到中等风险"

        if not risks:
            risks.append("未发现明显高风险信号，但仍需结合财报与宏观环境判断")

        return {
            "risk_level": risk_level,
            "risk_score": score,
            "risk_points": risks,
        }


class ReportAgent:
    """报告生成 Agent：整合所有 Agent 输出生成研究报告"""

    def generate(self, market_data, news_data, sentiment_data, risk_data):
        report = f"""
# 多 Agent 金融研究报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 一、公司基本信息

股票代码：{market_data['ticker']}  
公司名称：{market_data['company_name']}  
所属行业：{market_data['sector']} / {market_data['industry']}

## 二、市场表现

最新股价：{market_data['latest_price']}  
近 6 个月收益率：{market_data['return_6m']}%  
年化波动率：{market_data['volatility']}%  
市值：{market_data['market_cap']}  
市盈率 PE：{market_data['pe_ratio']}  
预期市盈率 Forward PE：{market_data['forward_pe']}

## 三、新闻与市场情绪

新闻整体情绪：{sentiment_data['sentiment_label']}  
平均情绪得分：{sentiment_data['average_score']}

近期相关新闻：
"""
        for i, news in enumerate(news_data, 1):
            report += f"\n{i}. {news['title']}"

        report += f"""

## 四、风险评估

综合风险等级：{risk_data['risk_level']}  
风险评分：{risk_data['risk_score']}

主要风险点：
"""
        for risk in risk_data["risk_points"]:
            report += f"\n- {risk}"

        report += """

## 五、综合结论

从市场表现、新闻情绪和风险指标来看，该股票需要结合估值水平、价格波动、近期市场情绪以及公司基本面进一步判断。

> 免责声明：本系统输出仅用于研究与学习，不构成任何投资建议。
"""
        return report.strip()


class FinanceResearchOrchestrator:
    """总控 Agent：负责任务调度与 Agent 协作"""

    def __init__(self):
        self.market_agent = MarketDataAgent()
        self.news_agent = NewsAgent()
        self.sentiment_agent = SentimentAgent()
        self.risk_agent = RiskAgent()
        self.report_agent = ReportAgent()

    def run(self, ticker: str):
        print(f"正在分析：{ticker}")

        market_data = self.market_agent.get_stock_data(ticker)
        print("金融数据获取完成")

        news_data = self.news_agent.get_news(ticker)
        print("新闻数据获取完成")

        sentiment_data = self.sentiment_agent.analyze(news_data)
        print("情绪分析完成")

        risk_data = self.risk_agent.assess(market_data, sentiment_data)
        print("风险评估完成")

        report = self.report_agent.generate(
            market_data,
            news_data,
            sentiment_data,
            risk_data,
        )

        filename = f"{ticker}_research_report.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"研究报告已生成：{filename}")
        return report


if __name__ == "__main__":
    ticker = input("请输入股票代码，例如 AAPL / TSLA / MSFT / NVDA：").strip().upper()

    system = FinanceResearchOrchestrator()
    result = system.run(ticker)

    print("\n" + "=" * 60)
    print(result)
