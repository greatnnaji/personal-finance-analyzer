import React, { useState } from 'react';
import './TransactionList.css';

const TransactionList = ({ transactions }) => {
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-CA', {
      style: 'currency',
      currency: 'CAD'
    }).format(amount);
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-CA');
  };

  // Filter transactions
  const filteredTransactions = transactions.filter(transaction => {
    if (filter === 'all') return true;
    if (filter === 'income') return transaction.amount > 0;
    if (filter === 'expenses') return transaction.amount < 0;
    return transaction.category === filter;
  });

  // Sort transactions
  const sortedTransactions = [...filteredTransactions].sort((a, b) => {
    if (sortBy === 'date') {
      return new Date(b.date) - new Date(a.date);
    }
    if (sortBy === 'amount') {
      return Math.abs(b.amount) - Math.abs(a.amount);
    }
    return 0;
  });

  // Get unique categories for filter
  const categories = [...new Set(transactions.map(t => t.category))];

  return (
    <div className="transaction-list">
      <div className="transaction-controls">
        <div className="filter-controls">
          <label>Filter:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Transactions</option>
            <option value="income">Income Only</option>
            <option value="expenses">Expenses Only</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>

        <div className="sort-controls">
          <label>Sort by:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="date">Date</option>
            <option value="amount">Amount</option>
          </select>
        </div>
      </div>

      <div className="transaction-table">
        <div className="transaction-header">
          <div>Date</div>
          <div>Description</div>
          <div>Category</div>
          <div>Amount</div>
        </div>

        <div className="transaction-body">
          {sortedTransactions.slice(0, 50).map((transaction, index) => (
            <div key={index} className="transaction-row">
              <div className="transaction-date">
                {formatDate(transaction.date)}
              </div>
              <div className="transaction-description">
                {transaction.description}
              </div>
              <div className="transaction-category">
                <span className="category-tag">{transaction.category}</span>
              </div>
              <div className={`transaction-amount ${transaction.amount >= 0 ? 'positive' : 'negative'}`}>
                {formatCurrency(transaction.amount)}
              </div>
            </div>
          ))}
        </div>

        {sortedTransactions.length > 50 && (
          <div className="transaction-footer">
            Showing first 50 of {sortedTransactions.length} transactions
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionList;