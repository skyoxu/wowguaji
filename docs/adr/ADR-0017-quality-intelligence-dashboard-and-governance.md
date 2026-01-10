# ADR-0017: Quality Intelligence Dashboard and Governance (Not In Scope)

- Status: Deferred
- Context: wowguaji focuses on Godot+C# game runtime quality gates and auditable artifacts under `logs/**`.
- Decision:
  - Do not introduce a separate "quality intelligence dashboard" system in this repo.
  - Keep using existing quality gates and artifacts produced by the current scripts (typecheck/lint/unit/scene/security/perf).
  - If a future project requires cross-repo quality aggregation, define it as a separate component and record it in a dedicated ADR.
- References: ADR-0005 (Quality Gates), ADR-0015 (Performance Budgets), ADR-0003 (Observability)
