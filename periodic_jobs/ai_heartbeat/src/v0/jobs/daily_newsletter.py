#!/usr/bin/env python3
"""
Daily newsletter generator for 「鸭哥 AI 手记」.

Two-loop architecture: extract topics from group chat, run parallel research,
apply axiom lens to identify gaps, run targeted second research, then write.

Usage:
  python daily_newsletter.py               # Run for yesterday (default)
  python daily_newsletter.py --date 20260301  # Run for a specific date
  python daily_newsletter.py --dry-run     # Generate only, skip Kit publish
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Ensure path is correct.")
    sys.exit(1)


DEFAULT_MODEL = "anthropic/claude-opus-4-6"


def run_daily_newsletter(date_str: str, dry_run: bool = False, model_id: str = DEFAULT_MODEL):
    """
    Triggers a newsletter generation session in OpenCode.

    Args:
        date_str: Date in YYYYMMDD format (e.g. "20260301")
        dry_run: If True, generate newsletter file but skip Kit publish
        model_id: OpenCode model ID to use
    """
    client = OpenCodeClient()

    date_display = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    session_title = f"Daily Newsletter {date_display}"
    session_id = client.create_session(session_title)

    if not session_id:
        print("Failed to create OpenCode session.")
        return

    chat_csv = f"periodic_jobs/ai_heartbeat/daily_messages/{date_str}.csv"
    output_path = f"contexts/survey_sessions/daily_ai_newsletter/ai_frontline_{date_str}.md"

    # Guard: abort if chat CSV doesn't exist
    if not Path(chat_csv).exists():
        print(f"ABORT: Chat CSV not found: {chat_csv}")
        print("The WeChat export for this date has not been generated yet.")
        print("This usually means the Windows-side rsync trigger did not fire.")
        print("To manually export, run:")
        print(f"  cd periodic_jobs/wechat_db_parser && .venv/bin/python scripts/daily_export_messages.py --data-dir Msg --date {date_str}")
        return

    if dry_run:
        publish_step = """## Phase 7：跳过发布（dry-run 模式）

文件已生成，不发布到 Kit。"""
    else:
        publish_step = f"""## Phase 7：发布到 Kit

运行以下命令发送邮件给所有订阅者并发布到 web：

```bash
source periodic_jobs/ai_heartbeat/.venv/bin/activate && \\
  python periodic_jobs/ai_heartbeat/src/v0/kit_broadcast.py \\
  {output_path}
```

脚本会在 2 分钟后自动发送。输出 broadcast ID 给用户以便跟踪。"""

    prompt = f"""你是「鸭哥 AI 手记」的编辑，负责为 {date_display} 生成当期 newsletter。

本任务采用「双循环」架构：先从群聊提取话题并做并行调研，再用公理体系识别缺口做二次调研，最后写作。严格按以下 7 步顺序执行，不要跳步。

---

## Phase 0：读取框架文件

先读以下文件建立框架：

- `periodic_jobs/ai_heartbeat/docs/newsletter_design.md` — newsletter 完整设计规范（必读）
- `contexts/survey_sessions/daily_ai_newsletter/ai_frontline_20260301.md` — 首期样本（格式和语气的参考标杆，注意 blockquote + 懒人包 + `---` 分隔 + 也值得知道的格式）
- `rules/skills/workflow_parallel_subagents.md` — 并行 agent 调度方法（Phase 2 需要）

**注意**：此阶段不读公理文件。公理是 Phase 3 的思维透镜，必须在看过群聊和初步调研结果之后再读，这样才能按需选择最相关的公理。


## Phase 1：群聊话题提取

读取 `{chat_csv}`。CSV 格式：`sender,content`，其中「鸭哥」是用户本人。

仔细阅读全文，提取 2-3 个有信息密度、值得深入的话题。每个话题输出一张**话题卡片**（在 chat response 中，不写文件）：

```
### 话题 N：[话题名称]
- 一句话描述：...
- 这个话题真正服务的判断：...[这不是材料摘要，而是你准备在正文里成立的核心判断]
- 读者为什么该关心：...[一句话说清这段的阅读价值]
- 群聊关键发言摘录：（2-3 条最有信息量的原话）
- 群聊中分享的相关链接：（群友在讨论中分享的 URL，包括 yage.ai/share 链接、个人博客、GitHub 项目等。这些链接本身就是正文素材，不只是 citation）
- 正文只该保留的 1 个关键细节：...[如果这个话题里有很多产品/方案细节，先决定哪一个细节最值得进正文，其余留在调研层]
- 待调研问题：
  1. [具体问题，不是泛泛的"搜一下这个话题"]
  2. ...
  3. ...
```

话题选择标准：
- 忽略闲聊、表情包、纯粹社交互动
- 寻找有技术深度的讨论、行业观察、有争议的判断
- 识别能连接到更大行业现象的讨论线索
- 特别关注鸭哥本人的发言，他的观察和判断是 newsletter 的核心视角

---

## Phase 2：并行调研

**在执行本步之前，先读 `rules/skills/workflow_parallel_subagents.md`**。

根据 Phase 1 的话题卡片，同时启动多个 background librarian agent：

1. **每个话题一个 agent**：将话题卡片中的「待调研问题」作为该 agent 的调研方向。每个 agent 的 prompt 要求：
   - 针对话题的 3-5 个具体子问题做深入搜索
   - 返回中文摘要，500-800 字
   - 所有关键数据点必须附带来源 URL
   - 聚焦事实和数字，不要泛泛而谈

2. **一个广谱新闻 agent**：不限于群聊话题，扫描当日（{date_display}）AI 领域的重大新闻，涵盖前沿模型、融资、安全事件、监管政策等。这个 agent 的发现可能成为「也值得知道」的素材，也可能与群聊话题形成意外的同构映射。

**启动所有 agent 后，等待系统通知，不要轮询。**

**结果收集（关键）**：收到系统通知后，对每个 agent 调用 `background_output(task_id="...", full_session=true)` 获取完整结果。如果返回 `has_more: true`，用 `message_limit` 参数增大范围直到拿到全部内容。**确认所有 agent 的完整输出都已收集后，才进入 Phase 3。** 不完整的调研数据会直接导致 newsletter 缺乏深度。

---

## Phase 3：公理驱动的整合与缺口识别

收到所有调研结果后，做以下四件事：

### 3a. 读取公理索引
现在（而不是更早）读 `rules/axioms/INDEX.md`，浏览全部公理类别和条目。带着 Phase 1 的话题和 Phase 2 的调研结果去读，这样你能准确判断哪些公理与本期话题最相关。

### 3b. 初步交叉对照
将群聊话题和调研结果对照，初步找出：
- 群聊讨论和外部新闻之间的**同构映射**（结构性共鸣）
- 群聊不同讨论线索之间的隐藏连接
- 广谱新闻中与群聊话题意外呼应的条目

### 3c. 公理精读
根据话题内容，从 `rules/axioms/INDEX.md` 中选择 2-3 个最相关的公理，**读对应的详细文件**。例如：
- 话题涉及「什么在变贵/变便宜」→ 读 T05（认知是资产）
- 话题涉及「委托 AI 做事的质量」→ 读 A03（IC 到管理者）
- 话题涉及「工具选择」→ 读 A09（构建者思维）

### 3d. 缺口识别
用公理作为思维透镜重新审视 Phase 2 的材料，回答：
- 有哪些更深的问题在第一轮调研中没有被问到？
- 论证链上有哪些缺口需要补数据？（比如：群聊说了一个判断，调研既没有证实也没有证伪）
- 有哪些看似不相关的线索之间存在公理层面的隐藏连接，但缺少事实支撑？

输出：**二次调研清单**（2-4 个具体的查询/问题），在 chat response 中列出。

---

## Phase 4：二次针对性调研

根据 Phase 3 的二次调研清单，启动 1-2 个 background librarian agent 做精准补充。

这一轮的查询是公理视角催生的，不是简单重复第一轮，所以应该能挖到第一轮挖不到的深度。每个 agent 的 prompt 同样要求附带来源 URL 和具体数据。

等待结果返回后进入下一步。如果 Phase 3 判断材料已经足够充分（所有论证链都有支撑），可以跳过此步直接进入 Phase 5。

---

## Phase 5：写 newsletter 并保存

综合所有材料（群聊 + 两轮调研 + 公理视角），按以下规范写作，写完直接保存到 `{output_path}`。

### 结构骨架（严格遵循）

```markdown
# [鸭哥 AI 手记] {date_display}

> [一句话揭示所有主题的暗线，是洞察不是摘要]

**懒人包：[一两句话概括 2-3 个话题的核心要点]**

## [话题一标题]

[段落...]

[段落...]

---

## [话题二标题]

[段落...]

---

## 也值得知道

**[标题]**：[一两句话 + 来源链接]

**[标题]**：[一两句话 + 来源链接]

---

[固定 Footer]
```

### 深度要求（最重要，优先级高于选题数量）

以下是导致 newsletter 失败的最常见模式，必须避免：

1. **禁止复述**：群聊中的讨论是切入点，不是内容本身。如果你的章节基本上是群友发言的改写，那就是失败的。你的工作是在群友的观察上叠加分析层，问出他们没问的问题，找到他们没看到的连接。
2. **每个话题必须有纵深**：从群聊的一个观察出发，至少往下挖两层。第一层：这个观察背后的结构性原因是什么？第二层：这个结构性原因有什么非显然的推论，它在哪些看似不相关的领域也在起作用？
3. **用外部数据深化，不是装饰**：调研到的数字和事实应该推进论证，而不是贴在观点旁边做注脚。好的用法："基准测试显示 X 在 A 上领先、Y 在 B 上领先，这印证了两种不同的设计哲学"。坏的用法："根据最新数据，X 的市场份额达到了 N%"。
4. **找同构映射**：在群聊的不同讨论线索之间、或群聊讨论和外部新闻之间，发现结构性共鸣。如果找不到自然的映射不要硬凑，但要主动寻找。
5. **公理是思维透镜**：用 Phase 3 精读的公理的思维方式去分析话题，但绝对不要在正文中提及公理名称或编号。读者看到的是洞察和分析，不是你的思考框架。
6. **主题是判断，不是材料堆**：一个话题里可以有很多项目名、产品名、benchmark、机制细节，但正文只展开最能支撑核心判断的那一小部分。其余材料只在需要时点到为止，不要写成 inventory。
7. **优先回答这段为什么值得读**：每个章节开头先用一句话说清这段最重要的判断或价值，再进入案例和数据。不要先铺材料，再让读者自己猜这段的重点。

### 可读性要求（与深度同等重要）

深度不等于晦涩。以下规则确保文章读起来顺畅：

1. **先给画面，再给道理**：每个观点先用具体场景打底，再提炼规律。不要一上来就堆抽象概念。
2. **一段只说一件事**：两个论点或两组数据就拆成两段。给读者喘息空间。
3. **长句拆短**：超过 50 字的句子拆成两句。逗号不能代替句号。
4. **抽象概念必须有具体托底**：出现"结构性变化"类抽象词时紧跟具体例子。找不到例子就不要用这个词。
5. **归属准确**：鸭哥的发言用"鸭哥"称呼，其他群友用"有人"或"群里有人"。
6. **语气像聊天**：多用"你会发现""说白了""为什么？"这类口语化过渡。不要像分析报告。
7. **跨案例切换先搭桥**：从案例 A 跳到案例 B 之前，先显式说出它们共享的命题，再切到下一个例子。只要读起来有"这怎么突然跳到这儿"的感觉，就说明桥没搭好。
8. **说清单位和时间窗口**：涉及成本、token、时长、频率、规模时，明确写清是单次、单周、单月、累计，避免让读者自己换算。
9. **群里已分享过的链接也是正文素材**：如果群聊里已经分享过一篇文章、调研或链接，它不只是 citation，也可以作为叙事上下文的一部分。需要时把这个上下文自然带上。

### 结构
1. **开头 blockquote**：一句话揭示本期所有主题的暗线（是洞察不是摘要）
2. **懒人包**：blockquote 后紧跟一段加粗的「**懒人包**」，用一两句话概括本期 2-3 个主题的核心要点，方便读者快速判断是否继续阅读
3. **2-3 个主题章节**：每章自然引出群聊讨论作为切入点，再用外部数据深化。鸭哥的发言用"鸭哥"称呼，其他群友用"有人"或"群里有人"
4. **也值得知道**：2-3 条简短新闻，附来源链接（可以来自广谱新闻 agent 的发现）
5. **Footer**（固定，见下）

章节之间用 `---` 分隔。

### 语气
- 中文为主，技术术语保留英文
- 理性内敛，不堆砌词藻
- 有观点但不说教，让分析自然引向结论
- 所有关键 claim 必须有内联来源链接，格式：`（[来源名](URL)）`
- 不用 emoji，不用破折号（——）
- 尽量用自然段落，顶层以外避免 bullet points

### 篇幅
全文 55-75 行 Markdown，信息密度优先于覆盖广度。

### 保存与验证
写完后立即保存到 `{output_path}`。保存后运行 `wc -l` 确认行数在 55-75 范围内。如果不在范围内，调整后重新保存。

### Footer（固定）
```
---

*本期素材来自 AI Builder Space 社群讨论与公开 AI 行业信息的交叉验证。*

*本文由AI综合领域调研和微信群聊自动生成。请注意甄别幻觉。*

*订阅本 newsletter：[yage-ai.kit.com](https://yage-ai.kit.com/)*
```

---

## Phase 6：自我审视（必须执行）

**重要**：自我审视结果在 chat response 中输出，不写入文件。只有发现需要修正的问题时，才回去编辑 `{output_path}`。

文件已在 Phase 5 保存。现在重新读取保存的文件，逐项检查：
1. 是否有任何话题只是群聊发言的复述/改写，缺少你叠加的分析层？如果是，重写该话题。
2. 每个话题是否至少往下挖了两层（结构性原因 → 非显然推论）？如果某个话题只有一层，补充深度。
3. 全文是否在 55-75 行 Markdown 范围内？如果超出，删减信息密度最低的部分。
4. 所有关键 claim 是否都有内联来源链接？如果有裸 claim，补充来源或标注[未验证]。
5. 是否有任何公理名称或编号出现在正文中？如果有，改为用公理的思维方式分析，删除显式引用。
6. 「也值得知道」section 是否为空？如果是，从广谱新闻 agent 的结果中补充 2-3 条。
7. 是否有任何段落把一个产品/项目写成了 feature list，而没有服务更大的判断？如果有，压缩到只保留 1 个最关键细节，把篇幅让给判断本身。
8. 是否有任何跨案例切换缺少桥接句，让读者感觉突然跳转？如果有，补一句共享命题，再保留例子。
9. 是否有任何成本、token、时长、规模的表述缺少单位或时间窗口？如果有，补成单次/单周/单月/累计等明确表述。
10. **句式与沟通风格审查**（参照 `rules/COMMUNICATION.md`）：逐段扫描全文，检查以下违规模式并逐一修正：
   - **否定句式**：找出所有「不是 X 而是 Y」「不是 X，是 Y」「X 不在于 Y，而在于 Z」类句式，改为正向陈述。原则：直接说 X 是什么，不要先说它不是什么。例如「这不是技术问题，而是管理问题」→「这是个管理问题」；「关键不在工具，在于心智」→「关键在于心智」。
   - **破折号**：找出所有「——」「—」「--」，拆成两句或改用冒号、分句。
   - **华丽辞藻与营销语气**：删除「惊喜」「震撼」「颠覆」等词。
   如果发现违规，直接在已保存的 md 文件中修正，并在 chat response 中列出修正清单。

修正完成后进入下一步。

---

{publish_step}
"""

    print(f"Triggering daily newsletter for {date_display} (Session: {session_id})...")
    print(f"Model: {model_id}")
    print(f"Chat CSV: {chat_csv}")
    print(f"Output: {output_path}")
    if dry_run:
        print("Mode: dry-run (no Kit publish)")

    result = client.send_message(session_id, prompt, model_id=model_id)

    if not result:
        print("No immediate response from server. Sending continuation ping...")
        result = client.send_message(session_id, "继续", model_id=model_id)

    if result:
        client.wait_for_session_complete(session_id)
        messages = client.get_session_messages(session_id) or []
        assistants = [m for m in messages if (m.get("info") or {}).get("role") == "assistant"]
        if assistants:
            info = assistants[-1].get("info") or {}
            print(f"Resolved model: {info.get('providerID')}/{info.get('modelID')}")
        print(f"Newsletter for {date_display} complete.")
    else:
        print("Failed to start newsletter session.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate daily AI newsletter")
    parser.add_argument(
        "--date", "-d",
        default=(datetime.now() - timedelta(days=1)).strftime("%Y%m%d"),
        help="Date in YYYYMMDD format (default: yesterday)",
    )
    parser.add_argument(
        "--model", "-M",
        default=DEFAULT_MODEL,
        help=f"OpenCode model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Generate newsletter file but skip Kit publish",
    )
    args = parser.parse_args()

    print(f"Starting daily newsletter generation for {args.date}...")
    run_daily_newsletter(date_str=args.date, dry_run=args.dry_run, model_id=args.model)
    print("Done.")
