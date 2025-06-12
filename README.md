## To Start the App

### With Docker
1. Run the following command:
    ```bash
    docker compose up
    ```
2. Open your browser and go to [http://localhost:5137]

### Without Docker

#### Start the Front End
1. Run the following command in the hackable_vue directory:
    ```bash
    npm run dev
    ```

#### Start the Backend
1. Navigate to the `hackable_api` directory:
    ```bash
    cd hackable_api
    ```
2. Install Poetry if you don't have it:
    ```bash
    pip install poetry
    ```
3. Install dependencies:
    ```bash
    poetry install
    ```
4. Run the app:
    ```bash
    poetry run python -m app.app.run_app
    ```
5. Open your browser and go to [http://localhost:5137]

To run API unit or integration tests:

In poetry
execute the following command from the `hackable_api` directory (integration tests will only work with a docker db container up)

```bash
poetry run pytest app/tests/unit
```
```bash
poetry run pytest app/tests/integration
```

In Docker
execute the following command from the `hackable` directory

```bash
docker compose run --rm backend poetry run pytest app/tests/unit
```
```bash
docker compose run --rm backend poetry run pytest app/tests/integration
```