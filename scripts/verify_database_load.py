import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def print_section(title: str, values: dict[str, int]) -> None:
    print(title)
    for name, count in values.items():
        print(f"- {name}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify TalentLens PostgreSQL load counts.")
    parser.parse_args()

    from api.config import get_settings
    from database.connection import open_connection
    from database.verification import verify_database_counts, verify_database_quality

    settings = get_settings()
    with open_connection(settings.database_url) as connection:
        counts = verify_database_counts(connection)
        quality = verify_database_quality(connection)

    print_section("Table counts:", counts)
    print_section("Quality checks:", quality)


if __name__ == "__main__":
    main()

