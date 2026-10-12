"""FastAPI service for the country database."""

from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from database import CountryDatabaseManager


DATABASE_PATH = Path(__file__).resolve().with_name("countries.db")
database = CountryDatabaseManager(DATABASE_PATH)


@asynccontextmanager
async def lifespan(_app):
    print(
        """
Country Data API is ready!
Documentation: http://127.0.0.1:8000/docs

PRESENTATION DEMO (open the link above):
1. GET /countries -> Try it out -> Execute. Expect 200 and 20 countries.
2. GET /countries/{country_name} -> Try it out -> enter Andorra -> Execute.
3. POST /countries -> Try it out -> paste this JSON -> Execute (expect 201):
   {
     "country_name": "Demo Country",
     "capital": "Example City",
     "population": 1000,
     "area": 25.5
   }
4. GET /countries/{country_name} -> enter Demo Country -> Execute (expect 200).
5. PUT /countries/{country_name} -> enter Demo Country, then use this JSON:
   {
     "capital": "New Example City",
     "population": 1200,
     "area": 30.0
   }
   Click Execute (expect 200).
6. DELETE /countries/{country_name} -> enter Demo Country -> Execute (expect 200).
   The demo country is removed, leaving the original 20 countries.
"""
    )
    yield


app = FastAPI(title="Country Data API", version="1.0.0", lifespan=lifespan)


class CountryCreate(BaseModel):
    country_name: str = Field(min_length=1)
    capital: str = Field(min_length=1)
    population: int = Field(ge=0)
    area: float = Field(ge=0)


class CountryUpdate(BaseModel):
    capital: str = Field(min_length=1)
    population: int = Field(ge=0)
    area: float = Field(ge=0)


class CountryResponse(CountryCreate):
    pass


@app.get("/countries", response_model=list[CountryResponse])
def get_countries():
    """Return every country in the database."""
    return database.get_all_countries()


@app.get("/countries/{country_name}", response_model=CountryResponse)
def get_country(country_name: str):
    """Return one country selected by its name."""
    country = database.get_country_by_name(country_name)
    if country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country '{country_name}' was not found.",
        )
    return country


@app.post("/countries", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
def create_country(country: CountryCreate):
    """Add a country to the database."""
    try:
        database.create_country(
            country_name=country.country_name,
            capital=country.capital,
            population=country.population,
            area=country.area,
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Country '{country.country_name}' already exists.",
        ) from None

    return database.get_country_by_name(country.country_name)


@app.put("/countries/{country_name}", response_model=CountryResponse)
def update_country(country_name: str, country: CountryUpdate):
    """Update the details for a country selected by its name."""
    updated = database.update_country(
        country_name=country_name,
        capital=country.capital,
        population=country.population,
        area=country.area,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country '{country_name}' was not found.",
        )

    return database.get_country_by_name(country_name)


@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    """Delete a country selected by its name."""
    deleted = database.delete_country(country_name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country '{country_name}' was not found.",
        )

    return {"message": f"Country '{country_name}' was deleted."}
