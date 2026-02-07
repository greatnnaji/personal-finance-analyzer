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
  .slice(0, 10).map(expense => {
    const fullDescription = expense.description;
    let displayDescription = fullDescription;
    
    // Smart truncation: keep beginning and end for IDs, abbreviate common terms
    if (fullDescription.length > 25) {
      if (fullDescription.includes('E-TRANSFER')) {
        // For E-TRANSFER, keep the last digits of the ID
        const match = fullDescription.match(/E-TRANSFER\s+(\d+)/);
        if (match) {
          const id = match[1];
          displayDescription = `E-TRANS ...${id.slice(-4)}`;
        } else {
          displayDescription = fullDescription.substring(0, 25) + '...';
        }
      } else if (fullDescription.includes('INTERNET TRANSFER')) {
        const match = fullDescription.match(/INTERNET TRANSFER\s+(\w+)/);
        if (match) {
          const ref = match[1];
          displayDescription = `INT TRANS ...${ref.slice(-4)}`;
        } else {
          displayDescription = fullDescription.substring(0, 25) + '...';
        }
      } else if (fullDescription.includes('PREAUTHORIZED DEBIT')) {
        displayDescription = fullDescription.replace('PREAUTHORIZED DEBIT', 'PRE-AUTH').substring(0, 25);
      } else if (fullDescription.includes('SERVICE CHARGE')) {
        displayDescription = fullDescription.replace('SERVICE CHARGE', 'SVC CHG').substring(0, 25);
      } else {
        // Default: show first 25 chars
        displayDescription = fullDescription.substring(0, 25) + '...';
      }
    }
    
    return {
      description: displayDescription,
      fullDescription: fullDescription, // Store full text for tooltip
      amount: Math.abs(expense.amount),
      category: expense.category
    };
  });

  // Prepare data for spending patterns
  const spendingByDay = analysis.spending_patterns?.spending_by_day || {};
  const dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const spendingByDayData = dayOrder.map(day => ({
    day: day.substring(0, 3), // Short day names
    amount: Math.abs(spendingByDay[day] || 0)
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
            <Tooltip 
              formatter={(value, name, props) => {
                // Show full description and formatted amount
                return [`$${value.toFixed(2)}`, props.payload.fullDescription || props.payload.description];
              }}
            />
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

        {/* Spending by Day of Week */}
        <div className="chart-card">
          <h3>Spending by Day of Week</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={spendingByDayData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
              <Bar dataKey="amount" fill="#8884D8" name="Spending" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Charts;
