# type: ignore
try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias  # noqa: F401

try:
    from functools import cached_property
except ImportError:
    cached_property: TypeAlias = property  # noqa: F401

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # noqa: F401
