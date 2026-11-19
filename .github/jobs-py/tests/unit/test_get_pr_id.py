from .context import src

from src.get_pr_id import get_pr_id


def test_main_commit():
    assert get_pr_id("7d46c75af91adbfdfc70689f4d8b3405b26bda6b") == 196


def test_feature_commit():
    assert get_pr_id("f30be53c2a5b3d61928c0f41a2e25605a9901d6a") is None


def test_dne_commit():
    assert get_pr_id("f30be53c2a5b3d61928c0f41a2e25605a9901d6b") is None
