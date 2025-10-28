from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter
def format_amount(value, decimals=2):
    """Format a numeric value with commas and a fixed number of decimals.

    Usage in templates:
        {{ value|format_amount }}          -> 1,234.56
        {{ value|format_amount:0 }}        -> 1,234
    The filter is resilient to None and non-numeric input (returns input unchanged).
    """
    if value is None:
        return ""
    try:
        # decimals may come in as a string from the template filter arg
        decimals = int(decimals)
    except (TypeError, ValueError):
        decimals = 2

    try:
        d = Decimal(value)
    except (TypeError, InvalidOperation):
        return value

    fmt = f"{{:,.{decimals}f}}"
    return fmt.format(d)
