#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Ensure path is correct.")
    sys.exit(1)

def run_ai_news_survey(mode="weekly", model_id="anthropic/claude-opus-4-6", publish_to_kit=False):
    """
    Delegates the AI News Survey and personalized report generation to the OpenCode Agent.
    Uses axiom-based evaluation framework for evidence-tiered, builder-focused reporting.

    Args:
        mode: "weekly" (7 days) or "daily" (1 day)
        model_id: OpenCode model ID to use
        publish_to_kit: If True, publish newsletter to Kit subscribers instead of personal email
    """
    client = OpenCodeClient()

    date_str = datetime.now().strftime('%Y/%m/%d')
    date_file = datetime.now().strftime('%Y%m%d')

    if mode == "daily":
        days_back = 1
        session_title = f"Daily AI News {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        report_filename = f"daily_ai_newsletter_{date_file}.md"
        report_path = f"contexts/survey_sessions/daily_ai_newsletter/{report_filename}"
        report_title = "AI 日报"
        period_desc = "今日"
        days_desc = "1 天"
        max_lines = 100
    else:
        days_back = 7
        session_title = f"Autonomous AI News Survey {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        report_filename = f"ai_news_weekly_{date_file}.md"
        report_path = f"contexts/survey_sessions/{report_filename}"
        report_title = "AI 周报"
        period_desc = "本周"
        days_desc = "7 天"
        max_lines = 300

    session_id = client.create_session(session_title)

    if not session_id:
        print("Failed to create OpenCode session.")
        return

    if publish_to_kit:
        delivery_instruction = f"""### Phase 6：交付

- **Kit 发布**：使用 Kit Broadcast 发送给所有订阅者并发布到 web：
  ```bash
  python3 periodic_jobs/ai_heartbeat/src/v0/kit_broadcast.py {report_path}
  ```
  脚本会自动将 Markdown 转换为 HTML，并在 2 分钟后发送给所有 Kit 订阅者。
  - **邮件标题**：直接使用报告第一行的标题（如 `[鸭哥 AI 日报] 2026-02-28`）"""
    else:
        delivery_instruction = f"""### Phase 6：交付

- **邮件通知**：使用 `--file` 参数发送全文 HTML 邮件：
  ```bash
  python3 tools/send_email_to_myself.py "[鸭哥 {report_title}] {date_str}：[用一句话描述{period_desc}最重要的已验证事实]" "" --file {report_path}
  ```
  脚本会自动将 Markdown 转换为带样式的 HTML。
  - **邮件标题**：[鸭哥 {report_title}] {date_str}：[用一句话描述{period_desc}最重要的已验证事实]"""

    prompt = f"""你是一个资深的 AI 行业调研员，负责为用户生成{report_title}洞察报告。

## 第零步：读取公理体系（必须先做）

在开始任何调研之前，先读取 `rules/axioms/INDEX.md`，浏览完整公理索引并建立评估框架。

然后基于本期话题，自主选择最相关的 3-5 条公理深入阅读（不限于固定条目）。
你选择的公理将作为你的**评估函数**：决定什么值得写、什么应该过滤、如何分层呈现。

## 成功标准

这份报告的目标读者是一个 builder-practitioner：他自己动手构建 AI 系统，时间有限，需要快速区分信号与噪声。

"有用"的定义：
1. **事实与观点严格分离**：事实表在前，分析在后。读者一眼就能分辨哪些是已验证的事实、哪些是分析推断。
2. **每条事实标注证据层级**：[官方]、[一手报道]、[三方测试]、[行业分析]、[未验证]。
3. **每条事实必须附带原始来源 URL**：来源列不能只写媒体名称，必须是可点击的真实 URL（如 `[TechCrunch](https://...)`），方便读者验证。
4. **证据层级必须与来源 URL 一致**：
   - [官方] → 来源 URL 必须是官方域名（如 openai.com, anthropic.com, deepmind.google, nvidia.com, google.com 等）
   - [一手报道] → 来源 URL 应是主流媒体的直接采访或官方新闻稿
   - [三方测试] → 来源 URL 可以是技术博客的 benchmark、独立研究机构
   - [行业分析] → 来源 URL 可以是分析师报告、市场研究
   - [未验证] → 单一来源或无法追溯官方
   - 如果只能找到第三方报道官方信息，应标注 [行业分析] 而非 [官方]
5. **数字必须交叉验证**：所有关键数字（营收、融资额、benchmark 分数、用户量）必须在至少一个独立来源中确认。如果只有单一来源且为非官方来源，标注[未验证]。
6. **构建者视角**：不是"这个新闻对行业意味着什么"，而是"如果我这周要构建什么，这条信息如何影响我的决策"。
7. **噪声显式过滤**：不仅列出值得关注的，还要列出"不值得关注"的内容及原因，节省读者筛选时间。
8. **篇幅克制**：全文不超过 {max_lines} 行 Markdown。信息密度 > 覆盖广度。

## 任务执行流

### Phase 1：广度调研 + 事实采集

使用 Tavily 搜索{period_desc}（{date_str} 往前推 {days_desc}）最重大的 AI 行业进展。

搜索范围：
- 前沿模型发布（Frontier Models）
- AI 硬件与基础设施（Chips/Infra）
- Agent 生态与工具
- 安全事件与漏洞
- 监管政策与行业冲突

重点关注：OpenAI, Anthropic, Google DeepMind, DeepSeek, NVIDIA, Meta, Groq 等。

**关键原则**：
1. 每条信息采集后立即分类证据层级。不要等到写报告时才考虑可信度。
2. **记录原始来源 URL**：每条事实必须记录其来源的完整 URL，不能只记录媒体名称。
### Phase 2：数字验证 + 交叉核查

对 Phase 1 中采集到的关键数字逐一验证：
- 财务数据（营收、融资额、估值）→ 找官方财报或 SEC 文件
- Benchmark 分数 → 找官方公告中的原始数据
- 用户量/采用率 → 区分官方数据和第三方估算
- 产品功能声明 → 找官方文档或发布博客

**规则**：如果某个数字只出现在博客或分析文章中，且无法追溯到一手来源，必须标注[未验证]或[行业分析]，不得以[官方]呈现。宁可不写某个数字，也不要写一个错误的数字。

### Phase 3：构建者视角筛选

用以下过滤器决定哪些内容进入报告的"构建者视角"section（最多 2-3 个议题）：

过滤条件（至少满足一项）：
1. **直接影响构建决策**：比如某个 API 价格变化、新模型能力对技术选型的影响、安全漏洞对现有系统的威胁
2. **有定量支撑的趋势信号**：不是"AI 正在改变一切"式的叙事，而是有具体数字支撑的趋势转折点
3. **与用户公理体系产生化学反应**：与 V02（可验证性）、T08（第一性原理）、A03（IC→Manager）、A09（构建者思维）等公理产生实质性共鸣或张力

淘汰条件（任一即淘汰）：
- 纯叙事无数据（"这标志着范式转移"）
- 产品公告无发布日期或可测试产品
- 融资新闻无技术实质
- 通用 AI 发展预测（"2027年将实现 AGI"）

### Phase 4：报告撰写

报告结构（严格按此顺序）：

```
# [鸭哥 {report_title}] YYYY-MM-DD

**覆盖周期**：...

## 一、{period_desc}事实表
（表格形式，每条标注证据层级和来源 URL）
（子分类：前沿模型、融资与估值、安全事件等）

## 二、构建者视角
（2-3 个高密度议题，每个包含：事实 → 定量支撑 → 对构建者的实际意义）

## 三、定量锚点
（表格形式，所有已验证的关键数字汇总）

## 四、值得警惕
（安全风险、供应链风险、需要立即行动的事项）

## 五、不值得关注（噪声过滤）
（显式列出被过滤的内容及过滤理由，节省读者时间）
```

### Phase 5：自我审视（必须执行）

**重要**：自我审视结果直接在 chat response 中输出，不要写入 Markdown 文件。只有发现需要修正的问题时，才编辑已保存的 md 文件。

在报告写完后，回顾整篇报告并回答：
1. 是否有任何数字只有单一来源且未标注[未验证]？如果有，修正证据层级。
2. 是否有任何"我的判断"式的段落混在事实表中？如果有，移到"构建者视角"section。
3. 全文是否超过 {max_lines} 行？如果超过，删减信息密度最低的部分。
4. "不值得关注"section 是否为空？如果是，说明过滤器太松，重新审视。
5. 是否有任何原始调研中出现了错误数字（如量级错误、单位混淆）？如果有，说明具体问题。

{delivery_instruction}

## 写作风格要求

- 中文为主，技术术语保留英文原文
- 理性内敛，不堆砌宏大词藻。"这标志着范式转移"不如"Terminal-Bench 从 64% 跳到 77.3%"
- 不要写"我的判断"——这是 AI 生成的报告，不要假装是读者本人的判断
- 不要写"对鸭哥的启发"式的通用建议——如果建议不够具体到可以立即执行，就不要写
- 不要用 emoji 或重要性星级等——用证据层级标签代替
- 不用"值得关注""非常重要"等主观强调词——让数据说话

请开始执行。
"""
    print(f"Triggering {mode} news survey in OpenCode (Session: {session_id})...")
    print(f"Using model: {model_id}")
    if publish_to_kit:
        print("Publish mode: Kit subscribers")

    result = client.send_message(session_id, prompt, model_id=model_id)

    if not result:
        print("No immediate response from server. Sending continuation ping...")
        result = client.send_message(session_id, "继续", model_id=model_id)

    if result:
        client.wait_for_session_complete(session_id)
        messages = client.get_session_messages(session_id) or []
        assistants = [m for m in messages if (m.get("info") or {}).get("role") == "assistant"]
        if assistants:
            last_info = assistants[-1].get("info") or {}
            print(f"Resolved model: {last_info.get('providerID')}/{last_info.get('modelID')}")
        print(f"{report_title} complete.")
    else:
        print("Failed to start survey session.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI news survey (daily or weekly)")
    parser.add_argument("--mode", "-m", choices=["daily", "weekly"], default="weekly",
                        help="Survey mode: 'daily' (1 day) or 'weekly' (7 days, default)")
    parser.add_argument("--model", "-M", default="anthropic/claude-opus-4-6",
                        help="OpenCode model ID (default: anthropic/claude-opus-4-6)")
    parser.add_argument("--publish-to-kit", "-k", action="store_true",
                        help="Publish newsletter to Kit subscribers instead of personal email")
    args = parser.parse_args()

    print(f"Starting AI News Survey ({args.mode})...")
    run_ai_news_survey(mode=args.mode, model_id=args.model, publish_to_kit=args.publish_to_kit)
    print("Survey process finished.")
