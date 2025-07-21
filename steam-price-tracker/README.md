# Steam Price‑Tracker 🛒

一個讓玩家 **快速查詢 Steam 遊戲現價與折扣，並顯示歷史價格趨勢** 的全端專案  
（前端 React / 後端 Node.js + Express / 資料庫 MySQL）。

---

## 📑 目錄
1. [專案緣起](#專案緣起)
2. [核心功能](#核心功能)
3. [技術棧](#技術棧)
4. [系統架構圖](#系統架構圖)
5. [資料表結構](#資料表結構)
6. [API 一覽](#api-一覽)
7. [專案啟動](#專案啟動)
8. [開發進度 & 甘特圖](#開發進度--甘特圖)
9. [Todo / Roadmap](#todo--roadmap)
10. [License](#license)

---

## 專案緣起
Steam 平台折扣頻繁，但缺乏官方「歷史價格」查詢。  
本專案透過爬蟲與排程記錄價格，並提供 RESTful API 與前端 UI，  
協助玩家判斷「現在買划算嗎？」。

---

## 核心功能
| 分類 | 功能 |
|------|------|
| 訪客 | 🔍 關鍵字搜尋遊戲 → 顯示現價 / 原價 / 折扣 |
|      | 📋 查無資料時顯示提示 |
| Admin | 🗄️ 每日自動更新價格（爬蟲 + crontab） |
|      | 📊 未來擴充：歷史價格折線圖、價格提醒、願望清單 |

---

## 技術棧
| 層級 | 技術 |
|------|------|
| Frontend | React (+ Vite)、Axios、Tailwind、Chart.js |
| Backend  | Node.js、Express、cron、Cheerio |
| Database | MySQL (`products`, `price_history`) |
| DevOps   | VS Code、ESLint、GitHub Copilot、Render / Railway |

---

## 系統架構圖
```mermaid
flowchart TD
    subgraph 使用者
        Browser["Web Browser"]
    end
    subgraph 前端 (React)
        UI["搜尋 UI ‑ React"]
    end
    subgraph 後端 (Express)
        API["/api/search"]
    end
    DB[(MySQL)]

    Browser -- 輸入關鍵字 --> UI
    UI -- Axios --> API
    API -- SQL LIKE --> DB
    DB -- JSON --> API
    API -- 回傳結果 --> UI
    UI -- 顯示清單 --> Browser
```

CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  image_url TEXT,
  steam_url TEXT,
  current_price INT,
  original_price INT,
  discount INT
);

CREATE TABLE price_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT,
  price INT,
  recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id)
);

# 1. 後端
cd backend
npm install
npm run dev   # http://localhost:3000

# 2. 前端
cd frontend
npm install
npm run dev   # http://localhost:5173


gantt
  title Steam 商品查詢功能（週次）
  dateFormat  YYYY-MM-DD
  axisFormat  %W

  section Backend
  設計資料表          :done,    2025-07-01, 0.5w
  API 路由            :active,  after 2025-07-01, 0.5w
  模糊 SQL 查詢       :         after 2025-07-04, 0.3w
  JSON 回傳           :         after 2025-07-06, 0.3w

  section Frontend
  搜尋 UI            :done,    2025-07-01, 0.3w
  串接 API           :active,  after 2025-07-03, 0.3w
  渲染清單            :         after 2025-07-05, 0.3w
  無資料提示          :         after 2025-07-07, 0.15w

  section Test
  API 測試           :          after 2025-07-07, 0.3w
  整合測試           :          after 2025-07-08, 0.3w
