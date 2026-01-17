using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Runtime;

/// <summary>
/// Domain event: core.player.damaged
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Combat.md
/// </remarks>
public sealed record PlayerDamaged(
    [property: JsonPropertyName("amount")] int Amount,
    [property: JsonPropertyName("type")] string DamageType,
    [property: JsonPropertyName("critical")] bool Critical,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.player.damaged";
}

