import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await api.login(email, password);
      // data should be { access_token, token_type }
      localStorage.setItem("token", data.access_token);
      // Optional: store email too if you want to show "Logged in as..."
      localStorage.setItem("user_email", email);

      alert("Logged in successfully");
      navigate("/products");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="max-w-md mx-auto bg-white rounded-lg shadow-sm border border-cloud-accent/40 p-6">
      <h2 className="text-2xl font-bold text-cloud-primary mb-4">Sign in</h2>
      <p className="text-sm text-cloud-primary/80 mb-4">
        Use the same email and password you registered in the system to access your cart and checkout.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-cloud-primary mb-1">
            Email
          </label>
          <input
            type="email"
            className="w-full rounded-md border border-cloud-accent/60 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-cloud-primary/60"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-cloud-primary mb-1">
            Password
          </label>
          <input
            type="password"
            className="w-full rounded-md border border-cloud-accent/60 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-cloud-primary/60"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-md bg-cloud-primary text-cloud-light font-semibold hover:bg-cloud-secondary hover:text-cloud-primary transition-colors disabled:opacity-50"
        >
          {loading ? "Signing in..." : "Sign in"}
        </button>
      </form>
    </section>
  );
};

export default Login;