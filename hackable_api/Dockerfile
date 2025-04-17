FROM python:3.11-slim

# Install Poetry and dependencies
RUN apt-get update && apt-get install -y tzdata \
  && pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

WORKDIR /api/app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install

COPY . /api/app

# Set environment for Python imports
ENV PYTHONPATH=/app

# Command to run the app
CMD ["poetry", "run", "python", "app/run_app.py"]
