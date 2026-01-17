namespace Game.Core.Contracts.Gathering;

/// <summary>
/// Domain event: core.resource.generated
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Gathering.md
/// </remarks>
public sealed record ResourceGenerated(
    string SkillId,
    string NodeId,
    string ResourceItemId,
    int Quantity,
    System.DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.resource.generated";
}

