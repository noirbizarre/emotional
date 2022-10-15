# type: ignore
try:
    from functools import cached_property
except ImportError:
    cached_property = property  # noqa: F401

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # noqa: F401
