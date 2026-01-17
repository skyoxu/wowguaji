using FluentAssertions;
using Game.Core.Contracts.Combat;
using Game.Core.Contracts.Crafting;
using Game.Core.Contracts.Dlc;
using Game.Core.Contracts.Gathering;
using Game.Core.Contracts.Skills;
using Xunit;

namespace Game.Core.Tests.Contracts.Gameplay;

public sealed class GameplayContractsTests
{
    [Fact]
    public void Event_type_constants_are_stable()
    {
        CombatStarted.EventType.Should().Be("core.combat.started");
        LootDropped.EventType.Should().Be("core.loot.dropped");

        CraftingCompleted.EventType.Should().Be("core.crafting.completed");
        RecipeUnlocked.EventType.Should().Be("core.recipe.unlocked");
        EquipmentEquipped.EventType.Should().Be("core.equipment.equipped");

        DlcEnabled.EventType.Should().Be("core.dlc.enabled");

        GatheringStarted.EventType.Should().Be("core.gathering.started");
        GatheringStopped.EventType.Should().Be("core.gathering.stopped");
        ResourceGenerated.EventType.Should().Be("core.resource.generated");

        SkillXpChanged.EventType.Should().Be("core.skill.xp.changed");
    }
}

