#!/usr/bin/bash
set -e

# 1. Configurable variables
PROJECT_NAME=${1:-AfricAutoTrade}  # pass an argument or defaults to "trading-bot"
BASE_DIR="./${PROJECT_NAME}"

# 2. Define directory tree
dirs=(
    "$BASE_DIR/.github/workflows"
    "$BASE_DIR/src/api"
    "$BASE_DIR/src/core"
    "$BASE_DIR/src/core"
    "$BASE_DIR/src/data"
    "$BASE_DIR/src/models"
    "$BASE_DIR/src/services"
    "$BASE_DIR/tests"
)

# 3. Create directories
for d in "${dirs[@]}"; do
  mkdir -p "$d"
  echo "Created: $d"
done

# 4. Create placeholder files
touch \
  "$BASE_DIR/.gitignore" \
  "$BASE_DIR/requirements.txt" \
  "$BASE_DIR/Dockerfile" \
  "$BASE_DIR/.github/workflows/ci-cd.yml" \
  "$BASE_DIR/src/api/main.py" \
  "$BASE_DIR/src/core/backtester.py" \
  "$BASE_DIR/src/core/strategy.py" \
  "$BASE_DIR/src/core/indicators.py" \
  "$BASE_DIR/src/data/binance_client.py" \
  "$BASE_DIR/src/data/alpha_vantage.py" \
  "$BASE_DIR/src/models/db_models.py" \
  "$BASE_DIR/rc/models/schema.py" \
  "$BASE_DIR/src/services/trade_service.py" \
  "$BASE_DIR/tests/test_backtester.py" \
  "$BASE_DIR/tests/test_endpoints.py"

# 5. Seed templates
cat > "BASE_DIR/.gitignore" <<EOF
# Python
__pycache__/
*.pyc
.venv/

# Env
.env
EOF

cat > "$BASE_DIR/requirements.txt" <<EOF
langchain
backtesting.py
alpha_vantage
python-binance
psycopg2-binary
SQLAlchemy
openai
loguru
pytest
pydantic
asyncio
GitPython
docker
fastapi
uvicorn
tenacity
limits
EOF

cat > "$BASE_DIR/.github/workflows/ci-cd.yml" <<EOF
name: CI/CD Pipeline
on:
  push:
    branches: [ develop, main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with: { python-version: 3.12.3 }
      - name: Install dependencies
        run: |
          source .venv/bin/activate
          pip install -r requirements.txt
      - name: Lint
        run: |
          source .venv/bin/activate
          pip install flake8
          flake8 .
      - name: Test
        run: |
          source .venv/bin/activate
          pytest
EOF

echo "Project skeleton '$PROJECT_NAME' created.