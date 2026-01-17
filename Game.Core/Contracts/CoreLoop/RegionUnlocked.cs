namespace Game.Core.Contracts.CoreLoop;

/// <summary>
/// Domain event: core.region.unlocked
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Regions-Map.md
/// </remarks>
public sealed record RegionUnlocked(
    string RegionId,
    string Reason,
    System.DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.region.unlocked";
}
