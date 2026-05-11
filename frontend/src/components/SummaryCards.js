import React from 'react';
import './SummaryCards.css';

const SummaryCards = ({ analysis }) => {
  const { summary, by_category } = analysis;

  // Get top spending categories
  const topCategories = Object.entries(by_category)
    .filter(([, data]) => data.type === 'expense') // Only show expenses
    .sort(([,a], [,b]) => (b.total_spent || 0) - (a.total_spent || 0))
    .slice(0, 3);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-CA', {
      style: 'currency',
      currency: 'CAD'
    }).format(amount);
  };

  return (
    <div className="summary-cards">
      <div className="summary-card income">
        <h4>Total Income</h4>
        <div className="amount positive">
          {formatCurrency(summary.total_income)}
        </div>
      </div>

      <div className="summary-card expenses">
        <h4>Total Expenses</h4>
        <div className="amount negative">
          {formatCurrency(Math.abs(summary.total_expenses))}
        </div>
      </div>

      <div className="summary-card net">
        <h4>Net Income</h4>
        <div className={`amount ${summary.net_income >= 0 ? 'positive' : 'negative'}`}>
          {formatCurrency(summary.net_income)}
        </div>
      </div>

      <div className="summary-card categories">
        <h4>Top Spending Categories</h4>
        <div className="category-list">
          {topCategories.map(([category, data]) => (
            <div key={category} className="category-item">
              <span className="category-name">{category}</span>
              <span className="category-amount">
                {formatCurrency(data.total_spent || 0)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SummaryCards;