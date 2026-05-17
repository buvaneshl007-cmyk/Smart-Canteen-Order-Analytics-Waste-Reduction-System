import React, { useState, useEffect } from 'react';
import { analyticsService } from '../../services/api';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import {
  TrendingUp,
  DollarSign,
  ShoppingBag,
  Clock,
  CalendarDays,
  BarChart3,
} from 'lucide-react';
import toast from 'react-hot-toast';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const OwnerDashboard = () => {
  const [dailySales, setDailySales] = useState([]);
  const [monthlyDailySales, setMonthlyDailySales] = useState([]);
  const [quarterlyDailySales, setQuarterlyDailySales] = useState([]);
  const [weeklySales, setWeeklySales] = useState([]);
  const [hourlySales, setHourlySales] = useState([]);
  const [itemAnalytics, setItemAnalytics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [daily, monthlyDaily, quarterlyDaily, weekly, hourly, items] = await Promise.all([
        analyticsService.getDailySales(7),
        analyticsService.getDailySales(30),
        analyticsService.getDailySales(90),
        analyticsService.getWeeklySales(),
        analyticsService.getHourlySales(),
        analyticsService.getItemAnalytics(),
      ]);

      setDailySales(daily.data);
      setMonthlyDailySales(monthlyDaily.data);
      setQuarterlyDailySales(quarterlyDaily.data);
      setWeeklySales(weekly.data);
      setHourlySales(hourly.data);
      setItemAnalytics(items.data);
    } catch (error) {
      toast.error('Failed to fetch analytics');
    } finally {
      setLoading(false);
    }
  };

  // Calculate summary stats
  const totalRevenue = dailySales.reduce((sum, day) => sum + day.total_revenue, 0);
  const totalOrders = dailySales.reduce((sum, day) => sum + day.total_orders, 0);
  const avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;
  const monthlyRevenue = monthlyDailySales.reduce((sum, day) => sum + day.total_revenue, 0);
  const monthlyOrders = monthlyDailySales.reduce((sum, day) => sum + day.total_orders, 0);

  const bestWeekday = weeklySales.length > 0
    ? weeklySales.reduce((max, day) => (day.total_revenue > max.total_revenue ? day : max), weeklySales[0])
    : null;

  const getWeekStartKey = (dateValue) => {
    const date = new Date(dateValue);
    const day = date.getDay();
    const diff = (day + 6) % 7;
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - diff);
    return weekStart.toISOString().split('T')[0];
  };

  const weeklyBuckets = monthlyDailySales.reduce((acc, day) => {
    const key = getWeekStartKey(day.date);
    if (!acc[key]) {
      acc[key] = { week: key, revenue: 0, orders: 0, items: 0 };
    }
    acc[key].revenue += day.total_revenue;
    acc[key].orders += day.total_orders;
    acc[key].items += day.items_sold;
    return acc;
  }, {});

  const weeklyTrendData = Object.values(weeklyBuckets)
    .sort((a, b) => new Date(a.week) - new Date(b.week))
    .slice(-6);

  const monthlyBuckets = quarterlyDailySales.reduce((acc, day) => {
    const date = new Date(day.date);
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    if (!acc[key]) {
      acc[key] = {
        monthKey: key,
        monthLabel: date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }),
        revenue: 0,
        orders: 0,
      };
    }
    acc[key].revenue += day.total_revenue;
    acc[key].orders += day.total_orders;
    return acc;
  }, {});

  const monthlyComparisonData = Object.values(monthlyBuckets)
    .sort((a, b) => new Date(`${a.monthKey}-01`) - new Date(`${b.monthKey}-01`))
    .slice(-4);

  const cumulativeMonthlyRevenue = [];
  monthlyDailySales.reduce((running, day) => {
    const nextTotal = running + day.total_revenue;
    cumulativeMonthlyRevenue.push(nextTotal);
    return nextTotal;
  }, 0);

  // Chart configurations
  const dailySalesChart = {
    labels: dailySales.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
    datasets: [
      {
        label: 'Revenue (₹)',
        data: dailySales.map(d => d.total_revenue),
        borderColor: 'rgb(245, 158, 11)',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const weeklySalesChart = {
    labels: weeklySales.map(d => d.day_of_week),
    datasets: [
      {
        label: 'Revenue (₹)',
        data: weeklySales.map(d => d.total_revenue),
        backgroundColor: 'rgba(245, 158, 11, 0.8)',
      },
    ],
  };

  const weekdayOrdersChart = {
    labels: weeklySales.map(d => d.day_of_week),
    datasets: [
      {
        label: 'Orders',
        data: weeklySales.map(d => d.total_orders),
        backgroundColor: 'rgba(59, 130, 246, 0.85)',
      },
    ],
  };

  const topItemsChart = {
    labels: itemAnalytics.slice(0, 5).map(i => i.item_name),
    datasets: [
      {
        label: 'Quantity Sold',
        data: itemAnalytics.slice(0, 5).map(i => i.total_quantity),
        backgroundColor: [
          'rgba(245, 158, 11, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(139, 92, 246, 0.8)',
        ],
      },
    ],
  };

  const hourlySalesChart = {
    labels: hourlySales.map(h => `${h.hour}:00`),
    datasets: [
      {
        label: 'Orders',
        data: hourlySales.map(h => h.total_orders),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const hourlyRevenueChart = {
    labels: hourlySales.map(h => `${h.hour}:00`),
    datasets: [
      {
        label: 'Revenue (₹)',
        data: hourlySales.map(h => h.total_revenue),
        backgroundColor: 'rgba(16, 185, 129, 0.75)',
      },
    ],
  };

  const dailyOrdersItemsChart = {
    labels: dailySales.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
    datasets: [
      {
        label: 'Orders',
        data: dailySales.map(d => d.total_orders),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.15)',
        tension: 0.35,
      },
      {
        label: 'Items Sold',
        data: dailySales.map(d => d.items_sold),
        borderColor: 'rgb(245, 158, 11)',
        backgroundColor: 'rgba(245, 158, 11, 0.15)',
        tension: 0.35,
      },
    ],
  };

  const monthlyTrendChart = {
    labels: monthlyDailySales.map(d =>
      new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    ),
    datasets: [
      {
        label: 'Revenue (₹)',
        data: monthlyDailySales.map(d => d.total_revenue),
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.12)',
        fill: true,
        tension: 0.3,
      },
    ],
  };

  const cumulativeRevenueChart = {
    labels: monthlyDailySales.map(d =>
      new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    ),
    datasets: [
      {
        label: 'Cumulative Revenue (₹)',
        data: cumulativeMonthlyRevenue,
        borderColor: 'rgb(99, 102, 241)',
        backgroundColor: 'rgba(99, 102, 241, 0.15)',
        fill: true,
        tension: 0.25,
      },
    ],
  };

  const weeklyTrendChart = {
    labels: weeklyTrendData.map(w =>
      `Week of ${new Date(w.week).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
    ),
    datasets: [
      {
        label: 'Revenue (₹)',
        data: weeklyTrendData.map(w => w.revenue),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
      },
      {
        label: 'Orders',
        data: weeklyTrendData.map(w => w.orders),
        backgroundColor: 'rgba(245, 158, 11, 0.8)',
      },
    ],
  };

  const monthWiseComparisonChart = {
    labels: monthlyComparisonData.map(m => m.monthLabel),
    datasets: [
      {
        type: 'bar',
        label: 'Revenue (₹)',
        data: monthlyComparisonData.map(m => m.revenue),
        backgroundColor: 'rgba(139, 92, 246, 0.8)',
      },
      {
        type: 'line',
        label: 'Orders',
        data: monthlyComparisonData.map(m => m.orders),
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.2)',
        tension: 0.3,
      },
    ],
  };

  const topItemsRevenueChart = {
    labels: itemAnalytics.slice(0, 10).map(i => i.item_name),
    datasets: [
      {
        label: 'Revenue (₹)',
        data: itemAnalytics.slice(0, 10).map(i => i.total_revenue),
        backgroundColor: 'rgba(236, 72, 153, 0.75)',
      },
    ],
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Analytics Dashboard</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-primary-500 to-primary-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100 text-sm mb-1">Total Revenue</p>
              <p className="text-2xl font-bold">₹{totalRevenue.toFixed(2)}</p>
            </div>
            <DollarSign className="h-12 w-12 text-primary-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm mb-1">Total Orders</p>
              <p className="text-2xl font-bold">{totalOrders}</p>
            </div>
            <ShoppingBag className="h-12 w-12 text-blue-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm mb-1">Avg Order Value</p>
              <p className="text-2xl font-bold">₹{avgOrderValue.toFixed(2)}</p>
            </div>
            <TrendingUp className="h-12 w-12 text-green-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm mb-1">Peak Hour</p>
              <p className="text-2xl font-bold">
                {hourlySales.length > 0
                  ? `${hourlySales.reduce((max, h) => h.total_orders > max.total_orders ? h : max).hour}:00`
                  : 'N/A'}
              </p>
            </div>
            <Clock className="h-12 w-12 text-purple-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-emerald-500 to-emerald-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-emerald-100 text-sm mb-1">Revenue (30 Days)</p>
              <p className="text-2xl font-bold">₹{monthlyRevenue.toFixed(2)}</p>
            </div>
            <CalendarDays className="h-12 w-12 text-emerald-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-indigo-500 to-indigo-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-indigo-100 text-sm mb-1">Best Weekday</p>
              <p className="text-2xl font-bold">{bestWeekday ? bestWeekday.day_of_week : 'N/A'}</p>
              <p className="text-xs text-indigo-100 mt-1">{monthlyOrders} orders in 30 days</p>
            </div>
            <BarChart3 className="h-12 w-12 text-indigo-200" />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Sales Trend */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Daily Sales (Last 7 Days)</h2>
          <Line data={dailySalesChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        {/* Weekly Sales */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Sales by Day of Week</h2>
          <Bar data={weeklySalesChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">Orders by Day of Week</h2>
          <Bar data={weekdayOrdersChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        {/* Top Items */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Top 5 Items</h2>
          <Pie data={topItemsChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        {/* Hourly Sales */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Hourly Sales Pattern</h2>
          <Line data={hourlySalesChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">Hourly Revenue Pattern</h2>
          <Bar data={hourlyRevenueChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card lg:col-span-2">
          <h2 className="text-xl font-bold mb-4">Daily Orders vs Items Sold (Last 7 Days)</h2>
          <Line data={dailyOrdersItemsChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card lg:col-span-2">
          <h2 className="text-xl font-bold mb-4">Month-Wise Daily Revenue Trend (Last 30 Days)</h2>
          <Line data={monthlyTrendChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card lg:col-span-2">
          <h2 className="text-xl font-bold mb-4">Cumulative Revenue Growth (Last 30 Days)</h2>
          <Line data={cumulativeRevenueChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">Week-Wise Performance (Last 6 Weeks)</h2>
          <Bar data={weeklyTrendChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">Month-Wise Comparison (Revenue vs Orders)</h2>
          <Bar data={monthWiseComparisonChart} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        <div className="card lg:col-span-2">
          <h2 className="text-xl font-bold mb-4">Top 10 Items by Revenue</h2>
          <Bar
            data={topItemsRevenueChart}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              indexAxis: 'y',
            }}
          />
        </div>
      </div>

      {/* Top Items Table */}
      <div className="card mt-6">
        <h2 className="text-xl font-bold mb-4">Item Performance</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Item</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Quantity Sold</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Revenue</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Peak Hour</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {itemAnalytics.map(item => (
                <tr key={item.item_id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">{item.item_name}</td>
                  <td className="px-4 py-3 text-sm text-gray-700">{item.total_quantity}</td>
                  <td className="px-4 py-3 text-sm text-gray-700">₹{item.total_revenue.toFixed(2)}</td>
                  <td className="px-4 py-3 text-sm text-gray-700">{item.peak_hour}:00</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default OwnerDashboard;
