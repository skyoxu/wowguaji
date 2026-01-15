namespace Game.Core.Contracts.Crafting;

/// <summary>
/// Domain event: core.recipe.unlocked
/// </summary>
/// <remarks>
/// ADR: ADR-0004 (event naming and contracts).
/// Overlay: docs/architecture/overlays/PRD-WOWGUAJI-T2/08/08-Feature-Slice-Crafting.md
/// </remarks>
public sealed record RecipeUnlocked(
    string RecipeId,
    string SkillId,
    int SkillLevel,
    System.DateTimeOffset UnlockedAt
)
{
    public const string EventType = "core.recipe.unlocked";
}

