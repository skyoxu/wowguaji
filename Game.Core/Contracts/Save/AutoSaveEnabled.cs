using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.Save;

/// <summary>
/// Domain event: core.autosave.enabled
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Save-Offline.md
/// </remarks>
public sealed record AutoSaveEnabled(
    [property: JsonPropertyName("intervalMs")] double IntervalMs,
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.autosave.enabled";
}

