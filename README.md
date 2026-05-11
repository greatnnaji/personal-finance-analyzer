# Personal Finance Analyzer

A full-stack web application that analyzes personal financial transactions and provides AI-powered insights for better financial decision-making.

## Features

- **Transaction Processing**: Upload CSV/Excel files with transaction data
- **Smart Categorization**: Automatically categorizes transactions using rule-based pattern matching
- **Advanced Analytics**: Spending trends, monthly analysis, and anomaly detection
- **AI Insights**: Personalized recommendations for budgeting and savings opportunities
- **Interactive Dashboard**: Visual charts and summary cards for comprehensive financial overview
- **Budget Risk Prediction**: Early warning system for potential budget overruns

## Tech Stack

**Backend:**
- Python 3.8+
- Flask (Web framework)
- Pandas (Data processing)
- NumPy (Statistical analysis)

**Frontend:**
- React.js
- CSS3
- Chart.js/Recharts (Data visualization)

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- Conda (recommended for environment management)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-finance-analyzer.git
   cd personal-finance-analyzer
   ```

2. **Create and activate conda environment**
   ```bash
   conda create --name personalFinanceAnalyzer python=3.8
   conda activate personalFinanceAnalyzer
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5050`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   mkdir frontend
   cd frontend
   ```

2. **Create React app**
   ```bash
   npx create-react-app .
   ```

3. **Install dependencies and start development server**
   ```bash
   npm install
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

## Usage

### File Format Requirements

Upload CSV or Excel files with the following columns:
- **Date**: YYYY-MM-DD format
- **Description**: Transaction description
- **Amount**: Transaction amount (positive for income, negative for expenses)
- **Type**: "Credit" or "Debit"

### Example CSV Format:
```csv
Date,Description,Amount,Type
2024-01-15,Starbucks Coffee,-4.50,Debit
2024-01-15,Salary Deposit,3000.00,Credit
2024-01-16,Grocery Store,-85.32,Debit
```

### Getting Started

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Upload your transaction file using the file upload interface
4. View your comprehensive financial analysis and AI-powered insights

## Project Structure

```
personal-finance-analyzer/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── services/
│   ├── analyzer.py       # Financial analysis logic
│   ├── categorizer.py    # Transaction categorization
│   ├── data_parser.py    # File parsing and validation
│   └── file_processor.py # File handling utilities
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js    # Main dashboard component
│   │   │   ├── Charts.js       # Data visualization
│   │   │   ├── SummaryCards.js # Financial summary cards
│   │   │   └── AIInsights.js   # AI recommendations
│   │   └── App.js
│   └── public/
└── data/
    └── uploads/          # Temporary file storage
```

## API Endpoints

- `POST /api/upload-and-analyze` - Upload file and get analysis results
- `GET /api/health` - Health check endpoint

## Features in Detail

### Transaction Categorization
- Automatic categorization using regex pattern matching
- Categories include: Food & Dining, Transportation, Utilities, Entertainment, etc.
- Customizable category rules

### AI Insights
- **Spending Anomaly Detection**: Identifies unusual spending patterns
- **Budget Risk Prediction**: Warns about potential budget overruns
- **Savings Opportunities**: Suggests areas for cost reduction
- **Financial Health Assessment**: Evaluates overall financial well-being

### Analytics Dashboard
- Monthly spending trends
- Category-wise expense breakdown
- Income vs. expenses comparison
- Top expense transactions
- Spending patterns by day of week

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Built with Flask and React
- Data processing powered by Pandas and NumPy
- Financial categorization based on common transaction patterns
