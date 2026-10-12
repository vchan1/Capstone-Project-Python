# Country Data Pipeline Capstone Presentation Guide

Use this guide to set up the project from its GitHub repository and present the full data pipeline. The project uses a local virtual environment to run Python packages; `.venv` is excluded from GitHub, so each computer creates its own environment after cloning.

## Before presenting

1. Install Python 3.12.
2. Clone the project from GitHub and open its folder in your editor.
3. Open a terminal in the project folder and create a local virtual environment:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

4. Confirm that the terminal prompt begins with `(.venv)`.
5. If `countries.db` is not present, create and fill it by running:

   ```bash
   python seed_database.py
   ```

**Presenter comment:** Explain that GitHub contains the source code and project assets, while `.venv` is made locally because installed packages and environments belong to each computer.

## Start the API

1. In Terminal 1, make sure you are in the project folder and `.venv` is active.
2. Start the FastAPI server:

   ```bash
   uvicorn api:app --reload
   ```

3. Keep this terminal open. It prints the documentation address:

   ```text
   http://127.0.0.1:8000/docs
   ```

4. Open that address in a browser. The page is Swagger UI, where the API routes can be tried interactively.

**Presenter comment:** Say that FastAPI provides a way for other programs to read and change the country data through HTTP endpoints.

## Demonstrate the API

In Swagger UI, expand a route, click **Try it out**, fill in any fields, and click **Execute**.

1. **GET `/countries`** - retrieve every stored country. Expect status `200` and 20 records.
2. **GET `/countries/{country_name}`** - enter `Andorra` and retrieve one country. Expect status `200`.
3. **POST `/countries`** - create a temporary record with this request body. Expect status `201`.

   ```json
   {
     "country_name": "CapstoneTestland",
     "capital": "Sample City",
     "population": 12345,
     "area": 678.9
   }
   ```

4. **GET `/countries/{country_name}`** - enter `CapstoneTestland` to confirm it was created.
5. **PUT `/countries/{country_name}`** - enter `CapstoneTestland` and update it with this body. Expect status `200`.

   ```json
   {
     "capital": "Updated City",
     "population": 13000,
     "area": 700.5
   }
   ```

6. **DELETE `/countries/{country_name}`** - enter `CapstoneTestland` and delete the temporary record. Expect status `200`.
7. Run **GET `/countries`** again. It should return to 20 records.

**Presenter comment:** Point out that the country name is the natural primary key: it identifies each row without a separate numeric ID. The temporary record demonstrates create, read, update, and delete without changing the scraped countries.

## Show the client, CSV, and chart

1. Leave the API server running in Terminal 1.
2. Open Terminal 2 in the project folder and activate the environment:

   ```bash
   source .venv/bin/activate
   ```

3. Run the client:

   ```bash
   python client.py
   ```

4. Show the printed Pandas table.
5. Open `exported_countries.csv` to show the exported country data.
6. Open `population_vs_area.png` to show the scatter plot. The x-axis is population and the y-axis is area in square kilometers.

**Presenter comment:** Explain that the client gets the data from the API, converts it into a Pandas DataFrame, and then produces a reusable CSV and a visualization.

## Finish

1. Confirm the temporary `CapstoneTestland` record was deleted and the API still shows 20 countries.
2. Stop the API with **Control+C** in Terminal 1.

**Closing comment:** Summarize the pipeline in order: scrape the website, store records in SQLite, serve them with FastAPI, retrieve them with the client, and create the CSV and chart.
