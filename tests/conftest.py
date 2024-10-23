"""Configuration for the tests."""

import pytest
from syrupy import SnapshotAssertion

from .syrupy import CustomSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the custom extension."""
    return snapshot.use_extension(CustomSnapshotExtension)
