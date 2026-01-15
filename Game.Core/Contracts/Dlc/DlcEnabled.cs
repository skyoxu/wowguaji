namespace Game.Core.Contracts.Dlc;

/// <summary>
/// Domain event: core.dlc.enabled
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-DLC.md
/// </remarks>
public sealed record DlcEnabled(
    string DlcId,
    System.DateTimeOffset EnabledAt
)
{
    public const string EventType = "core.dlc.enabled";
}

