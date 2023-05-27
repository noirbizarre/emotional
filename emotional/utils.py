from __future__ import annotations

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader


def render_template(name: str, **kwargs) -> str:
    """
    Render a Jinja template
    """
    loader = ChoiceLoader(
        [
            FileSystemLoader("."),
            PackageLoader("emotional", "templates"),
        ]
    )
    env = Environment(loader=loader, trim_blocks=True)
    jinja_template = env.get_template(name)
    return jinja_template.render(**kwargs)
