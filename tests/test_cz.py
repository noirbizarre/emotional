from emotional.cz import CzEmotional


def test_example(config):
    """just testing a string is returned. not the content"""
    emotional_config = CzEmotional(config)
    example = emotional_config.example()
    assert isinstance(example, str)


def test_schema(config):
    """just testing a string is returned. not the content"""
    emotional_config = CzEmotional(config)
    schema = emotional_config.schema()
    assert isinstance(schema, str)


def test_info(config):
    """just testing a string is returned. not the content"""
    emotional_config = CzEmotional(config)
    info = emotional_config.info()
    assert isinstance(info, str)
