from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def jpy(value):
    """Format a whole-yen value with the yen symbol and digit grouping."""
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value
    return f"¥{amount:,.0f}"


@register.filter
def duration_hm(value):
    """Format a duration as compact hours and minutes."""
    if not isinstance(value, timedelta):
        return value
    total_minutes = max(0, int(value.total_seconds() // 60))
    hours, minutes = divmod(total_minutes, 60)
    if hours and minutes:
        return f"{hours}h {minutes}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"
