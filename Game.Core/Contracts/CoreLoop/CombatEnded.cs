namespace Game.Core.Contracts.CoreLoop;

/// <summary>
/// Domain event: core.combat.ended
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Combat.md
/// </remarks>
public sealed record CombatEnded(
    string EncounterId,
    bool PlayerWon,
    int GoldDelta,
    string[] ItemIds,
    System.DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.combat.ended";
}
