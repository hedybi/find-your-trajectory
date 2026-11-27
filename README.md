# Find Your Trajectory — Scholar Edition

**Find Your Trajectory** starts with **Scholar Edition**, an open, portable **agent skill** for understanding a scholar’s ideas: theoretical routes, bilingual foundations, paper-level mechanisms, related active researchers, and research-to-practice connections. It is not an automatic tool for exhaustively crawling every paper on the web.

This first release is the `scholar-atlas` skill for understanding scholars. Personal trajectory planning is a possible future direction and is not implemented in this release.

The core contribution is an evidence model and transferable research workflow. Direct citation, conceptual development, application, comparison and mentorship are different relationships. Documented partnerships, reported outcomes and future proposals remain visibly different claims.

## Use

Use `skills/scholar-atlas/SKILL.md` directly with an agent that can read local instructions, or copy the `scholar-atlas` directory into your agent’s supported skill location. No installation is performed by this repository. The `agents/openai.yaml` file supplies optional Codex UI metadata; the instructions and JSON remain portable.

Example request:

> Use $scholar-atlas to explain this scholar’s theoretical development. Start with an overview, then give Chinese–English concepts, evidence-backed routes, three relevant active scholars and clearly labelled practical proposals. Show a source overview and references beside key claims in the final report, with the corpus and access limits.

The workflow can produce Markdown, JSON, SVG, or a website. If a website is requested and a Sites skill is available, use that implementation workflow; Sites is optional and is not a runtime dependency. Publishing and contacting people require the user’s authorization.

Every final website or report must make its sources visible: a **Sources and coverage** overview plus specific references beside key claims. Source cards identify the official profile, Google Scholar/index entry, original paper or other material; explain its role, inspected portion and access limits; and give the observation date and relevant passage location. Scholar supports discovery and bibliographic checks, not original theoretical claims. Full texts, selected passages, index-only records, failed access attempts and private archives remain distinguishable. Private material gets a permitted attribution and access limitation, never a private path or fabricated public link. Sources cannot be confined to the research chat or an unseen JSON file, and the output must not imply exhaustive verification.

## Validate

Python 3.9+; standard library only:

```bash
python3 skills/scholar-atlas/scripts/validate_atlas.py examples/synthetic-atlas.json
python3 tests/test_validator.py
```

The validator checks reference integrity, DOI normalization and duplicate detection, work/version counts, bilingual fields, edge evidence categories, and impact status. It cannot establish source truth, historical priority, comprehensiveness, translation quality, causal impact, or whether citations are visible in the final rendered artifact. The forward acceptance review checks reader-facing provenance. Read `references/evidence-rules.md` inside the skill for the review standard.

`examples/synthetic-atlas.json` is a small **fictional** demonstration, not research evidence. `evals/forward-test.md` and its separate raw packet support independent acceptance testing. The repository contains no real scholar’s private archive or hosted-site identifiers.

## 中文说明

**Find Your Trajectory（找到你的轨迹）**首版为 **Scholar Edition（学者版）**：一个可开源、可迁移的**学者研究导览技能包**，帮助读者从总览进入理论根基、中英术语、机制细节、相关活跃学者和产学研联系。它不是自动穷尽全网论文的爬虫，也不保证获得所有全文。

当前交付的技能标识仍为 `scholar-atlas`，聚焦理解学者的研究轨迹。个人路径探索可以作为后续扩展方向，目前尚未实现。

它的重点是证据分级：引用不等于师承，时间顺序不等于理论继承，主题相关不等于已经合作。每条路线都能回到来源和定位；作者主张、导览者解释、未知事项及未来建议分别标明。论文与版本分开记录，避免把预印本、在线发表和正式卷期重复算成多项成果。

**最终网页或报告本身必须清晰展示来源。** 除来源总览外，关键断言旁还要有具体出处和页码、章节等定位；每个来源说明用途、实际访问/阅读范围及核验日期。学者官方主页、Google Scholar 等索引与论文原文各有用途，不能用 Scholar 替代理论原文证据。已读全文、仅读选段或摘要、仅查索引、访问失败与用户私有档案要明确区分；私有档案另标公开限制，不暴露私有路径或编造链接。不能只在研究过程或隐藏数据里保留引用，也不能把有限核验说成全量读完。

把 `skills/scholar-atlas` 交给支持本地技能的代理即可使用；仓库不会自动安装技能、建立远端或发布网站。上面的两个命令可验证合成示例及主要约束。详细规则见技能内的 `references/`。可选网站输出能调用现有 Sites 技能，但基础使用不依赖任何专有插件。

本项目以 MIT 许可发布。该许可覆盖仓库原创代码、文档及虚构示例，不改变外部论文、图片或其他来源的版权。
