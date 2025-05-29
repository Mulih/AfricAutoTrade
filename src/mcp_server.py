from fastapi import FastAPI, BackgroundTasks
from src.main import run_trading_bot
from typing import Dict, Any

app = FastAPI()
bot_running = False

@app.get("/")
def read_root() -> Dict[str, Any]:
    return {"status": "ok", "bot_running": bot_running}

@app.post("/start")
def start_bot(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    global bot_running
    if not bot_running:
        background_tasks.add_task(run_trading_bot)
        bot_running = True
        return {"message": "Bot started"}
    return {"message": "Bot already running"}

@app.post("/stop")
def stop_bot():
    return {"message": "Stop not implemented yet"}