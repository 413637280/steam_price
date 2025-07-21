from apscheduler.schedulers.background import BackgroundScheduler
from db import get_tracked_games, insert_price
from get_steam_price import get_steam_price

def update_prices():
    games = get_tracked_games()
    for game in games:
        data = get_steam_price(game)
        if data:
            insert_price(data["name"], data["current_price"])

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_prices, "interval", hours=24)
    scheduler.start()