namespace Game.Core.Contracts.Crafting;

/// <summary>
/// Domain event: core.equipment.equipped
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Crafting.md
/// </remarks>
public sealed record EquipmentEquipped(
    string Slot,
    string ItemId,
    System.DateTimeOffset EquippedAt
)
{
    public const string EventType = "core.equipment.equipped";
}

