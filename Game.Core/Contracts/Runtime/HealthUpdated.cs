using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Runtime;

/// <summary>
/// Domain event: core.health.updated
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-UI-Dashboard.md
/// </remarks>
public sealed record HealthUpdated(
    [property: JsonPropertyName("health")] int Health,
    [property: JsonPropertyName("delta")] int Delta,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.health.updated";
}

