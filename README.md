# AfricAutoTrade: Automated Crypto Trading Bot

[![Build Status](https://img.shields.io/github/actions/workflow/status/Mulih/AfricAutoTrade/ci.yml?branch=main&label=build)](https://github.com/Mulih/AfricAutoTrade/actions)
[![License](https://img.shields.io/github/license/Mulih/AfricAutoTrade)](https://github.com/Mulih/AfricAutoTrade/blob/main/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/mulih/africautotrade?label=Docker%20Pulls)](https://hub.docker.com/r/mulih/africautotrade)
[![GitHub stars](https://img.shields.io/github/stars/Mulih/AfricAutoTrade?style=social)](https://github.com/Mulih/AfricAutoTrade)

---

## Overview

AfricAutoTrade is a modular, production-grade, and extensible automated trading bot for cryptocurrency markets. It leverages machine learning, advanced order book analytics, and robust monitoring to automate trading strategies. Designed for both personal and professional use, it is ready for extension, deployment, and public demonstration.

---

## Features

- **Modular Architecture**: Clean separation of data ingestion, AI/ML, strategy, execution, and monitoring.
- **Machine Learning**: Uses a RandomForestClassifier with feature scaling for robust, data-driven predictions. Order book analytics are included as model features.
- **Strategy Engine**: Pluggable strategies, including AI-driven and order book-aware logic. Easily extend with industry-standard strategies (e.g., MA Crossover, RSI, MACD).
- **Order Book Analytics**: Real-time spread, imbalance, VWAP, and liquidity metrics, available for strategies, monitoring, and AI features.
- **Paper & Live Trading**: Switch between simulated and real trading with environment variables. Supports Binance and can be extended to other exchanges.
- **Advanced Monitoring**: Tracks PnL, win rate, drawdown, order book metrics, and more. Metrics are exposed via the MCP server API.
- **MCP Server (API)**: FastAPI-based server for browser/API control, settings, and metrics. Start, stop, and monitor the bot remotely.
- **Graceful Start/Stop**: Control the bot lifecycle via API or CLI, with safe shutdown and restart.
- **Dockerized**: Production-ready Docker and Compose setup, with secure user permissions and persistent logs.
- **Secure Secrets**: Uses Docker secrets and .env for sensitive data. Never commit secrets to version control.
- **Extensible Data Sources**: Scaffolded for order book, WebSocket, news/sentiment, on-chain, and macroeconomic data.
- **Unit Tested**: Includes tests for all major modules.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone <repo-url>
cd AfricAutoTrade
```

### 2. Set Up Environment

- Copy `.env.example` to `.env` and fill in your API keys.
- Create `db/password.txt` with a strong password (see `compose.yaml`).
- Ensure `logs/` directory exists (created automatically by Docker).

### 3. Build and Run with Docker Compose

```bash
docker compose build
docker compose up -d
```

### 4. Access the API

- Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API (FastAPI Swagger UI).
- Use `/start`, `/stop`, `/status`, `/settings`, and `/metrics` endpoints to control and monitor the bot.
- All metrics, including order book analytics, are available at `/metrics`.

---

## Project Structure

```text
AfricAutoTrade/
├── src/
│   ├── main.py                # Main trading loop and orchestration
│   ├── mcp_server.py          # FastAPI MCP server for control/monitoring
│   ├── ai/models.py           # AI/ML model logic (RandomForest, scaling, persistence)
│   ├── data_ingestion/        # Market data, order book, and advanced data sources
│   ├── execution/executor.py  # Trade execution (paper/live, Binance)
│   ├── monitoring/monitor.py  # Logging, metrics, and alerting
│   └── strategies/strategy.py # Trading strategies (AI, order book, etc.)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Production Docker build (secure user, logs)
├── compose.yaml               # Docker Compose for multi-service orchestration
├── db/password.txt            # Postgres password (secret, gitignored)
├── logs/                      # Persistent logs (mounted in Docker)
├── .env                       # Environment variables (gitignored)
└── tests/                     # Unit tests for all modules
```

---

## Configuration

- **.env**: Set your Binance API keys, database URL, and other secrets here.
- **compose.yaml**: Configure services, secrets, and volumes. PostgreSQL is included for persistence.
- **Environment Variables**:
  - `BINANCE_API_KEY`, `BINANCE_API_SECRET`: Your Binance credentials.
  - `EXECUTION_MODE`: `paper` or `live`.
  - `TRADING_CYCLE_INTERVAL_SECONDS`: How often the bot runs a trading cycle.

---

## Monitoring & Analytics

- **Metrics**: PnL, win rate, drawdown, order book spread, imbalance, VWAP, liquidity, and more.
- **API Access**: All metrics are available at `/metrics` via the MCP server.
- **Logging**: All actions and errors are logged to `logs/trading_bot_run.log` (persistent and host-accessible).
- **Alerting**: Alerts can be sent via log, print, or extended to email/SMS/Slack.

---

## Extending the Bot

- **Add New Strategies**: Implement new classes in `src/strategies/strategy.py` and select via settings.
- **Improve AI Model**: Swap in new ML models in `src/ai/models.py` (e.g., XGBoost, LSTM, etc.).
- **Integrate More Exchanges**: Add new execution modules in `src/execution/`.
- **Enhance Monitoring**: Extend `TradingMonitor` for more metrics or external alerting (Slack, email, etc.).
- **Advanced Data Sources**: Use the scaffolded functions in `data_ingestion` for order book, WebSocket, news, on-chain, and macro data.

---

## Security & Best Practices

- **Secrets**: Never commit `.env` or `db/password.txt` to version control.
- **API Keys**: Use read-only keys for paper trading. For live trading, use withdrawal-disabled keys.
- **Testing**: Run all tests in `tests/` before deploying changes.
- **Production**: Deploy behind a firewall, use HTTPS for the API, and monitor logs for anomalies.
- **Docker**: Runs as a non-root user, logs are persisted and always writable.

---

## DevOps & Deployment

- **CI/CD**: Integrate with GitHub Actions or similar for automated testing and deployment.
- **Docker**: All dependencies are pinned in `requirements.txt` for reproducible builds.
- **Logging**: All actions and errors are logged to `logs/trading_bot_run.log` and surfaced via the API.
- **Monitoring**: Use `/metrics` endpoint for real-time health and performance.
- **Persistent Logs**: Host `./logs` directory is mounted into the container for easy access and backup.

---

## License

This project is proprietary. You must contact [your.email@example.com] for permission to use this software.

---

## Disclaimer

This bot is for educational and personal use only. Trading cryptocurrencies is risky. The author is not responsible for any financial losses incurred.

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

## Author

- Alvin Muli Kyalo
- [[Github](https://github.com/Mulih)]
