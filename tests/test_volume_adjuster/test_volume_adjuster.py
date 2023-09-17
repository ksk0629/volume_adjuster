import pytest

from src.volume_adjuster.volume_adjuster import VolumeAdjuster


class TestVolumeAdjuster:
    @pytest.mark.volume_adjuster
    @pytest.fixture
    def test_normal_init(self):
        pass
