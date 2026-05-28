// frontend/src/pages/ProductList.tsx
import React, { useEffect, useState } from "react";
import { api } from "../api";

interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  stock: number;
}

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Read token from localStorage (same as Cart)
  const token = typeof window !== "undefined"
    ? localStorage.getItem("token")
    : null;

  useEffect(() => {
    api
      .getProducts()
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to load products");
        setLoading(false);
      });
  }, []);

  const handleAddToCart = async (productId: number) => {
    if (!token) {
      alert("Please log in via the backend docs (/docs) to use the cart.");
      return;
    }
    try {
      await api.addToCart(token, productId, 1);
      alert("Added to cart");
    } catch (e) {
      alert("Failed to add to cart");
    }
  };

  if (loading) {
    return <p>Loading products...</p>;
  }

  if (error) {
    return <p className="text-red-600">{error}</p>;
  }

  return (
    <section>
      <h2 className="text-2xl font-bold mb-4">Products</h2>
      {products.length === 0 ? (
        <p>No products available.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-3">
          {products.map((p) => (
            <div
              key={p.id}
              className="bg-white rounded-lg shadow-sm border border-cloud-accent/40 p-4"
            >
              <h3 className="text-lg font-semibold mb-1 text-cloud-primary">
                {p.name}
              </h3>
              <p className="text-sm text-cloud-primary/80 mb-2">
                {p.description || "No description"}
              </p>
              <p className="font-bold text-cloud-secondary mb-1">
                ₱{p.price.toFixed(2)}
              </p>
              <p className="text-xs text-cloud-primary/70 mb-3">
                Stock: {p.stock}
              </p>
              <button
                onClick={() => handleAddToCart(p.id)}
                className="w-full px-3 py-2 rounded-md bg-cloud-secondary text-cloud-primary font-semibold hover:bg-cloud-accent transition-colors"
              >
                Add to cart
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default ProductList;