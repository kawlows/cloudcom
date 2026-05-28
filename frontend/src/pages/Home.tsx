// frontend/src/pages/Home.tsx
import React from "react";
import { useNavigate } from "react-router-dom";

const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleGoProducts = () => {
    navigate("/products");
  };

  return (
    <div className="space-y-16">
      {/* Hero */}
      <section className="flex flex-col md:flex-row items-center justify-between gap-8 py-12">
        <div className="max-w-xl">
          <p className="uppercase tracking-wide text-xs font-semibold text-cloud-secondary mb-2">
            New season, new gear
          </p>
          <h1 className="text-4xl md:text-5xl font-extrabold text-cloud-primary mb-4">
            Everything you need, in one shop.
          </h1>
          <p className="text-lg text-cloud-primary/80 mb-6">
            Discover curated tech, accessories, and everyday essentials with fast checkout and a clean, modern experience.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleGoProducts}
              className="px-6 py-3 rounded-md bg-cloud-primary text-cloud-light font-semibold hover:bg-cloud-secondary hover:text-cloud-primary transition-colors"
            >
              Shop products
            </button>
            <button
              onClick={() => navigate("/cart")}
              className="px-6 py-3 rounded-md border border-cloud-primary text-cloud-primary font-semibold hover:bg-cloud-primary/5 transition-colors"
            >
              View cart
            </button>
          </div>
        </div>

        <div className="w-full md:w-1/2">
          <div className="bg-white rounded-xl shadow-lg border border-cloud-accent/40 p-6">
            <p className="text-sm font-semibold text-cloud-primary mb-4">
              Featured collections
            </p>
            <ul className="space-y-2 text-sm text-cloud-primary/80">
              <li>• Productivity essentials</li>
              <li>• Home and office upgrades</li>
              <li>• Accessories under ₱500</li>
              <li>• Limited-time offers</li>
            </ul>
            <p className="mt-4 text-xs text-cloud-primary/60">
              Browse our latest selection and add items to your cart in a few clicks.
            </p>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="grid gap-6 md:grid-cols-3">
        <div className="bg-white rounded-lg shadow-sm border border-cloud-accent/40 p-5">
          <h3 className="font-semibold text-cloud-primary mb-2">
            Simple shopping
          </h3>
          <p className="text-sm text-cloud-primary/80">
            Clean product catalog, straightforward cart, and no clutter—just the items you care about.
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-cloud-accent/40 p-5">
          <h3 className="font-semibold text-cloud-primary mb-2">
            Transparent pricing
          </h3>
          <p className="text-sm text-cloud-primary/80">
            Prices displayed clearly with totals calculated in your cart, so there are no surprises at checkout.
          </p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-cloud-accent/40 p-5">
          <h3 className="font-semibold text-cloud-primary mb-2">
            Fast and modern
          </h3>
          <p className="text-sm text-cloud-primary/80">
            Built with a modern stack for quick page loads and a responsive experience on any device.
          </p>
        </div>
      </section>
    </div>
  );
};

export default Home;