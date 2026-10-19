import pytest

from app.sources.manager import SourceManager


class FakeSource:
    """Stands in for a video or camera source; records whether it was released."""

    def __init__(self) -> None:
        self.released = False

    def release(self) -> None:
        self.released = True


class OtherFakeSource(FakeSource):
    pass


def test_switch_releases_previous_source() -> None:
    manager = SourceManager()
    first, second = FakeSource(), FakeSource()

    manager.switch(first)
    manager.switch(second)

    assert first.released
    assert not second.released
    assert manager.active is second


def test_close_releases_and_clears_active_source() -> None:
    manager = SourceManager()
    source = FakeSource()
    manager.switch(source)

    manager.close()

    assert source.released
    assert manager.active is None


def test_require_returns_source_of_requested_type() -> None:
    manager = SourceManager()
    source = FakeSource()
    manager.switch(source)

    assert manager.require(FakeSource) is source


def test_require_wrong_type_raises() -> None:
    manager = SourceManager()
    manager.switch(FakeSource())

    with pytest.raises(LookupError):
        manager.require(OtherFakeSource)
