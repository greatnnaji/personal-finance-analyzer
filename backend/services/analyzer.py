import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any
import calendar

class DataAnalyzer:
    def analyze_transactions(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Perform comprehensive analysis on transactions"""
        if not transactions:
            return {}
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        analysis = {
            'summary': self._get_summary_stats(df),
            'by_category': self._analyze_by_category(df),
            'by_month': self._analyze_by_month(df),
            'spending_trends': self._analyze_spending_trends(df),
            'top_expenses': self._get_top_expenses(df),
            'income_vs_expenses': self._analyze_income_vs_expenses(df),
            'spending_patterns': self._analyze_spending_patterns(df)
        }

        # percentage_of_total error -- fix
        analysis['ai_insights'] = self._generate_ai_insights(df, analysis)

        return analysis
    
    def _get_summary_stats(self, df: pd.DataFrame) -> Dict:
        print( "Calculating summary statistics...")
        """Calculate basic summary statistics"""
        total_income = df[df['amount'] > 0]['amount'].sum()
        total_expenses = abs(df[df['amount'] < 0]['amount'].sum())
        net_income = total_income - total_expenses
        
        return {
            'total_transactions': len(df),
            'total_income': round(total_income, 2),
            'total_expenses': round(total_expenses, 2),
            'net_income': round(net_income, 2),
            'average_transaction': round(df['amount'].mean(), 2),
            'date_range': {
                'start': df['date'].min().isoformat(),
                'end': df['date'].max().isoformat()
            }
        }
    
    def _analyze_by_category(self, df: pd.DataFrame) -> Dict:
        print( "Analyzing spending by category...")
        """Analyze spending by category"""
        # Separate income and expenses
        expenses_df = df[df['amount'] < 0].copy()
        income_df = df[df['amount'] > 0].copy()
        
        # Expenses by category
        expense_by_category = expenses_df.groupby('category')['amount'].sum().abs()
        expense_counts = expenses_df.groupby('category').size()
        
        # Income by category
        income_by_category = income_df.groupby('category')['amount'].sum()
        income_counts = income_df.groupby('category').size()

        # Calculate total expenses for percentage calculation
        total_expenses = expense_by_category.sum()
        
        categories = {}

        # Process expense categories
        for category in expense_by_category.index:
            total_spent = expense_by_category[category]
            # Ensure values are not NaN before calculations
            total_spent = 0 if pd.isna(total_spent) else total_spent
            count = expense_counts[category]
            percentage = (total_spent / total_expenses * 100) if total_expenses > 0 else 0
            avg = total_spent / count if count > 0 else 0
            
            categories[category] = {
                'total_spent': round(total_spent, 2),
                'transaction_count': int(count),
                'average_per_transaction': round(avg, 2),
                'percentage_of_total': round(percentage, 1),
                'type': 'expense'
            }
        
        # Process income categories
        for category in income_by_category.index:
            total_earned = income_by_category[category]
            # Ensure values are not NaN before rounding
            total_earned = 0 if pd.isna(total_earned) else total_earned
            count = income_counts[category]
            avg = total_earned / count if count > 0 else 0
            
            categories[category] = {
                'total_earned': round(total_earned, 2),
                'transaction_count': int(count),
                'average_per_transaction': round(avg, 2),
                'percentage_of_total': 0,  # Income doesn't count towards expense percentage
                'type': 'income'
            }
        
        return categories
    
    def _analyze_by_month(self, df: pd.DataFrame) -> Dict:
        print( "Analyzing spending by month...")
        """Analyze spending by month"""
        df['month'] = df['date'].dt.to_period('M')
        
        monthly_data = {}
        for month in df['month'].unique():
            month_df = df[df['month'] == month]
            
            total_income = month_df[month_df['amount'] > 0]['amount'].sum()
            total_expenses = abs(month_df[month_df['amount'] < 0]['amount'].sum())
            
            monthly_data[str(month)] = {
                'total_income': round(total_income, 2),
                'total_expenses': round(total_expenses, 2),
                'net_income': round(total_income - total_expenses, 2),
                'transaction_count': len(month_df)
            }
        
        return monthly_data
    
    def _analyze_spending_trends(self, df: pd.DataFrame) -> Dict:
        print( "Analyzing spending trends over time...")
        """Analyze spending trends over time"""
        expenses_df = df[df['amount'] < 0].copy()
        
        if expenses_df.empty:
            return {}
        
        # Daily spending
        daily_spending = expenses_df.groupby(expenses_df['date'].dt.date)['amount'].sum().abs()
        
        # Weekly spending
        weekly_spending = expenses_df.groupby(expenses_df['date'].dt.isocalendar().week)['amount'].sum().abs()
        
        return {
            'daily_average': round(daily_spending.mean(), 2),
            'highest_spending_day': {
                'date': str(daily_spending.idxmax()),
                'amount': round(daily_spending.max(), 2)
            },
            'lowest_spending_day': {
                'date': str(daily_spending.idxmin()),
                'amount': round(daily_spending.min(), 2)
            },
            'weekly_average': round(weekly_spending.mean(), 2)
        }
    
    def _get_top_expenses(self, df: pd.DataFrame, limit: int = 10) -> List[Dict]:
        print(  "Getting top individual expenses...")
        """Get top individual expenses"""
        expenses_df = df[df['amount'] < 0].copy()
        top_expenses = expenses_df.nlargest(limit, 'amount', keep='first')
        
        return [
            {
                'date': row['date'].isoformat(),
                'description': row['description'],
                'amount': abs(round(row['amount'], 2)),
                'category': row['category']
            }
            for _, row in top_expenses.iterrows()
        ]
    
    def _analyze_income_vs_expenses(self, df: pd.DataFrame) -> Dict:
        print( "Comparing income vs expenses...")
        """Compare income vs expenses"""
        income_transactions = df[df['amount'] > 0]
        expense_transactions = df[df['amount'] < 0]
        
        return {
            'income_transaction_count': len(income_transactions),
            'expense_transaction_count': len(expense_transactions),
            'average_income_per_transaction': round(income_transactions['amount'].mean(), 2) if not income_transactions.empty else 0,
            'average_expense_per_transaction': round(abs(expense_transactions['amount'].mean()), 2) if not expense_transactions.empty else 0,
            'income_to_expense_ratio': round(
                income_transactions['amount'].sum() / abs(expense_transactions['amount'].sum()), 2
            ) if not expense_transactions.empty else 0
        }
    
    def _analyze_spending_patterns(self, df):
        """Analyze spending patterns and habits"""
        patterns = {}
        
        # Day of week analysis
        df['day_of_week'] = df['date'].dt.day_name()
        spending_by_day = df[df['amount'] < 0].groupby('day_of_week')['amount'].sum().abs()
        patterns['spending_by_day'] = spending_by_day.to_dict()
        
        # Average daily spending
        date_range = (df['date'].max() - df['date'].min()).days
        if date_range > 0:
            patterns['average_daily_spending'] = float(abs(df[df['amount'] < 0]['amount'].sum()) / date_range)
        
        return patterns
    
    def _generate_ai_insights(self, df, analysis):
        """Generate AI-powered insights and alerts"""
        print( "Generating AI insights...")
        insights = []
        
        # 1. Spending Anomaly Detection
        insights.extend(self._detect_spending_anomalies(df, analysis))
        
        # 2. Budget Predictions
        insights.extend(self._predict_budget_risks(df, analysis))
        
        # 3. Savings Opportunities
        insights.extend(self._identify_savings_opportunities(df, analysis))
        
        # 4. Spending Habits Analysis
        insights.extend(self._analyze_spending_habits(df, analysis))
        
        # 5. Financial Health Assessment
        insights.extend(self._assess_financial_health(df, analysis))
        
        return insights
    
    def _detect_spending_anomalies(self, df, analysis):
        """Detect unusual spending patterns"""
        insights = []
        
        # Compare recent month vs previous months
        monthly_data = analysis['by_month']
        if len(monthly_data) >= 2:
            months = sorted(monthly_data.keys())
            current_month = months[-1]
            previous_months = months[-3:-1] if len(months) >= 3 else months[:-1]
            
            current_spending = abs(monthly_data[current_month]['total_expenses'])
            avg_previous_spending = np.mean([abs(monthly_data[month]['total_expenses']) for month in previous_months])
            
            if avg_previous_spending > 0:
                change_percent = ((current_spending - avg_previous_spending) / avg_previous_spending) * 100
                
                if change_percent > 25:
                    insights.append({
                        'type': 'spending_spike',
                        'severity': 'high' if change_percent > 50 else 'medium',
                        'title': 'Unusual Spending Detected',
                        'message': f'Your spending increased by {change_percent:.0f}% this month compared to your average.',
                        'amount': current_spending - avg_previous_spending,
                        'recommendation': 'Review your recent transactions to identify the cause of increased spending.'
                    })
                elif change_percent < -25:
                    insights.append({
                        'type': 'spending_decrease',
                        'severity': 'positive',
                        'title': 'Great Spending Control!',
                        'message': f'Your spending decreased by {abs(change_percent):.0f}% this month.',
                        'amount': avg_previous_spending - current_spending,
                        'recommendation': 'Consider putting the saved money into your emergency fund or investments.'
                    })
        
        # Category-specific anomalies
        for category, data in analysis['by_category'].items():
            if data['percentage_of_total'] > 40:
                insights.append({
                    'type': 'category_dominance',
                    'severity': 'medium',
                    'title': f'High {category} Spending',
                    'message': f'{category} represents {data["percentage_of_total"]:.0f}% of your total spending.',
                    'amount': data['total_spent'],
                    'recommendation': f'Consider ways to reduce {category} expenses or create a specific budget for this category.'
                })
        
        return insights
    
    def _predict_budget_risks(self, df, analysis):
        """Predict potential budget overruns"""
        insights = []
        
        # Simple prediction based on current month's trend
        current_month = datetime.now().replace(day=1)
        current_month_data = df[df['date'] >= current_month]
        
        if len(current_month_data) > 0:
            days_elapsed = (datetime.now() - current_month).days
            days_in_month = calendar.monthrange(current_month.year, current_month.month)[1]
            
            if days_elapsed > 0 and days_elapsed < days_in_month:
                current_spending = abs(current_month_data[current_month_data['amount'] < 0]['amount'].sum())
                projected_spending = (current_spending / days_elapsed) * days_in_month
                
                # Compare with average monthly spending
                monthly_data = analysis['by_month']
                if len(monthly_data) >= 2:
                    avg_monthly_spending = np.mean([abs(data['total_expenses']) for data in monthly_data.values()])
                    
                    if projected_spending > avg_monthly_spending * 1.2:
                        insights.append({
                            'type': 'budget_risk',
                            'severity': 'high',
                            'title': 'Budget Overrun Risk',
                            'message': f'Based on current spending, you may exceed your average monthly budget by ${projected_spending - avg_monthly_spending:.2f}.',
                            'amount': projected_spending - avg_monthly_spending,
                            'recommendation': 'Consider reducing discretionary spending for the remainder of the month.'
                        })
        
        return insights
    
    def _identify_savings_opportunities(self, df, analysis):
        """Identify potential savings opportunities"""
        insights = []
        
        # Look for frequent small transactions that add up
        small_transactions = df[(df['amount'] < 0) & (df['amount'] > -20)].copy()
        if len(small_transactions) > 0:
            small_tx_by_category = small_transactions.groupby('category')['amount'].agg(['sum', 'count']).reset_index()
            small_tx_by_category['total_spent'] = abs(small_tx_by_category['sum'])
            
            for _, row in small_tx_by_category.iterrows():
                if row['count'] >= 5 and row['total_spent'] >= 50:
                    insights.append({
                        'type': 'savings_opportunity',
                        'severity': 'medium',
                        'title': f'Small {row["category"]} Purchases Add Up',
                        'message': f'{row["count"]} small {row["category"]} purchases totaled ${row["total_spent"]:.2f}.',
                        'amount': row['total_spent'],
                        'recommendation': f'Consider bulk purchasing or setting a weekly limit for {row["category"]} expenses.'
                    })
        
        return insights
    
    def _analyze_spending_habits(self, df, analysis):
        """Analyze spending habits and patterns"""
        insights = []
        
        # Weekend vs weekday spending
        df['is_weekend'] = df['date'].dt.weekday >= 5
        weekend_spending = abs(df[(df['amount'] < 0) & (df['is_weekend'])]['amount'].sum())
        weekday_spending = abs(df[(df['amount'] < 0) & (~df['is_weekend'])]['amount'].sum())
        
        if weekend_spending > 0 and weekday_spending > 0:
            weekend_ratio = weekend_spending / (weekend_spending + weekday_spending)
            
            if weekend_ratio > 0.4:  # More than 40% spent on weekends
                insights.append({
                    'type': 'spending_pattern',
                    'severity': 'info',
                    'title': 'Weekend Spending Pattern',
                    'message': f'{weekend_ratio*100:.0f}% of your spending happens on weekends.',
                    'amount': weekend_spending,
                    'recommendation': 'Consider setting a weekend spending limit to better control your budget.'
                })
        
        return insights
    
    def _assess_financial_health(self, df, analysis):
        """Assess overall financial health"""
        insights = []
        
        # Income vs Expenses ratio
        total_income = analysis['summary']['total_income']
        total_expenses = abs(analysis['summary']['total_expenses'])
        
        if total_income > 0:
            savings_rate = (total_income - total_expenses) / total_income
            
            if savings_rate < 0:
                insights.append({
                    'type': 'financial_health',
                    'severity': 'high',
                    'title': 'Spending Exceeds Income',
                    'message': f'You spent ${total_expenses - total_income:.2f} more than you earned.',
                    'amount': total_expenses - total_income,
                    'recommendation': 'Immediate action needed: reduce expenses or increase income to avoid debt.'
                })
            elif savings_rate < 0.1:
                insights.append({
                    'type': 'financial_health',
                    'severity': 'medium',
                    'title': 'Low Savings Rate',
                    'message': f'You\'re only saving {savings_rate*100:.1f}% of your income.',
                    'amount': total_income * 0.2 - (total_income - total_expenses),
                    'recommendation': 'Financial experts recommend saving at least 20% of income. Consider reducing expenses.'
                })
            elif savings_rate >= 0.2:
                insights.append({
                    'type': 'financial_health',
                    'severity': 'positive',
                    'title': 'Excellent Savings Rate!',
                    'message': f'You\'re saving {savings_rate*100:.1f}% of your income.',
                    'amount': total_income - total_expenses,
                    'recommendation': 'Great job! Consider investing your savings for long-term growth.'
                })
        
        return insights