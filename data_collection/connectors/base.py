from typing import Protocol
from collections.abc import Iterator

from data_collection.contracts import RawJobPosting


class JobSourceConnector(Protocol):
    """Common interface for future job source connectors."""

    source_name: str

    def fetch(self) -> list[RawJobPosting]:
        """Return raw job postings from a source."""

    def iter_fetch(self, limit: int | None = None) -> Iterator[RawJobPosting]:
        """Stream raw job postings from a source."""
