using FluentAssertions;
using Game.Core.Contracts.CoreLoop;
using Xunit;

namespace Game.Core.Tests.Contracts.CoreLoop;

public sealed class CoreLoopContractsTests
{
    [Fact]
    public void Event_type_constants_are_stable()
    {
        InventoryItemAdded.EventType.Should().Be("core.inventory.item.added");
        SkillLevelledUp.EventType.Should().Be("core.skill.levelled_up");
        RegionUnlocked.EventType.Should().Be("core.region.unlocked");
        CombatEnded.EventType.Should().Be("core.combat.ended");
        OfflineRewardsGranted.EventType.Should().Be("core.offline.rewards.granted");
    }
}

