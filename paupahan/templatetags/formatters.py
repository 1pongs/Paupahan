"""
DEPRECATED shim module.

This file used to contain the `format_amount` filter at the project level. The
canonical implementation now lives in `paupahan.tenants.templatetags.formatters`.

Keeping this placeholder avoids accidental imports from the old location.
"""

raise ImportError(
    "Deprecated: use paupahan.tenants.templatetags.formatters instead of the project-level formatters"
)
