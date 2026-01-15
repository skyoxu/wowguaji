namespace Game.Core.Contracts.Gathering;

/// <summary>
/// Domain event: core.gathering.stopped
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Gathering.md
/// </remarks>
public sealed record GatheringStopped(
    string SkillId,
    string NodeId,
    string Reason,
    System.DateTimeOffset StoppedAt
)
{
    public const string EventType = "core.gathering.stopped";
}

