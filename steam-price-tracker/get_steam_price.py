import requests
from bs4 import BeautifulSoup

def get_steam_price(game_name):
    url = f"https://store.steampowered.com/search/?term={game_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("a", class_="search_result_row")

    if result:
        title_tag = result.find("span", class_="title")
        price_tag = result.find("div", class_="search_price")

        title = title_tag.text.strip() if title_tag else "未命名"
        if price_tag:
            price_text = price_tag.text.strip().replace("\n", " ").replace("Free", "0").strip()
            if "NT$" in price_text:
                price = price_text.split("NT$")[-1].strip()
            else:
                price = price_text or "查無價格"
        else:
            price = "查無價格"

        return {"name": title, "current_price": price}

    return None
