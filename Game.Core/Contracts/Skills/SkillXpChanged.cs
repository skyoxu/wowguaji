namespace Game.Core.Contracts.Skills;

/// <summary>
/// Domain event: core.skill.xp.changed
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Gathering.md
/// </remarks>
public sealed record SkillXpChanged(
    string SkillId,
    int XpDelta,
    int NewXp,
    System.DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.skill.xp.changed";
}

