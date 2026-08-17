"""Domain models and value objects with pure business logic."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExampleEntity:
    """Example domain entity with business invariants and no framework dependencies."""

    id: str
    name: str
    description: Optional[str] = None
