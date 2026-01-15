namespace Game.Core.Contracts.Combat;

/// <summary>
/// Domain event: core.loot.dropped
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Combat.md
/// </remarks>
public sealed record LootDropped(
    string EncounterId,
    string RegionId,
    int GoldDelta,
    string[] ItemIds,
    System.DateTimeOffset DroppedAt
)
{
    public const string EventType = "core.loot.dropped";
}

