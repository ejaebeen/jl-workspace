"""Tracing, logging, and metrics setup for MLflow and OpenTelemetry."""

import logging
import sys


def configure_observability() -> None:
    """Configures OpenTelemetry instrumentation and MLflow tracking."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str = "app") -> logging.Logger:
    """Returns a configured logger instance."""
    return logging.getLogger(name)
