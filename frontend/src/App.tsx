// frontend/src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import Home from "./pages/Home";
import ProductList from "./pages/ProductList";
import Cart from "./pages/Cart";

// Small wrapper to access navigate in header
const AppShell: React.FC = () => {
  const navigate = useNavigate();
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const userEmail =
    typeof window !== "undefined" ? localStorage.getItem("user_email") : null;

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_email");
    // Optional: clear cart UI or other state here
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-cloud-light">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <Link to="/" className="font-bold text-lg">
            CloudShop
          </Link>
          <nav className="space-x-4 text-sm flex items-center">
            <Link to="/" className="hover:underline">
              Home
            </Link>
            <Link to="/products" className="hover:underline">
              Products
            </Link>
            <Link to="/cart" className="hover:underline">
              Cart
            </Link>
            <Link to="/analytics" className="hover:underline">
              Analytics
            </Link>

            {token ? (
              <>
                {userEmail && (
                  <span className="text-xs text-cloud-primary/70">
                    {userEmail}
                  </span>
                )}
                <button
                  onClick={handleLogout}
                  className="px-3 py-1 rounded-md border border-cloud-primary text-cloud-primary text-xs font-semibold hover:bg-cloud-primary/5"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:underline">
                  Login
                </Link>
                <Link to="/signup" className="hover:underline">
                  Sign up
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<ProductList />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </main>
    </div>
  );
};

const App: React.FC = () => (
  <BrowserRouter>
    <AppShell />
  </BrowserRouter>
);

export default App;