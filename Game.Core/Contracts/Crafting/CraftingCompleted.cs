namespace Game.Core.Contracts.Crafting;

/// <summary>
/// Domain event: core.crafting.completed
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Crafting.md
/// </remarks>
public sealed record CraftingCompleted(
    string RecipeId,
    string OutputItemId,
    int OutputQuantity,
    System.DateTimeOffset CompletedAt
)
{
    public const string EventType = "core.crafting.completed";
}

