"""
Template filters for the flavors app.

Provides display utilities for flavor data, including cleaning legacy
import artifacts from flavor names without modifying database records.
"""

import re
from django import template

register = template.Library()


@register.filter
def clean_flavor_name(value):
    """
    Strip legacy prefixes and artifacts from flavor names.

    Handles common import artifacts like:
    - `*/` prefix (e.g., "*/Strawberry" -> "Strawberry")
    - `+` prefix (e.g., "+Vanilla" -> "Vanilla")
    - `*` prefix with space (e.g., "* Chocolate" -> "Chocolate")
    - Leading/trailing whitespace

    Args:
        value: The flavor name value (string or None)

    Returns:
        str: Cleaned flavor name, or empty string if value is None/empty
    """
    if not value:
        return ""

    name = str(value)

    # Strip leading artifacts: *, /, +, and whitespace
    name = re.sub(r'^[\*\/\+\s]+', '', name)

    # Strip trailing whitespace
    name = name.strip()

    return name
