namespace Game.Core.Contracts.Gathering;

/// <summary>
/// Domain event: core.gathering.started
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Gathering.md
/// </remarks>
public sealed record GatheringStarted(
    string SkillId,
    string NodeId,
    System.DateTimeOffset StartedAt
)
{
    public const string EventType = "core.gathering.started";
}

