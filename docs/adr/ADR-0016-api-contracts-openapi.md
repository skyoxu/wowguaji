# ADR-0016：API 契约与 OpenAPI 基线（不适用）

- 状态：Deferred
- 背景：wowguaji 是 Godot 4.5 + C#/.NET 8（Windows-only）游戏模板，当前不提供对外 HTTP API，也不维护 OpenAPI 相关文件与 CI 作业。
- 决策：
  - 本仓库不引入 OpenAPI 作为契约 SSOT。
  - 若未来确需对外 HTTP API（例如独立后端服务），应在对应服务仓库内落地 OpenAPI，并新增 ADR 记录其边界、版本策略、发布与门禁。
- 参考：ADR-0004（事件总线与契约）、ADR-0005（质量门禁）
