# create core directories
mkdir src
mkdir src/ai
mkdir src/data_ingestion
mkdir src/execution
mkdir src/monitoring
mkdir src/strategies
mkdir tests
mkdir terraform

# Create essential files (will be populated later)
touch requirements.txt
touch Dockerfile
touch terraform/main.tf
touch src/main.py

# Create initial empty files within src subdirectories
touch src/ai/models.py
touch src/data_ingestion/__init__.py
touch src/execution/executor.py
touch src/monitoring/monitor.py
touch src/strategies/strategy.py

# Create initial empty test files
touch tests/test_ai.py
touch tests/test_data_ingestion.py
touch tests/test_executor.py
touch tests/test_monitor.py
touch tests/test_strategy.py

# Git repository
echo ".venv/\n__pycache__/\n*.pyc\n.DS_Store\n.env\n.aws/\nterraform/.terraform/\nterraform/*.tfstate*\n" > .gitignore
git add .
git commit -m "chore: Initial project structure"