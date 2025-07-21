from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import random
import time

app = Flask(__name__)

# 從環境變數讀取 MongoDB 連線字串
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["steam_tracker"]
favorites_collection = db["favorites"]

def get_steam_price(game_name):
    search_url = f"https://store.steampowered.com/search/?term={game_name}"
    
    # 使用 undetected_chromedriver
    options = uc.ChromeOptions()
    options.add_argument("--headless")  # 無頭模式
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 防止被檢測為自動化工具
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(search_url)
        time.sleep(random.uniform(2, 5))  # 隨機延遲模擬人類行為
        game_item = driver.find_element(By.CSS_SELECTOR, "a.search_result_row")
        name = game_item.find_element(By.CSS_SELECTOR, ".title").text.strip()
        price_element = game_item.find_element(By.CSS_SELECTOR, ".search_price")
        price_text = price_element.text.strip()
        
        if "NT$" in price_text:
            prices = [p.strip() for p in price_text.split("NT$") if p.strip()]
            price = prices[-1] if prices else "查無價格"
        else:
            price = "查無價格"
        
        return {"name": name, "current_price": price}
    except Exception as e:
        return {"name": game_name, "current_price": f"爬蟲錯誤: {str(e)}"}
    finally:
        driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        game = request.form.get("query")
        if game:
            result = get_steam_price(game)
    tracked = list(favorites_collection.find({}, {"_id": 0, "name": 1}))
    return render_template("index.html", result=result, tracked=tracked)

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    game = request.form.get("game")
    if game:
        if not favorites_collection.find_one({"name": game}):
            favorites_collection.insert_one({"name": game})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
