from fastapi import FastAPI, BackgroundTasks
import os
import threading
from src.main import run_trading_bot, bot_stop_event
from src.monitoring.monitor import TradingMonitor
from typing import Dict, Any

app = FastAPI()
bot_thread = None
bot_running = False
monitor_instance = TradingMonitor(log_file='trading_bot_run.log')

@app.get("/")
def read_root() -> Dict[str, Any]:
    return {
        "status": "ok",
        "bot_running": bot_running,
        "settings": {
            "execution_mode": os.getenv('EXECUTION_MODE', 'paper'),
            "trading_cycle_interval": int(os.getenv('TRADING_CYCLE_INTERVAL_SECONDS', 300)),
            "api_key_set": bool(os.getenv('BINANCE_API_KEY')),
            "strategy": "default"
        }
    }

@app.post("/start")
def start_bot(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    global bot_thread, bot_running
    if not bot_running:
        bot_stop_event.clear()
        bot_thread = threading.Thread(target=run_trading_bot, kwargs={"stop_event": bot_stop_event}, daemon=True)
        bot_thread.start()
        bot_running = True
        return {"message": "Bot started"}
    return {"message": "Bot already running"}

@app.post("/stop")
def stop_bot() -> Dict[str, Any]:
    global bot_running
    if bot_running:
        bot_stop_event.set()
        bot_running = False
        return {"message": "Bot stop signal sent"}
    return {"message": "Bot is not running"}

@app.get("/status")
def get_status() -> Dict[str, Any]:
    return {
        "bot_running": bot_running,
        "thread_alive": bot_thread.is_alive() if bot_thread else False
    }

@app.get("/settings")
def get_settings() -> Dict[str, Any]:
    return {
        "execution_mode": os.getenv('EXECUTION_MODE', 'paper'),
        "trading_cycle_interval": int(os.getenv('TRADING_CYCLE_INTERVAL_SECONDS', 300)),
        "api_key_set": bool(os.getenv('BINANCE_API_KEY')),
        "strategy": "default"
    }

@app.post("/settings")
def update_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    # For demo: only allow changing trading_cycle_interval and execution_mode
    if 'trading_cycle_interval' in settings:
        os.environ['TRADING_CYCLE_INTERVAL_SECONDS'] = str(settings['trading_cycle_interval'])
    if 'execution_mode' in settings:
        os.environ['EXECUTION_MODE'] = settings['execution_mode']
    return {"message": "Settings updated", "settings": get_settings()}

@app.get("/metrics")
def get_metrics() -> Dict[str, Any]:
    metrics = monitor_instance.get_current_metrics()
    return {"metrics": metrics}