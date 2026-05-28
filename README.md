# CloudCom E-Commerce Platform

CloudCom is a full-stack E-Commerce application deployed on a VPS. It includes:

- A React + Vite frontend
- A FastAPI backend
- PostgreSQL as the main transactional database
- A separate reporting database for analytics
- Automated ETL processes (via cron) to sync from main DB to reporting DB
- An analytics dashboard showing sales, revenue, top products, and customer stats

---

## 1. Architecture Overview

### Components

- **Frontend**
  - Built with React + Vite
  - Served from the VPS (e.g. via `serve -s dist` or nginx)
  - Uses `VITE_API_URL` to call the backend (e.g. `http://<server-ip>:8000`)

- **Backend (API)**
  - FastAPI app (`app.main:app`)
  - Runs on `http://<server-ip>:8000`
  - Routers:
    - `auth` – user registration and login
    - `products` – product listing and details
    - `cart` – shopping cart operations
    - `orders` – checkout and order creation
    - `analytics` – reporting endpoints

- **Main (Transactional) Database**
  - PostgreSQL
  - Stores:
    - Users
    - Products
    - Carts and cart items
    - Orders and order items

- **Reporting Database**
  - Separate PostgreSQL database (or schema) for analytics
  - Tables:
    - `daily_sales` (via `DailySales` model)
      - `date`
      - `total_orders`
      - `total_revenue`
      - `total_items`
    - `top_product_daily` (via `TopProductDaily` model)
      - `date`
      - `product_id`
      - `product_name`
      - `total_quantity`
      - `total_revenue`

- **ETL Process**
  - Script: `backend/app/etl_to_reporting.py`
  - Reads from main DB (`orders`, `order_items`, `products`)
  - Aggregates by day into `daily_sales` and `top_product_daily`
  - Runs automatically via cron (every minute)

- **Automation & Services**
  - `systemd` services:
    - `cloudcom-backend.service` – runs the FastAPI backend
    - `cloudcom-frontend.service` – serves the built frontend
  - `cron` job:
    - Runs ETL every minute to keep analytics up to date

---

## 2. Backend Setup

### 2.1 Clone and install

```bash
# On the VPS
cd /root
git clone https://github.com/<your-username>/<your-repo>.git cloudcom
cd cloudcom/backend

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2.2 Environment configuration

Create a `.env` file (or similar) used by `app.config`:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/cloudcom
REPORTING_DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/cloudcom_reporting
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Adjust values as needed for your environment.

### 2.3 Run backend manually (for testing)

```bash
cd /root/cloudcom/backend
source .venv/bin/activate
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API is then available at `http://<server-ip>:8000`.

---

## 3. Reporting DB and ETL

### 3.1 Reporting models

- `backend/app/reporting_models.py` defines:
  - `DailySales`
  - `TopProductDaily`

These map to the `daily_sales` and `top_product_daily` tables in the reporting DB.

### 3.2 ETL script

- Script: `backend/app/etl_to_reporting.py`
- Responsibilities:
  - Ensure reporting tables exist
  - For a given date (default: today):
    - Remove any existing rows for that date (idempotent)
    - Aggregate:
      - Total orders
      - Total revenue
      - Total items
      - Top products by quantity and revenue
    - Insert rows into:
      - `daily_sales`
      - `top_product_daily`

### 3.3 Run ETL manually

```bash
cd /root/cloudcom/backend
source .venv/bin/activate
python3 -m app.etl_to_reporting
```

You should see output like:

```text
ETL completed for YYYY-MM-DD
```

---

## 4. Automating ETL with Cron

To keep analytics updated automatically, ETL is scheduled to run every minute using cron.

Set up (as root):

```bash
# Append ETL cron job
(sudo crontab -l 2>/dev/null; echo "* * * * * cd /root/cloudcom/backend && /root/cloudcom/backend/.venv/bin/python -m app.etl_to_reporting >> /var/log/cloudcom_etl.log 2>&1") | sudo crontab -
```

Verify:

```bash
sudo crontab -l
# You should see the ETL line
```

This ensures:

- ETL runs every minute
- `daily_sales` and `top_product_daily` stay in sync with the latest orders
- Logs are stored in `/var/log/cloudcom_etl.log`

---

## 5. Frontend Setup

### 5.1 Install and build

```bash
cd /root/cloudcom/frontend
npm install
```

Create `.env.production`:

```env
VITE_API_URL=http://<server-ip>:8000
```

Then build:

```bash
npm run build
```

### 5.2 Serve the built frontend (example with `serve`)

```bash
npm install -g serve
serve -s dist -l 4173
```

The frontend will be available at `http://<server-ip>:4173`.

---

## 6. Running Backend and Frontend via systemd

### 6.1 Backend service (`cloudcom-backend.service`)

Create:

```bash
sudo nano /etc/systemd/system/cloudcom-backend.service
```

Contents:

```ini
[Unit]
Description=CloudCom FastAPI backend
After=network.target

[Service]
User=root
WorkingDirectory=/root/cloudcom/backend
Environment="PATH=/root/cloudcom/backend/.venv/bin"
ExecStart=/root/cloudcom/backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudcom-backend
sudo systemctl start cloudcom-backend
sudo systemctl status cloudcom-backend
```

### 6.2 Frontend service (`cloudcom-frontend.service`)

Create:

```bash
sudo nano /etc/systemd/system/cloudcom-frontend.service
```

Contents:

```ini
[Unit]
Description=CloudCom frontend (Vite build)
After=network.target

[Service]
User=root
WorkingDirectory=/root/cloudcom/frontend
ExecStart=/usr/local/bin/serve -s dist -l 4173
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

(Adjust the `ExecStart` path to `serve` as needed, e.g. use `which serve`.)

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudcom-frontend
sudo systemctl start cloudcom-frontend
sudo systemctl status cloudcom-frontend
```

Now both backend and frontend start automatically on boot.

---

## 7. Application Features

### 7.1 Authentication

- Register: `/auth/register`
- Login: `/auth/login`
  - JWT tokens with `sub` set to user email
  - `get_current_user` uses the email from JWT to load the user

### 7.2 Products

- Endpoint: `GET /products`
  - Optional query: `?q=<search>`
  - Returns JSON list of products
- Frontend uses `getProducts` in `frontend/src/api.ts` to display product list.

### 7.3 Cart and Orders

- Cart:
  - `GET /cart/` – get current cart for logged in user
  - `POST /cart/add` – add items to cart
  - `POST /cart/clear` – clear cart
- Checkout:
  - `POST /orders/checkout` – converts cart into an order and order_items

### 7.4 Analytics

- `GET /analytics/daily-sales`
  - Query params:
    - `start_date` (YYYY-MM-DD)
    - `end_date` (YYYY-MM-DD)
  - Returns:
    - `date`
    - `total_orders`
    - `total_revenue`
    - `total_items`

- `GET /analytics/top-products`
  - Query params:
    - `target_date` (YYYY-MM-DD)
    - `limit` (e.g. 5)
  - Returns:
    - `product_id`
    - `product_name`
    - `total_quantity`
    - `revenue`

Frontend analytics dashboard consumes these endpoints to show:

- Daily sales chart/table
- Top products per day

---

## 8. Demo Script (What to Show)

1. **Architecture slide/overview**
   - Explain:
     - Frontend (React/Vite)
     - Backend (FastAPI)
     - Main PostgreSQL DB
     - Reporting DB
     - ETL + cron
     - Analytics dashboard

2. **User flow (frontend)**
   - Open frontend URL (e.g. `http://<server-ip>:4173`)
   - Show products page (data from `/products`)
   - Register or log in
   - Add items to cart
   - Checkout to create an order

3. **ETL and reporting**
   - Explain ETL script `etl_to_reporting.py`
   - Mention cron job running every minute
   - Optionally show logs from `/var/log/cloudcom_etl.log`

4. **Analytics dashboard**
   - Open analytics page in frontend
   - Select appropriate date range
   - Show:
     - Daily total orders, revenue, and items
     - Top products for a selected date

5. **Operations**
   - Show `systemctl status cloudcom-backend` and `cloudcom-frontend`
   - Show `sudo crontab -l` with ETL cron line

This demonstrates the full requirement:
- Full-stack e-commerce
- Separate transactional and reporting DBs
- Automated ETL
- Reporting dashboard
- Deployed and accessible via VPS
