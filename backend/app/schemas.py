# backend/app/schemas.py

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ----------------------------
# User schemas
# ----------------------------

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

    @field_validator("password")
    @classmethod
    def password_max_length(cls, v: str) -> str:
        # bcrypt via passlib only supports up to 72 bytes
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes long")
        return v


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True  # like orm_mode in Pydantic v1
    }


# ----------------------------
# Product schemas
# ----------------------------

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class ProductRead(ProductBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# ----------------------------
# Cart / Order schemas
# ----------------------------

class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    line_total: float
    product_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class OrderRead(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemRead] = []

    model_config = {
        "from_attributes": True
    }


# ----------------------------
# Token / auth schemas
# ----------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
