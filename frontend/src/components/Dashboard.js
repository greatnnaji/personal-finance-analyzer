import React from 'react';
import TransactionList from './TransactionList';
import Charts from './Charts';
import SummaryCards from './SummaryCards';
import AIInsights from './AIInsights'; 
import './Dashboard.css';

const Dashboard = ({ data, onReset }) => {
  const { transactions, analysis } = data;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Financial Analysis Results</h2>
        <button onClick={onReset} className="reset-button">
          Upload New File
        </button>
      </div>

      <SummaryCards analysis={analysis} />

      <AIInsights insights={analysis.ai_insights} />

       <Charts analysis={analysis} />
      
      <div className="dashboard-content">
        <div className="transactions-section">
          <h3>Recent Transactions ({transactions.length} total)</h3>
          <TransactionList transactions={transactions} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;