"""Fetch API data, display it as a table, and save CSV and chart outputs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/countries"
PROJECT_FOLDER = Path(__file__).resolve().parent


def fetch_countries():
    """Fetch all countries from the running FastAPI service."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise SystemExit(
            "Could not connect to the API. Start it in another terminal with: "
            "uvicorn api:app --reload"
        ) from error
    except requests.exceptions.Timeout as error:
        raise SystemExit("The API took too long to respond. Please try again.") from error
    except requests.exceptions.HTTPError as error:
        raise SystemExit(f"The API returned an error: {error}") from error

    countries = response.json()
    if not countries:
        raise SystemExit("The API returned no countries. Seed the database first.")
    return countries


def main():
    countries = fetch_countries()
    dataframe = pd.DataFrame.from_records(countries)

    print("Countries received from the API:")
    print(dataframe.to_string(index=False))

    csv_path = PROJECT_FOLDER / "exported_countries.csv"
    dataframe.to_csv(csv_path, index=False)
    print(f"\nCSV saved to: {csv_path}")

    chart_path = PROJECT_FOLDER / "population_vs_area.png"
    plt.figure(figsize=(10, 6))
    plt.scatter(
        dataframe["population"],
        dataframe["area"],
        color="royalblue",
        alpha=0.8,
        edgecolors="white",
        linewidths=0.6,
    )
    plt.title("Country Population vs. Area")
    plt.xlabel("Population")
    plt.ylabel("Area (sq. km)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Scatter plot saved to: {chart_path}")


if __name__ == "__main__":
    main()
