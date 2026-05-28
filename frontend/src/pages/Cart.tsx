// frontend/src/pages/Cart.tsx
import React, { useEffect, useState } from "react";
import { api } from "../api";

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  product_name?: string;
  product_price?: number;
}

const Cart: React.FC = () => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const loadCart = async () => {
    if (!token) {
      setError("Please log in to view your cart.");
      setItems([]);
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      setError(null);
      const data = await api.getCart(token);
      setItems(data);
    } catch (e: any) {
      console.error(e);
      setError(e.message || "Failed to load cart.");
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCart();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handleClear = async () => {
    if (!token) return;
    try {
      await api.clearCart(token);
      await loadCart();
    } catch (e: any) {
      alert(e.message || "Failed to clear cart.");
    }
  };

  const handleCheckout = async () => {
    if (!token) {
      alert("Please log in to checkout.");
      return;
    }

    try {
      const order = await api.checkout(token);
      alert(`Checkout successful. Order #${order.id} created.`);
      await loadCart();
    } catch (e: any) {
      alert(e.message || "Checkout failed.");
    }
  };

  if (!token) {
    return (
      <p className="text-sm text-cloud-primary">
        Please log in to view and manage your cart.
      </p>
    );
  }

  if (loading) {
    return <p className="text-sm text-cloud-primary">Loading cart...</p>;
  }

  if (error) {
    return <p className="text-sm text-red-600">{error}</p>;
  }

  const total = items.reduce((sum, item) => {
    const price = item.product_price || 0;
    return sum + price * item.quantity;
  }, 0);

  return (
    <section>
      <h2 className="text-2xl font-bold mb-4 text-cloud-primary">
        Your Cart
      </h2>
      {items.length === 0 ? (
        <p className="text-sm text-cloud-primary">Your cart is empty.</p>
      ) : (
        <>
          <div className="space-y-3 mb-4">
            {items.map((item) => (
              <div
                key={item.id}
                className="flex justify-between items-center bg-white rounded-md shadow-sm px-3 py-2 border border-cloud-accent/40"
              >
                <div>
                  <p className="font-semibold text-cloud-primary">
                    {item.product_name || `Product ${item.product_id}`}
                  </p>
                  <p className="text-sm text-cloud-primary/80">
                    Qty: {item.quantity} • ₱
                    {(item.product_price || 0).toFixed(2)}
                  </p>
                </div>
                <p className="font-bold text-cloud-secondary">
                  ₱{((item.product_price || 0) * item.quantity).toFixed(2)}
                </p>
              </div>
            ))}
          </div>

          <div className="flex justify-between items-center border-t border-cloud-primary/20 pt-3">
            <p className="text-lg font-semibold text-cloud-primary">Total:</p>
            <p className="text-xl font-bold text-cloud-primary">
              ₱{total.toFixed(2)}
            </p>
          </div>

          <div className="mt-4 flex gap-3">
            <button
              onClick={handleClear}
              className="px-4 py-2 rounded-md bg-cloud-primary text-cloud-light font-semibold hover:bg-cloud-secondary hover:text-cloud-primary transition-colors"
            >
              Clear cart
            </button>
            <button
              onClick={handleCheckout}
              className="px-4 py-2 rounded-md bg-cloud-secondary text-cloud-primary font-semibold hover:bg-cloud-accent transition-colors"
            >
              Checkout (API)
            </button>
          </div>
        </>
      )}
    </section>
  );
};

export default Cart;