import pytest
from src.config import Config, Framework, Repository

def test_config_creation():
    repository = Repository("test-repo", "https://example.com")
    framework = Framework.PYTEST
    config = Config([repository], framework)
    assert config.repositories == [repository]
    assert config.framework == framework

def test_config_creation_invalid_repositories():
    with pytest.raises(ValueError):
        Config([], Framework.PYTEST)

def test_config_creation_invalid_framework():
    with pytest.raises(ValueError):
        Config([Repository("test-repo", "https://example.com")], None)
