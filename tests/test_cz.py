import pytest

from cz_shiny.cz import CzShiny


def test_example(config):
    """just testing a string is returned. not the content"""
    shiny = CzShiny(config)
    example = shiny.example()
    assert isinstance(example, str)


def test_schema(config):
    """just testing a string is returned. not the content"""
    shiny = CzShiny(config)
    schema = shiny.schema()
    assert isinstance(schema, str)


def test_info(config):
    """just testing a string is returned. not the content"""
    shiny = CzShiny(config)
    info = shiny.info()
    assert isinstance(info, str)
