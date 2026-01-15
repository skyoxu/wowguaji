namespace Game.Core.Contracts.CoreLoop;

/// <summary>
/// Domain event: core.offline.rewards.granted
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Save-Offline.md
/// </remarks>
public sealed record OfflineRewardsGranted(
    int OfflineSeconds,
    System.DateTimeOffset LastOnlineTime,
    System.DateTimeOffset SettledAt
)
{
    public const string EventType = "core.offline.rewards.granted";
}
