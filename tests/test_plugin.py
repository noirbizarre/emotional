from commitizen.factory import committer_factory

from emotional.plugin import Emotional


def test_registered(config):
    committer = committer_factory(config)
    assert isinstance(committer, Emotional)


def test_example(config):
    """just testing a string is returned. not the content"""
    emotional_config = Emotional(config)
    example = emotional_config.example()
    assert isinstance(example, str)


def test_schema(config):
    """just testing a string is returned. not the content"""
    emotional_config = Emotional(config)
    schema = emotional_config.schema()
    assert isinstance(schema, str)


def test_info(config):
    """just testing a string is returned. not the content"""
    emotional_config = Emotional(config)
    info = emotional_config.info()
    assert isinstance(info, str)
