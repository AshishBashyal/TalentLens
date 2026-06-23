from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def open_connection(database_url: str) -> Iterator[object]:
    """Open a PostgreSQL connection.

    psycopg is imported lazily so scripts that only preview transformations do not
    require the database dependency at import time.
    """

    import psycopg

    connection = psycopg.connect(database_url)
    try:
        yield connection
    finally:
        connection.close()

