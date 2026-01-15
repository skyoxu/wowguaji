using FluentAssertions;
using Game.Core.Contracts.Save;
using Xunit;

namespace Game.Core.Tests.Contracts.Save;

public sealed class SaveContractsTests
{
    [Fact]
    public void Save_event_type_constants_are_stable()
    {
        SaveCreated.EventType.Should().Be("core.save.created");
        SaveLoaded.EventType.Should().Be("core.save.loaded");
        SaveDeleted.EventType.Should().Be("core.save.deleted");
        AutoSaveEnabled.EventType.Should().Be("core.autosave.enabled");
        AutoSaveDisabled.EventType.Should().Be("core.autosave.disabled");
        AutoSaveCompleted.EventType.Should().Be("core.autosave.completed");
    }
}

