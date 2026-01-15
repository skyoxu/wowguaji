namespace Game.Core.Contracts.CoreLoop;

/// <summary>
/// Domain event: core.inventory.item.added
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Core-Loop.md
/// </remarks>
public sealed record InventoryItemAdded(
    string ItemId,
    int Quantity,
    string Reason,
    System.DateTimeOffset OccurredAt
)
{
    public const string EventType = "core.inventory.item.added";
}
