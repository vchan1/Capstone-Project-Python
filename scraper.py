"""Scrape the first 20 country records from Scrape This Site."""

import requests
from bs4 import BeautifulSoup


SOURCE_URL = "https://www.scrapethissite.com/pages/simple/"
COUNTRY_LIMIT = 20


def scrape_countries(limit=COUNTRY_LIMIT):
    """Return up to `limit` countries as dictionaries with typed values."""
    response = requests.get(
        SOURCE_URL,
        headers={"User-Agent": "CountryCapstoneStudentProject/1.0"},
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    country_cards = soup.select(".country")[:limit]

    if not country_cards:
        raise ValueError("No country records were found; the page layout may have changed.")

    countries = []
    for card in country_cards:
        name_element = card.select_one(".country-name")
        capital_element = card.select_one(".country-capital")
        population_element = card.select_one(".country-population")
        area_element = card.select_one(".country-area")

        if not all((name_element, capital_element, population_element, area_element)):
            raise ValueError("A country record is missing one or more required fields.")

        countries.append(
            {
                "country_name": name_element.get_text(strip=True),
                "capital": capital_element.get_text(strip=True),
                "population": int(population_element.get_text(strip=True)),
                "area": float(area_element.get_text(strip=True)),
            }
        )

    return countries


if __name__ == "__main__":
    for country in scrape_countries():
        print(country)
