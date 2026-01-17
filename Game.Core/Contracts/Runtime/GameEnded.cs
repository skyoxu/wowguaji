using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Runtime;

/// <summary>
/// Domain event: core.game.ended
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Core-Loop.md
/// </remarks>
public sealed record GameEnded(
    [property: JsonPropertyName("score")] int Score,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.game.ended";
}

