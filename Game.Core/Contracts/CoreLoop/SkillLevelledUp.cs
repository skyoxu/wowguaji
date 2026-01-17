namespace Game.Core.Contracts.CoreLoop;

/// <summary>
/// Domain event: core.skill.levelled_up
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Gathering.md
/// </remarks>
public sealed record SkillLevelledUp(
    string SkillId,
    int NewLevel,
    System.DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.skill.levelled_up";
}
