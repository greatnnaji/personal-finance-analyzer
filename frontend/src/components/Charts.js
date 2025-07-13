import React from 'react';
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, LineChart, Line, ResponsiveContainer
} from 'recharts';
import './Charts.css';

const Charts = ({ analysis }) => {
  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  // Prepare data for category pie chart
  const categoryData = Object.entries(analysis.by_category || {})
    .filter(([category, data]) => category !== "Income")
    .map(([category, data]) => ({
    name: category,
    value: Math.abs(data.total_spent),
    count: data.transaction_count
  }));

  // Prepare data for monthly spending chart
  const monthlyData = Object.entries(analysis.by_month || {}).map(([month, data]) => ({
    month: month,
    income: data.total_income,
    expenses: Math.abs(data.total_expenses),
    net: data.net_income
  }));

  // Prepare data for top expenses
  const topExpenses = (analysis.top_expenses || [])//.sort((a, b) => Math.abs(b.amount) - Math.abs(a.amount))
  .slice(0, 10).map(expense => ({
    description: expense.description.length > 20 
      ? expense.description.substring(0, 20) + '...' 
      : expense.description,
    amount: Math.abs(expense.amount),
    category: expense.category
  }));

  // Custom tooltip for pie chart
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <p className="label">{data.name}</p>
          <p className="value">${data.value.toFixed(2)}</p>
          <p className="count">{data.count} transactions</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="charts-container">
      <h2>Spending Insights</h2>
      
      <div className="charts-grid">
        {/* Category Breakdown Pie Chart */}
        <div className="chart-card">
          <h3>Spending by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Monthly Spending Trend */}
        <div className="chart-card">
          <h3>Monthly Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
              <Legend />
              <Bar dataKey="income" fill="#00C49F" name="Income" />
              <Bar dataKey="expenses" fill="#FF8042" name="Expenses" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Expenses */}
        <div className="chart-card">
          <h3>Top Expenses</h3>
          <ResponsiveContainer width="100%" height={500}>
            <BarChart data={topExpenses} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="description" type="category" width={200} />
            <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
            <Bar dataKey="amount" fill="#FF6F61" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Income vs Expenses Trend */}
        <div className="chart-card">
          <h3>Income vs Expenses Trend</h3>
          <ResponsiveContainer width="100%" height={500}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
              <Legend />
              <Line type="monotone" dataKey="income" stroke="#00C49F" strokeWidth={2} name="Income" />
              <Line type="monotone" dataKey="expenses" stroke="#FF8042" strokeWidth={2} name="Expenses" />
              <Line type="monotone" dataKey="net" stroke="#0088FE" strokeWidth={2} name="Net Income" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Charts;
