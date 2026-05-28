// frontend/src/pages/AnalyticsPage.tsx
import React, { useEffect, useState } from "react";
import { api } from "../api";

interface DailySalesRow {
  date: string;
  total_orders: number;
  total_revenue: number;
  total_items: number;
}

interface TopProductRow {
  product_id: number;
  product_name: string;
  total_quantity: number;
  revenue: number;
}

const formatDateInput = (d: Date): string => d.toISOString().slice(0, 10);

export const AnalyticsPage: React.FC = () => {
  const today = new Date();
  const todayStr = formatDateInput(today);

  const [startDate, setStartDate] = useState<string>(todayStr);
  const [endDate, setEndDate] = useState<string>(todayStr);
  const [targetDate, setTargetDate] = useState<string>(todayStr);

  const [dailySales, setDailySales] = useState<DailySalesRow[]>([]);
  const [topProducts, setTopProducts] = useState<TopProductRow[]>([]);

  const [loading, setLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadAnalytics = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const [daily, top] = await Promise.all([
        api.getDailySales(startDate, endDate),
        api.getTopProducts(targetDate, 5),
      ]);
      setDailySales(daily ?? []);
      setTopProducts(top ?? []);
    } catch (error) {
      console.error("Failed to load analytics", error);
      setErrorMessage("Failed to load analytics data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadAnalytics();
  }, []);

  return (
    <div className="p-6 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Analytics Dashboard</h1>
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
          onClick={() => void loadAnalytics()}
          disabled={loading}
        >
          {loading ? "Loading..." : "Refresh"}
        </button>
      </div>

      {errorMessage && (
        <div className="p-3 rounded bg-red-100 text-red-700 text-sm">
          {errorMessage}
        </div>
      )}

      {/* Daily Sales */}
      <section className="space-y-4">
        <div className="flex flex-wrap items-center gap-4">
          <h2 className="text-xl font-semibold">Daily Sales</h2>
          <label className="text-sm">
            Start date:
            <input
              type="date"
              className="ml-2 border rounded px-2 py-1"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </label>
          <label className="text-sm">
            End date:
            <input
              type="date"
              className="ml-2 border rounded px-2 py-1"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </label>
        </div>

        <div className="overflow-x-auto border rounded">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-3 py-2 border">Date</th>
                <th className="px-3 py-2 border">Total Orders</th>
                <th className="px-3 py-2 border">Total Revenue</th>
                <th className="px-3 py-2 border">Total Items</th>
              </tr>
            </thead>
            <tbody>
              {dailySales.length === 0 ? (
                <tr>
                  <td className="px-3 py-2 border text-center" colSpan={4}>
                    No data
                  </td>
                </tr>
              ) : (
                dailySales.map((row) => (
                  <tr key={row.date}>
                    <td className="px-3 py-2 border">{row.date}</td>
                    <td className="px-3 py-2 border">{row.total_orders}</td>
                    <td className="px-3 py-2 border">
                      {row.total_revenue.toFixed(2)}
                    </td>
                    <td className="px-3 py-2 border">{row.total_items}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* Top Products */}
      <section className="space-y-4">
        <div className="flex flex-wrap items-center gap-4">
          <h2 className="text-xl font-semibold">Top Products</h2>
          <label className="text-sm">
            Date:
            <input
              type="date"
              className="ml-2 border rounded px-2 py-1"
              value={targetDate}
              onChange={(e) => setTargetDate(e.target.value)}
            />
          </label>
        </div>

        <div className="overflow-x-auto border rounded">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-3 py-2 border">Product ID</th>
                <th className="px-3 py-2 border">Name</th>
                <th className="px-3 py-2 border">Total Quantity</th>
                <th className="px-3 py-2 border">Revenue</th>
              </tr>
            </thead>
            <tbody>
              {topProducts.length === 0 ? (
                <tr>
                  <td className="px-3 py-2 border text-center" colSpan={4}>
                    No data
                  </td>
                </tr>
              ) : (
                topProducts.map((row) => (
                  <tr key={`${row.product_id}-${row.product_name}`}>
                    <td className="px-3 py-2 border">{row.product_id}</td>
                    <td className="px-3 py-2 border">{row.product_name}</td>
                    <td className="px-3 py-2 border">{row.total_quantity}</td>
                    <td className="px-3 py-2 border">
                      {row.revenue.toFixed(2)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};