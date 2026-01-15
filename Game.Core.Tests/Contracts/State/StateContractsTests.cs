using FluentAssertions;
using Game.Core.Contracts.State;
using Xunit;

namespace Game.Core.Tests.Contracts.State;

public sealed class StateContractsTests
{
    [Fact]
    public void State_event_type_constants_are_stable()
    {
        StateManagerUpdated.EventType.Should().Be("core.state.manager.updated");
    }
}

