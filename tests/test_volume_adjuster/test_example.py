import pytest

from src.volume_adjuster.type_checker import TypeChecker


class TesTypeChecker:
    @pytest.mark.type_checker
    @pytest.fixture
    def test_normal_init(
        self,
    ):
        pass
