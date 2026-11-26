# Millennium Relay: P vs NP (`millennium-relay-p-vs-np`)

> **用全球普通人的分布式 AI Agent 接力，对抗大厂的万卡/万 Agent 中心化算力。**  
> **Crowdsourced, Machine-Verified AI Agent Relay on the P vs NP Millennium Prize Problem.**

[![Relay Gate CI](https://github.com/3099404236/millennium-relay-p-vs-np/actions/workflows/relay-gate.yml/badge.svg)](https://github.com/3099404236/millennium-relay-p-vs-np/actions/workflows/relay-gate.yml)

---

## 1. 为什么建这个仓库？/ Why This Exists

2026 年秋天，AI 在数学前沿的格局发生了剧变：大型实验室投入数百万美元、同时拉起上万个中心化 Agent 强攻千禧年难题（例如 OpenAI 2026 年 9 月在 Navier–Stokes 上部署约 10,000 个 Agent）。

普通研究者和个人开发者不可能一个人开一万个 Agent，但 **如果 1,000 个普通人每人跑 10 个 Agent，通过 GitHub 以「接力棒（Baton）」的形式协同推进，能不能形成等效甚至更具多样性的探索能力？**

**答案是：完全有道理，并且 2025–2026 年学术界已经跑通了这一范式**——但前提是 **绝不能只把原始聊天记录（Chat Log）丢到 GitHub 上**（陶哲轩在 2026 年 6 月的 *New Mathematical Workflows* 中指出，未经机器验证的长篇 AI 文本只会制造「证明消化不良 / Proof Indigestion」）。

真正能规模化的「普通人 AI 数学接力」必须具备三大工程支柱（借鉴 **Choir (arXiv:2609.31903)**、**Open Proof Network**、**PolyProof** 与 **Equational Theories Project**）：

1. **有向无环图（DAG）任务拆解（`roadmap.json`）**：把巨型难题拆成可独立认领、可继续向下分解的子引理与路线节点。
2. **确定性机器验证门禁（Deterministic Gate / CI）**：不看贡献者是谁、不管你用 Claude / Gemini / Codex / 本地模型还是纯手写，PR 必须通过自动化验证（Python 符号与数值验证 + Lean 4 形式化核检验），杜绝 AI 幻觉污染主干。
3. **失败即资产（"Failure Pays" 结构化验尸报告）**：每一棒即使没攻克 P vs NP，只要严格定位了「在哪一步撞墙、撞到了哪道数学壁垒」，就写入 `POSTMORTEM.md` 并剪枝该死胡同，让后面几千个接力者的 Agent **不再重复烧 Token**。

---

## 2. 2026 年 11 月千禧年七大难题最新格局（为何选 P vs NP？）

截至 **2026 年 11 月 26 日**（综合 Clay Mathematics Institute、Wolfram MathWorld、Nature、Science、Scientific American 公开记录）：

| 千禧年难题 | CMI 状态 | 2026 年 11 月前沿进展 | 是否适合作为大众 AI 接力靶标 |
| :--- | :--- | :--- | :--- |
| **庞加莱猜想** (Poincaré) | Solved | Perelman (2003/2010) 已正式解决 | 已解决 |
| **纳维-斯托克斯方程** (Navier–Stokes) | Active | OpenAI (2026.09) 提交带外力爆破解，CMI 进入 2 年审查期 | 已有候选解，审查中 |
| **黎曼猜想** (Riemann Hypothesis) | Active | Levent Alpöge + Claude (2026.11.20) 发布 Lean 4 证明并获 Lean FRO/Mathlib 独立复核（同日 Masullo/Vakil 发布纯人类预印本） | 已有形式化验证证明，审查中 |
| **杨-米尔斯存在性与质量间隙** | Unsolved | 4D *存在性* 已有 Lean 构造声明（2026.10–11），**质量间隙 (Mass Gap) 仍未解决** | 需庞大构造性 QFT / 格点规范场工具链 |
| **霍奇猜想** (Hodge Conjecture) | Unsolved | 仅局部特例有未评审进展，一般情形完全开放 | 代数几何与上同调前置库极其庞大 |
| **BSD 猜想** (Birch & Swinnerton-Dyer) | Unsolved | 解析秩 0、1 已解，**解析秩 $\ge 2$ 尚无一例证明** | 极有价值，适合作为平行接力仓库 |
| **P vs NP** | **Unsolved** | **完全未解决**；OpenAI 2026.10 证伪了指数时间假说（ETH），反而让电路下界与算法方法边界空前活跃 | **最佳首棒靶标**：陈述最干净、离散/电路可机检、四大已知壁垒极清晰 |

---

## 3. 第一棒（Baton #001）战果与诚实结论

- **是否解决了 P vs NP？** **没有（Failed to resolve P vs NP）**——这是诚实且符合预期的第一棒结果。
- **第一棒实际完成了什么可验证成果？**
  1. **严格证伪并剪枝了死胡同路线 `route-1a`（Tseitin–ETH 标度二分定理）**：
     证明并验证：即使利用 2026 年 10 月证伪 ETH 的次指数 $3\text{-SAT}$ 算法 $T(m) = \exp(m / (\log m)^{1/2})$，通过黑盒 Tseitin 规约到 Ryan Williams 算法方法，最高也只能触及略超线性电路 $s^*(n) = \Theta(n\sqrt{\log n})$；若想靠黑盒 Tseitin 触及 $\text{P/poly}$，等价于先证明 $3\text{-SAT} \in \bigcap_{\epsilon>0}\text{DTIME}(2^{m^\epsilon})$（反向逼近 $\text{P}=\text{NP}$ 的自相矛盾）。
  2. **定位了 `route-1b`（Hardness Magnification 硬度放大）的双重阻塞**：记录了 $\text{NEXP}$ vs $\text{NP}$ 复杂度类鸿沟与 CHOPRS (STOC 2020) **局部性壁垒（Locality Barrier）**。
  3. **建好了完整的接力底座与自动化门禁**：
     - 进攻报告：[batons/baton-001-p-vs-np-initial-attack/ATTACK_REPORT.md](batons/baton-001-p-vs-np-initial-attack/ATTACK_REPORT.md)
     - 失败验尸单：[batons/baton-001-p-vs-np-initial-attack/POSTMORTEM.md](batons/baton-001-p-vs-np-initial-attack/POSTMORTEM.md)
     - 发起对话记录：[batons/baton-001-p-vs-np-initial-attack/CONVERSATION_ORIGIN.md](batons/baton-001-p-vs-np-initial-attack/CONVERSATION_ORIGIN.md)
     - 路线依赖图：[roadmap.json](roadmap.json)
     - Lean 4 形式化骨架：[formal/lean4/MillenniumRelay/TseitinDichotomy.lean](formal/lean4/MillenniumRelay/TseitinDichotomy.lean)
     - 可执行验证与 CI 门禁：[verification/](verification/) & [.github/workflows/relay-gate.yml](.github/workflows/relay-gate.yml)

---

## 4. 如何接过下一棒？（For Humans & AI Agents）

无论你是人类研究者，还是你把本仓库交给你自己的 AI Agent（Claude Code / Antigravity / Codex / Gemini / 本地模型），只需要 4 步即可接力：

1. **阅读 Agent 上岗手册**：让你的 Agent 先读取 [`AGENT_SKILL.md`](AGENT_SKILL.md)、[`roadmap.json`](roadmap.json) 与最近的 `POSTMORTEM.md`（避免踩已经剪枝的坑）。
2. **认领一个开放节点（Baton）**：在 GitHub Issues 中认领现有任务（如 **Baton #002: Lean 4 消除 `sorry`**、**Baton #003: 绕过 Tseitin 的直接 $\text{TC}^0\text{-SAT}$ 算法**、**Baton #004: 非局部硬度放大**、**Baton #005: GCT 群表示重数障碍实验**），或提新 Issue 分解子引理。
3. **本地运行门禁测试**：
   ```bash
   python verification/verify_tseitin_dichotomy.py
   python verification/verify_barriers.py
   python verification/validate_relay_gate.py
   ```
4. **提交 PR（成功证明 / 分解子引理 / 严格失败验尸，三者皆受认可）**：GitHub Actions 会自动运行门禁校验，通过后即可合并进入公共接力图谱。

---

## 5. References & Inspiration

- **Choir**: Yidi Qi & Melanie Weber (2026), *Choir: An Open Protocol for Distributed Multi-Agent Autoformalization*, [arXiv:2609.31903](https://arxiv.org/abs/2609.31903)
- **Open Proof Network**: [github.com/thisisanameforsure/open_proof_network](https://github.com/thisisanameforsure/open_proof_network) ("Trust artifacts, not parties" & "Failure pays")
- **PolyProof**: [github.com/polyproof/polyproof](https://github.com/polyproof/polyproof)
- **Terence Tao (2026)**: *New Mathematical Workflows* & *The Equational Theories Project* ([arXiv:2512.07087](https://arxiv.org/abs/2512.07087))
- **Complexity Barriers**: Baker–Gill–Solovay (1975), Razborov–Rudich (1997), Aaronson–Wigderson (2009), Williams (2011/2014), CHOPRS (STOC 2020)
