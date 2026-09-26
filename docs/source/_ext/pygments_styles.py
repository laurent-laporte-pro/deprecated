"""Pygments styles of the documentation, tuned for readability.

The Lovelace (light mode) and Gruvbox dark (dark mode) styles are kept as is, except for
the few colors whose contrast with the background is below the WCAG AA level (4.5:1):
these colors are replaced by the same hue, darkened (light mode) or lightened (dark mode).
"""

from pygments.style import Style
from pygments.styles.gruvbox import GruvboxDarkStyle
from pygments.styles.lovelace import LovelaceStyle


def _replace_colors(style: type[Style], colors: dict[str, str]) -> dict:
    """Return the token styles of *style*, with the *colors* replaced."""
    styles = {}
    for token, definition in style.styles.items():
        for old, new in colors.items():
            definition = definition.replace(old, new)
        styles[token] = definition
    return styles


class ReadableLovelaceStyle(LovelaceStyle):
    """Lovelace, on the light gray of Furo, with darker colors (4.5:1 or more)."""

    name = "readable-lovelace"
    # Light gray background (Furo's secondary background) to set the code blocks apart
    # from the white page.
    background_color = "#f8f9fb"
    styles = _replace_colors(
        LovelaceStyle,
        {
            "#888888": "#6e6e6e",  # comments, punctuation
            "#289870": "#217c5b",  # namespaces (imported modules)
            "#709030": "#5d7728",  # string escapes, entities
            "#908828": "#766f21",  # exceptions (e.g. DeprecationWarning), global variables
            "#b85820": "#af541e",  # docstrings, constants
        },
    )


class ReadableGruvboxDarkStyle(GruvboxDarkStyle):
    """Gruvbox dark, with lighter reds and grays (4.5:1 or more on #282828)."""

    name = "readable-gruvbox-dark"
    styles = _replace_colors(
        GruvboxDarkStyle,
        {
            "#fb4934": "#fb5f4d",  # keywords, decorators
            "#928374": "#9e9184",  # comments
        },
    )
