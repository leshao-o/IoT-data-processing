import pytest
from app.config import settings

def test_settings_mode_is_test():
    assert settings.MODE == "TEST"
