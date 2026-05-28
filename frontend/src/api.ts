// frontend/src/api.ts

const API_BASE = import.meta.env.VITE_API_URL;

export const api = {
  // Auth
  async register(email: string, password: string, full_name?: string) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, full_name }),
    });
    if (!res.ok) throw new Error("Registration failed");
    return res.json();
  },

  async login(email: string, password: string) {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
    });
    if (!res.ok) throw new Error("Login failed");
    return res.json();
  },

  // Products
  async getProducts(q?: string) {
    const query = q ? `?q=${encodeURIComponent(q)}` : "";
    const res = await fetch(`${API_BASE}/products${query}`);
    if (!res.ok) throw new Error("Failed to fetch products");
    return res.json();
  },

  // Cart
  async getCart(token: string) {
    const res = await fetch(`${API_BASE}/cart/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Failed to fetch cart");
    return res.json();
  },

  async addToCart(token: string, product_id: number, quantity: number) {
    const res = await fetch(`${API_BASE}/cart/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ product_id, quantity }),
    });
    if (!res.ok) throw new Error("Failed to add to cart");
    return res.json();
  },

  async clearCart(token: string) {
    const res = await fetch(`${API_BASE}/cart/clear`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({}),
    });
    if (!res.ok) throw new Error("Failed to clear cart");
    return res.json();
  },

  // Checkout
  async checkout(token: string) {
    const res = await fetch(`${API_BASE}/orders/checkout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!res.ok) throw new Error("Checkout failed");
    return res.json();
  },

  // ===== Analytics =====
  async getDailySales(startDate: string, endDate: string) {
    const params = new URLSearchParams();
    params.append("start_date", startDate);
    params.append("end_date", endDate);

    const res = await fetch(
      `${API_BASE}/analytics/daily-sales?${params.toString()}`
    );
    if (!res.ok) throw new Error("Failed to fetch daily sales");
    return res.json();
  },

  async getTopProducts(targetDate: string, limit: number = 5) {
    const params = new URLSearchParams();
    params.append("target_date", targetDate);
    params.append("limit", String(limit));

    const res = await fetch(
      `${API_BASE}/analytics/top-products?${params.toString()}`
    );
    if (!res.ok) throw new Error("Failed to fetch top products");
    return res.json();
  },
};
