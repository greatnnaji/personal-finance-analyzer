import React from 'react';
import './AIInsights.css';

const AIInsights = ({ insights }) => {
  if (!insights || insights.length === 0) {
    return (
      <div className="ai-insights-container">
        <h2>🤖 AI Insights</h2>
        <p>No insights available. Upload more transaction data to get personalized recommendations!</p>
      </div>
    );
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'high': return '⚠️';
      case 'medium': return '💡';
      case 'positive': return '✅';
      case 'info': return 'ℹ️';
      default: return '💭';
    }
  };

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'high': return 'severity-high';
      case 'medium': return 'severity-medium';
      case 'positive': return 'severity-positive';
      case 'info': return 'severity-info';
      default: return 'severity-default';
    }
  };

  const groupInsightsByType = (insights) => {
    const grouped = {};
    insights.forEach(insight => {
      if (!grouped[insight.type]) {
        grouped[insight.type] = [];
      }
      grouped[insight.type].push(insight);
    });
    return grouped;
  };

  const typeLabels = {
    'spending_spike': 'Spending Alerts',
    'spending_decrease': 'Savings Wins',
    'category_dominance': 'Category Analysis',
    'budget_risk': 'Budget Predictions',
    'savings_opportunity': 'Savings Opportunities',
    'spending_pattern': 'Spending Habits',
    'financial_health': 'Financial Health'
  };

  const groupedInsights = groupInsightsByType(insights);

  return (
    <div className="ai-insights-container">
      <h2>🤖 AI-Powered Insights</h2>
      <div className="insights-grid">
        {Object.entries(groupedInsights).map(([type, typeInsights]) => (
          <div key={type} className="insight-group">
            <h3 className="insight-group-title">{typeLabels[type] || type}</h3>
            {typeInsights.map((insight, index) => (
              <div key={index} className={`insight-card ${getSeverityClass(insight.severity)}`}>
                <div className="insight-header">
                  <span className="insight-icon">{getSeverityIcon(insight.severity)}</span>
                  <h4 className="insight-title">{insight.title}</h4>
                  {insight.amount && (
                    <span className="insight-amount">${Math.abs(insight.amount).toFixed(2)}</span>
                  )}
                </div>
                <p className="insight-message">{insight.message}</p>
                {insight.recommendation && (
                  <div className="insight-recommendation">
                    <strong>💡 Recommendation:</strong> {insight.recommendation}
                  </div>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AIInsights;