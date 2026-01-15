namespace Game.Core.Contracts.Combat;

/// <summary>
/// Domain event: core.combat.started
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Combat.md
/// </remarks>
public sealed record CombatStarted(
    string EncounterId,
    string RegionId,
    string EnemyId,
    System.DateTimeOffset StartedAt
)
{
    public const string EventType = "core.combat.started";
}

