import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

const Signup: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await api.register(email, password, fullName || undefined);
      alert("Account created. You can now sign in.");
      navigate("/login");
    } catch (err: any) {
      setError(err.message || "Sign up failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="max-w-md mx-auto bg-white rounded-lg shadow-sm border border-cloud-accent/40 p-6">
      <h2 className="text-2xl font-bold text-cloud-primary mb-4">Sign up</h2>
      <p className="text-sm text-cloud-primary/80 mb-4">
        Create an account to save your cart and track your orders.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-cloud-primary mb-1">
            Full name
          </label>
          <input
            className="w-full rounded-md border border-cloud-accent/60 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-cloud-primary/60"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>
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
          {loading ? "Creating account..." : "Sign up"}
        </button>
      </form>
    </section>
  );
};

export default Signup;