using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Runtime;

/// <summary>
/// Domain event: core.player.moved
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-UI-Dashboard.md
/// </remarks>
public sealed record PlayerMoved(
    [property: JsonPropertyName("x")] double X,
    [property: JsonPropertyName("y")] double Y,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.player.moved";
}

