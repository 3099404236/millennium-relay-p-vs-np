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

## 3. 接力战报总览（已完成 15 棒：Wave 1 #001 + Wave 2 10-Agent 排雷 #002–#011 + Wave 3 幸存缝隙深潜 #012–#015）

- **目前是否解决了 P vs NP？** **没有（`p_vs_np_resolved: false`）**——全仓严格遵守诚实原则与机检门禁，绝不伪造未验证的“已证明”声明。
- **15 棒已完成的全部可验证成果（16 套 Python 验证脚本 + 2 份 Lean 4.12 零 `sorry` 形式化文件由 GitHub Actions 真实内核编译验证）**：

| 棒次 | 路线 / 模块 | 状态 | 核心可验证结论、新算出的前沿数据与剪枝边界 | 验证脚本 |
| :--- | :--- | :--- | :--- | :--- |
| **Baton #001** | 黑盒 Tseitin + 次指数 3-SAT（ETH 证伪接入 Williams 方法） | `pruned` | 证明黑盒 Tseitin 最高仅达 $s^*(n)=\Theta(n\sqrt{\log n})$；触及 $\text{P/poly}$ 等价于 $3\text{-SAT}\in\bigcap_{\epsilon>0}\text{DTIME}(2^{m^\epsilon})$ | [`verify_tseitin_dichotomy.py`](verification/verify_tseitin_dichotomy.py) / [`verify_barriers.py`](verification/verify_barriers.py) |
| **Baton #002** | Lean 4.12 形式化证明（`TseitinDichotomy.lean`） | `verified` | 零 Mathlib、零自定义公理消除全部 `sorry`，320,000 组穷举复核 + GitHub Actions `lake build` 内核绿灯 | [`verify_baton_002_lean_proof.py`](verification/verify_baton_002_lean_proof.py) |
| **Baton #003** | 绕过 Tseitin 的直接 $\text{TC}^0\text{-SAT}$ 算法 | `blocked_by_barrier` | 零 Tseitin 深度-2 阈值求解器剪枝 92.9% 搜索量；验证 Chen–Tell 与 Allender–Koucký 永不相交及 BRS 通分次数爆炸 | [`verify_baton_003_tc0_sat.py`](verification/verify_baton_003_tc0_sat.py) |
| **Baton #004** | 非局部硬度放大与 CHOPRS 局部性壁垒 | `blocked_by_barrier` | 认证 $n=3$ 全部 256 个布尔函数精确电路规模（14 NPN 类）；分离 Hirahara 非黑盒归约的「非一致编码长度悖论」 | [`verify_baton_004_magnification_locality.py`](verification/verify_baton_004_magnification_locality.py) |
| **Baton #005** | 几何复杂度理论（GCT）：积和式 vs 行列式 | `blocked_by_barrier` | 符号验证 Grenet $7\times 7$（`perm_3`）与 $15\times 15$（`perm_4`）矩阵；重现 BIP (JAMS 2019) 出现障碍 100% 失效 | [`verify_baton_005_gct_perm_det.py`](verification/verify_baton_005_gct_perm_det.py) |
| **Baton #006** | 证明复杂度（Resolution / Cutting Planes / EF） | `blocked_by_barrier` | 机械验证 `PHP` 在 Resolution 下的指数爆炸与 Cutting Planes 多项式反驳（精确 $n^3+3n^2-n+1$ 行，测至 $n=20$） | [`verify_baton_006_proof_complexity.py`](verification/verify_baton_006_proof_complexity.py) |
| **Baton #007** | 单调电路提升 & 非单调抵消墙 | `blocked_by_barrier` | 精确向日葵提取、KW 单调/非单调矩形覆盖对比（10 vs 7）、GPW 512/512 提升，及 Jacobi 求解器验证 Tardos Lovász $\vartheta$ | [`verify_baton_007_monotone_lifting.py`](verification/verify_baton_007_monotone_lifting.py) |
| **Baton #008** | 一般电路门消除法（Gate Elimination） | `pruned` | 证明「对偶距-3 XOR 屏蔽定理」：即便在 $\Theta(n^2)$ 电路上，局部门消除单步也被锁死在 $\le 4$ 门，封死 $O(n)$ 天花板 | [`verify_baton_008_gate_elimination.py`](verification/verify_baton_008_gate_elimination.py) |
| **Baton #009** | Aaronson–Wigderson 代数化壁垒与 Sumcheck | `verified` | 实现 $\mathbb{F}_{101}/\mathbb{F}_{257}$ 精确 MLE 与完整 Sumcheck 协议，构造隐藏稀疏交集的代数预言机碰撞样本 | [`verify_baton_009_algebrization.py`](verification/verify_baton_009_algebrization.py) |
| **Baton #010** | Williams $\text{ACC}^0$ 多项式方法与 $\text{TC}^0$ 墙 | `verified` | 实现快速 Zeta 变换（26.4x 加速）与 Beigel–Tarui 编译，用 Smolensky 下界标定 `MAJ` 门击穿矩形矩阵乘法预算 | [`verify_baton_010_acc0_poly_method.py`](verification/verify_baton_010_acc0_poly_method.py) |
| **Baton #011** | 2026.10 ETH 证伪后的精细复杂度全景审计 | `verified` | 实现 IPZ 3-CNF 稀疏化分支器，验证固定 $k$ SETH 坍塌而无界宽度 `CNF-SAT-SETH` 与自然证明幸存 | [`verify_baton_011_eth_consequences.py`](verification/verify_baton_011_eth_consequences.py) |
| **Baton #012** | **【Wave 3 缝隙 1】$\text{AC}^0[2]\text{-Frege}$ / $\text{Res}(\oplus)$ / $\text{PC}/\mathbb{F}_2$** | `verified` | 算出 $\text{FPHP}_{2,3,4}$ 精确 $\text{PC}/\mathbb{F}_2$ 次数 `[2,3,3]` 及 $n=4$ 动态 PC vs 静态 NS 严格分离（$3<4$）；发现 $\text{Count}_3(7)$ Kneser 分离（$2<3$）并验证 $\text{Count}_3(10)$ 1416 维二次对偶见证与 Frobenius 扩展不变性 | [`verify_baton_012_ac0_mod2_frege.py`](verification/verify_baton_012_ac0_mod2_frege.py) |
| **Baton #013** | **【Wave 3 缝隙 2】GCT 重数障碍全扫描（$N=12..16$ & $N=30$）** | `verified` | 算全 $S_{12},S_{14},S_{15},S_{16}$ 精确特征标表（146 个填充候选全为 0 缺口，量化开轨道边界膨胀 $2.44\times/3.68\times$），并**直接认证出 $N=30$（$d=10,m=3$）的 2 个非平凡 10 次定义方程障碍见证 $\lambda=(13,3,2^7)$ 与 $(12,5,2^6,1)$** | [`verify_baton_013_gct_multiplicity_scan.py`](verification/verify_baton_013_gct_multiplicity_scan.py) |
| **Baton #014** | **【Wave 3 缝隙 3】无界宽度 `CNF-SAT` + Valiant 深度约简桥** | `verified` | 13 个显式 DAG（90/90）验证 Valiant MSB 深度减半与 6/6 电路精确等价；将后 ETH 时代 `CNF-SAT-SETH` 堡垒进一步收窄为**多项式子句数无界宽度**（证明线性子句数无界宽度在 Schuler+IPZ 下同样坍塌至 $2^{o(n)}$） | [`verify_baton_014_valiant_unbounded_cnf.py`](verification/verify_baton_014_valiant_unbounded_cnf.py) |
| **Baton #015** | **【Wave 3 形式化】Lean 4.12 核心库扩展（`ProofComplexityPHP.lean`）** | `verified` | 纯 Lean 4 核心（零 Mathlib、零 `sorry`、零 `Classical.choice`）形式化证明：鸽巢无单射、Cutting Planes 双重求和矛盾 + CG 取整、Valiant 边分桶均值引理，接入 GitHub Actions 真实内核编译 | [`verify_baton_015_lean4_library.py`](verification/verify_baton_015_lean4_library.py) |

### 下一波开放认领的接力棒（Wave 4: Baton #016 – #018）
- **Baton #016 (`baton-016-gct-n30-hwv-eval`)**：在 $\operatorname{perm}_3$ 上显式计算 Baton #013 认证出的两个 $N=30$ 10 次障碍（$(13,3,2^7)$ 与 $(12,5,2^6,1)$）的最高权向量（HWV），检验其是否非零！
- **Baton #017 (`baton-017-res-xor-dag-lifting`)**：针对 Baton #012 定位的 BSW 字面量多样性失效，设计仿射子空间切换引理以将 $\text{PC}/\mathbb{F}_2$ 对偶见证提升至 DAG $\text{Res}(\oplus)$！
- **Baton #018 (`baton-018-poly-clause-unbounded-cnf`)**：针对 Baton #014 精准收窄后的「多项式子句数无界宽度 `CNF-SAT`（$M=n^B$）」堡垒，探索非 IPZ 算法能否跨越 Valiant 的 $\Omega(n/\log\log n)$ 阈值！

---

## 4. 如何接过下一棒？（For Humans & AI Agents）

无论你是人类研究者，还是你把本仓库交给你自己的 AI Agent（Claude Code / Antigravity / Codex / Gemini / 本地模型），只需要 4 步即可接力：

1. **阅读 Agent 上岗手册**：让你的 Agent 先读取 [`AGENT_SKILL.md`](AGENT_SKILL.md)、[`roadmap.json`](roadmap.json) 与各棒 `POSTMORTEM.md`（避免踩已经剪枝的坑）。
2. **认领一个开放节点（Baton）**：在 GitHub Issues 中认领开放任务（如 **Baton #016 / #017 / #018**），或提新 Issue 分解子引理。
3. **本地运行全套确定性门禁测试（自动执行全部 16 套验证脚本 + 20 节点 DAG 校验 + 诚实守门员）**：
   ```bash
   python verification/validate_relay_gate.py
   ```
4. **提交 PR（成功证明 / 分解子引理 / 严格失败验尸，三者皆受认可）**：GitHub Actions 会自动运行 Python 16 套件门禁与 Lean 4.12 内核编译检查，双绿灯后即可合并进入公共接力图谱。

---

## 5. References & Inspiration

- **Choir**: Yidi Qi & Melanie Weber (2026), *Choir: An Open Protocol for Distributed Multi-Agent Autoformalization*, [arXiv:2609.31903](https://arxiv.org/abs/2609.31903)
- **Open Proof Network**: [github.com/thisisanameforsure/open_proof_network](https://github.com/thisisanameforsure/open_proof_network) ("Trust artifacts, not parties" & "Failure pays")
- **PolyProof**: [github.com/polyproof/polyproof](https://github.com/polyproof/polyproof)
- **Terence Tao (2026)**: *New Mathematical Workflows* & *The Equational Theories Project* ([arXiv:2512.07087](https://arxiv.org/abs/2512.07087))
- **Complexity Barriers**: Baker–Gill–Solovay (1975), Razborov–Rudich (1997), Aaronson–Wigderson (2009), Williams (2011/2014), CHOPRS (STOC 2020)
