import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setError(null);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setAnalysisData(null);
  };

  const handleReset = () => {
    setAnalysisData(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Personal Finance Analyzer</h1>
        <p>Upload your transaction data to get insights into your spending patterns</p>
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            <h3>Error:</h3>
            <p>{error}</p>
            <button onClick={handleReset}>Try Again</button>
          </div>
        )}

        {!analysisData ? (
          <FileUpload 
            onAnalysisComplete={handleAnalysisComplete}
            onError={handleError}
            loading={loading}
            setLoading={setLoading}
          />
        ) : (
          <Dashboard 
            data={analysisData}
            onReset={handleReset}
          />
        )}
      </main>
    </div>
  );
}

export default App;