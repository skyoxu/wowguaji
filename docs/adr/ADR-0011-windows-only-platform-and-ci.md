---
ADR-ID: ADR-0011
title: 平台与 CI 策略（Windows-only）
status: Accepted
decision-time: '2025-09-10'
deciders: [架构团队, DevOps团队]
archRefs: [CH01, CH03, CH07, CH09, CH10]
depends-on: [ADR-0005, ADR-0008]
supersedes: [ADR-0009]
impact-scope:
  - .github/workflows/
  - scripts/ci/**
  - scripts/release/**
  - build/**
verification:
  - path: scripts/ci/lint_workflows.ps1
    assert: 校验 workflows 基本结构；所有 Job 使用 windows-latest；禁止 shell 非 pwsh
  - path: .github/workflows/windows-quality-gate.yml
    assert: 质量门禁 Job 在 windows-latest 上运行，所有 run 步骤显式 shell: pwsh
  - path: .github/workflows/windows-release.yml
    assert: 发布 Job 在 windows-latest 上运行，且无 bash/跨平台 runner
monitoring-metrics:
  - ci_compliance_rate
  - gate_pass_rate
---

# ADR-0011: 平台与 CI 策略（Windows-only）

## Context

项目仅支持 Windows 平台。为降低脚本语法分歧与运行器差异带来的失败率，统一 CI 运行环境与 Shell 策略，简化发布/回滚链路；同步废止跨平台策略（ADR-0009）。

## Decision

- 平台范围：Windows-only（运行时与分发）；跨平台目标废止。
- CI 运行器：默认 `runs-on: windows-latest`。
- Shell 策略：所有 `run:` 步骤显式 `shell: pwsh`（或使用 Job 级 `defaults.run.shell: pwsh`）；禁止使用 `shell: bash` 等非 pwsh shell。
- 控制流：通知与旁路步骤使用步骤级 `if:` 与必要的 `continue-on-error`，替代脚本内判空。
- 守卫：`scripts/ci/lint_workflows.ps1` 作为基础静态检查，禁止非 Windows runner 与非 pwsh shell；质量门禁脚本负责把输出落盘到 `logs/ci/<YYYY-MM-DD>/`。
- 日志：所有 CI/脚本输出写入 `logs/**`（SSoT 见 `docs/architecture/base/03-observability-sentry-logging-v2.md` 与 `AGENTS.md` 6.3）以便取证与审计。

## Consequences

- 优点：统一语法/环境，降低 CI 失败率与脚本歧义；发布与回滚路径收敛。
- 代价：不再验证 macOS/Linux；未来若恢复跨平台，需要撤销本 ADR 并恢复 OS 矩阵。

## Alternatives

- 继续维持多 OS 矩阵（与 Windows-only 目标冲突）。
- 在 Windows runner 上默认使用 Bash（与团队 PowerShell 技栈与系统工具链冲突）。

## Compliance Checklist

- [ ] 所有 Job `runs-on: windows-latest`。
- [ ] 所有 `run:` 步骤显式 `shell: pwsh`（或 Job 级 `defaults.run.shell: pwsh`）。
- [ ] 不存在 `shell: bash` / 其他 shell。
- [ ] 回滚与通知步骤：使用 `if:` 判空；失败不拖垮主流程（必要时 `continue-on-error`）。
- [ ] `scripts/ci/lint_workflows.ps1` 校验通过，并纳入分支保护（如有）。
