# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.routers import auth
from backend.app.routers import products
from backend.app.routers import cart
from backend.app.routers import orders
from backend.app.routers import analytics

app = FastAPI(
    title="CloudShop API",
    description="CloudShop E-Commerce API with reporting and analytics",
    version="1.0.0",
)

# CORS settings (adjust allow_origins when deploying to VPS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "CloudShop API is running"}

# Routers
app.include_router(auth.router, tags=["auth"])
app.include_router(products.router, tags=["products"])
app.include_router(cart.router, tags=["cart"])
app.include_router(orders.router, tags=["orders"])
app.include_router(analytics.router)