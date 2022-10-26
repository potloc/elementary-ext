"""Passthrough shim for elementary extension."""
import sys

import structlog
from meltano.edk.logging import pass_through_logging_config
from elementary_ext.extension import elementary


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = elementary()
    ext.pass_through_invoker(
        structlog.getLogger("elementary_invoker"),
        *sys.argv[1:] if len(sys.argv) > 1 else []
    )
