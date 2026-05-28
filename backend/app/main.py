# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, products, cart, orders, analytics


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# CORS settings
cors_origins = ["*"]
if settings.backend_cors_origins:
    cors_origins = [origin.strip() for origin in settings.backend_cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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
app.include_router(analytics.router, tags=["analytics"])
