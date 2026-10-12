# Country Data Pipeline Capstone

This project follows the supplied capstone brief. It will collect the first 20
country records from Scrape This Site, store them in SQLite, expose CRUD routes
through FastAPI, and use a client to export a CSV and create a scatter plot.

See [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) for setup-from-GitHub and a
step-by-step presentation walkthrough with presenter comments. The `.venv`
folder is local and ignored by Git; create a new environment after cloning.

## Project roadmap

1. **Setup and scrape** - create a virtual environment and collect 20 typed records.
2. **SQLite and OOP** - create `countries.db` and a `CountryDatabaseManager` with
   create, read, update, and delete methods. Country name is the primary key.
3. **FastAPI** - add the five required `/countries` endpoints.
4. **Client and CSV** - request the API data, display a Pandas DataFrame, and save
   `exported_countries.csv`.
5. **Visualization and integration** - save `population_vs_area.png` with
   population on the x-axis and area on the y-axis.

## Phase 1: setup and scraper

Install Python 3.12 from the official [Python macOS downloads page](https://www.python.org/downloads/macos/) if it is not already installed. Then open a terminal in this project folder and run these commands one at a time:

```bash
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests beautifulsoup4
python scraper.py
```

The first command should report Python 3.12.x. After activating the
environment, your terminal prompt normally shows `(.venv)`. The scraper should
print 20 dictionaries. Each dictionary has a country name, capital, integer
population, and numeric area. The site lists Antarctica with capital text
`None`; this first version preserves the source text exactly.

To leave the virtual environment later, run:

```bash
deactivate
```

## Phase 2: save countries in SQLite

Make sure the `(.venv)` label is visible in your terminal, then run:

```bash
python seed_database.py
```

This creates `countries.db`, creates its `countries` table if needed, and saves
any of the first 20 scraped countries that are not already present. The country
name is the primary key, so it uniquely identifies a row. Run the command again
to refresh the scrape; it will skip country names already in the database.

The CRUD methods are in `database.py`:

- `create_country(...)` inserts a country.
- `get_all_countries()` reads all countries.
- `get_country_by_name(name)` reads one country.
- `update_country(...)` changes a country's capital, population, and area.
- `delete_country(name)` removes a country.

## Phase 3: run the FastAPI service

Install the API packages in the active virtual environment:

```bash
python -m pip install fastapi uvicorn
```

Start the service from the project folder:

```bash
uvicorn api:app --reload
```

Keep this terminal open while the service runs. Open `http://127.0.0.1:8000/docs`
in your browser to try all five routes. The `GET /countries` route should show
the 20 saved records. Use `GET /countries/Andorra` to look up one record. Stop
the service with Control+C in the terminal when you are done.

When the service starts, the terminal also prints the Swagger documentation
address so it is easy to find during a presentation.

The API code is in `api.py`. It validates incoming numbers as non-negative,
returns 404 when a requested country does not exist, and returns 409 if a POST
tries to insert a duplicate country name.

## Phase 4 and 5: client, CSV, and scatter plot

Leave the API running in its first terminal. Open a second terminal in the
project folder, activate the same virtual environment, and install the client
and chart packages:

```bash
source .venv/bin/activate
python -m pip install pandas matplotlib
python client.py
```

`client.py` reads `GET /countries`, prints all returned records as a Pandas
table, writes `exported_countries.csv` without an extra index column, and saves
`population_vs_area.png` with population on the x-axis and area on the y-axis.
Both output files are saved in this project folder. The API must be running
before you start the client.

The complete list of packages needed across all phases is in `requirements.txt`.
For a concise presentation checklist with presenter comments, see
[`PRESENTATION_GUIDE.md`](PRESENTATION_GUIDE.md).
