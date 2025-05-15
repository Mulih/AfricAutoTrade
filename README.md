# AfricAutoTrade

## Overview

Modular, production-grade trading bot for equities and crypto.

## Structure

- `src/data/`: Data ingestion (exchange fetchers, base classes)
- `src/core/`: Signal generation, indicators, backtesting, performance metrics
- `src/risk/`: Risk management (position sizing, circuit breakers)
- `src/execution/`: Order execution (exchange adapters, mocks)
- `src/monitoring/`: Monitoring, Prometheus metrics, notifications
- `src/api/`: FastAPI endpoints (REST API)
- `src/settings/`: Configuration and secrets management
- `src/models/`: Database models and session management
- `tests/`: Unit and integration tests

## Installation

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

- Copy `.env.example` to `.env` and edit as needed.
- See `src/settings/config.py` for all environment variables.
- Secrets can be loaded from AWS Secrets Manager or environment.

## Testing

```sh
pytest --cov=src
```

- Coverage reports are generated in the terminal.
- All core modules and critical paths are tested.

## Deployment

- Build Docker image:
  `docker build -t africautotrade .`
- Run locally:
  `docker run -p 8000:8000 --env-file .env africautotrade`
- Healthcheck:
  Dockerfile includes a `/health` endpoint for container health.
- CI/CD:
  See `.github/workflows/ci-cd.yml` for linting, testing, build, and AWS deployment.

## API

- `/fetch/stock/{symbol}` – Fetch stock data
- `/fetch/crypto/{symbol}` – Fetch crypto data
- `/qa` – Run QA checks
- `/metrics` – Prometheus metrics endpoint
- `/health` – Healthcheck endpoint

## Monitoring & Logging

- Centralized logging (CloudWatch/Grafana ready)
- Prometheus `/metrics` endpoint for live metrics

## Documentation

- All modules include Sphinx-style docstrings.
- To build HTML docs:

  ```sh
  cd docs
  make html
  ```

- See `docs/` for API and developer documentation.

## Contributing

- Please lint and test before submitting PRs.
- Follow modular architecture and type-hinting best practices.

## License

MIT License
