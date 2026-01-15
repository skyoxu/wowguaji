using FluentAssertions;
using Game.Core.Contracts.Runtime;
using Xunit;

namespace Game.Core.Tests.Contracts.Runtime;

public sealed class RuntimeContractsTests
{
    [Fact]
    public void Runtime_event_type_constants_are_stable()
    {
        GameStarted.EventType.Should().Be("core.game.started");
        GameEnded.EventType.Should().Be("core.game.ended");
        ScoreUpdated.EventType.Should().Be("core.score.updated");
        HealthUpdated.EventType.Should().Be("core.health.updated");
        PlayerMoved.EventType.Should().Be("core.player.moved");
        PlayerDamaged.EventType.Should().Be("core.player.damaged");
    }
}

