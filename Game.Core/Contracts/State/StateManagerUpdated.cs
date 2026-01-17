using System;
using System.Text.Json.Serialization;

namespace Game.Core.Contracts.State;

/// <summary>
/// Domain event: core.state.manager.updated
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Core-Loop.md
/// </remarks>
public sealed record StateManagerUpdated(
    [property: JsonPropertyName("occurredAt")] DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.state.manager.updated";
}

