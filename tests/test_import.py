import pytest


@pytest.mark.parametrize(
    "mod",
    [
        "async_selector_thread",
        "async_selector_thread.selector_thread",
    ],
)
def test_import(mod):
    __import__(mod)
