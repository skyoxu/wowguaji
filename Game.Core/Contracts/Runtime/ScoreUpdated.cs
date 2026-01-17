using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Runtime;

/// <summary>
/// Domain event: core.score.updated
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-UI-Dashboard.md
/// </remarks>
public sealed record ScoreUpdated(
    [property: JsonPropertyName("score")] int Score,
    [property: JsonPropertyName("added")] int Added,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.score.updated";
}

