import pytest
import page_loader.page_loader as page_loager


def test_echo():
    assert page_loager.echo(5) == 5
