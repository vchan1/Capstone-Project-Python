"""Scrape the first 20 countries and insert any that are not stored yet."""

from database import CountryDatabaseManager
from scraper import scrape_countries


def seed_database():
    database = CountryDatabaseManager()
    countries = scrape_countries()
    inserted = 0

    for country in countries:
        existing_country = database.get_country_by_name(country["country_name"])
        if existing_country is None:
            database.create_country(
                country_name=country["country_name"],
                capital=country["capital"],
                population=country["population"],
                area=country["area"],
            )
            inserted += 1

    print(f"Scraped {len(countries)} countries.")
    print(f"Inserted {inserted} new countries into countries.db.")
    print(f"The database now contains {len(database.get_all_countries())} countries.")


if __name__ == "__main__":
    seed_database()
