using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Save;

/// <summary>
/// Domain event: core.save.deleted
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Save-Offline.md
/// </remarks>
public sealed record SaveDeleted(
    [property: JsonPropertyName("saveId")] string SaveId,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.save.deleted";
}

