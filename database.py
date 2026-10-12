"""SQLite storage for country records."""

import sqlite3
from contextlib import contextmanager


class CountryDatabaseManager:
    """Create the country table and provide its CRUD operations."""

    def __init__(self, database_path="countries.db"):
        self.database_path = database_path
        self._create_table()

    @contextmanager
    def _connection(self):
        """Open a connection, commit on success, and always close it."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _create_table(self):
        """Create the table once, using the country name as its primary key."""
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS countries (
                    country_name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL,
                    area REAL NOT NULL
                )
                """
            )

    @staticmethod
    def _row_to_dict(row):
        return dict(row) if row is not None else None

    def create_country(self, country_name, capital, population, area):
        """Insert one country. A duplicate country name raises an error."""
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
                """,
                (country_name, capital, population, area),
            )

    def get_all_countries(self):
        """Return all countries ordered by name."""
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT country_name, capital, population, area
                FROM countries
                ORDER BY country_name
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def get_country_by_name(self, country_name):
        """Return one country, or None if the name is not in the table."""
        with self._connection() as connection:
            row = connection.execute(
                """
                SELECT country_name, capital, population, area
                FROM countries
                WHERE country_name = ?
                """,
                (country_name,),
            ).fetchone()
        return self._row_to_dict(row)

    def update_country(self, country_name, capital, population, area):
        """Update a country's details; return True if a row was found."""
        with self._connection() as connection:
            cursor = connection.execute(
                """
                UPDATE countries
                SET capital = ?, population = ?, area = ?
                WHERE country_name = ?
                """,
                (capital, population, area, country_name),
            )
        return cursor.rowcount > 0

    def delete_country(self, country_name):
        """Delete a country; return True if a row was found."""
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM countries WHERE country_name = ?",
                (country_name,),
            )
        return cursor.rowcount > 0
