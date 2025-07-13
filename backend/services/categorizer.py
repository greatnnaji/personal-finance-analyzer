import re
from typing import List, Dict

class TransactionCategorizer:
    def __init__(self):
        # Define category patterns (case-insensitive)
        self.category_patterns = {
            'Food & Dining': [
                r'starbucks', r'mcdonald', r'subway', r'tim hortons', r'pizza',
                r'restaurant', r'cafe', r'coffee', r'uber eats', r'doordash',
                r'skip', r'food', r'dining', r'takeout', r'delivery'
            ],
            'Groceries': [
                r'grocery', r'supermarket', r'metro', r'loblaws', r'sobeys',
                r'walmart', r'costco', r'fresh', r'market', r'food basics'
            ],
            'Transportation': [
                r'gas', r'shell', r'esso', r'petro', r'uber', r'taxi',
                r'bus', r'transit', r'parking', r'car wash', r'automotive'
            ],
            'Entertainment': [
                r'netflix', r'spotify', r'amazon prime', r'disney', r'hulu',
                r'cinema', r'movie', r'theatre', r'gaming', r'steam'
            ],
            'Shopping': [
                r'amazon', r'walmart', r'target', r'shopping', r'store',
                r'purchase', r'retail', r'mall', r'clothing', r'electronics'
            ],
            'Utilities': [
                r'hydro', r'electric', r'gas bill', r'water', r'internet',
                r'phone', r'cable', r'utility', r'heating', r'cooling'
            ],
            'Healthcare': [
                r'pharmacy', r'doctor', r'medical', r'dental', r'hospital',
                r'clinic', r'health', r'medicine', r'prescription'
            ],
            'Banking': [
                r'atm', r'withdrawal', r'bank', r'fee', r'charge',
                r'transfer', r'interest', r'service charge'
            ],
            'Income': [
                r'payroll', r'salary', r'deposit', r'income', r'wages',
                r'pay', r'transfer received', r'refund'
            ]
        }
    
    def categorize_transaction(self, transaction: Dict) -> Dict:
        """Categorize a single transaction"""
        description = transaction.get('description', '').lower()
        trans_type = transaction.get('type', '')
        
        # Income transactions
        if trans_type == 'Credit':
            for pattern in self.category_patterns['Income']:
                if re.search(pattern, description):
                    transaction['category'] = 'Income'
                    return transaction
            transaction['category'] = 'Other Income'
            return transaction
        
        # Expense transactions
        for category, patterns in self.category_patterns.items():
            if category == 'Income':  # Skip income patterns for debits
                continue
            
            for pattern in patterns:
                if re.search(pattern, description):
                    transaction['category'] = category
                    return transaction
        
        # Default category for unmatched transactions
        transaction['category'] = 'Other'
        return transaction
    
    def categorize_batch(self, transactions: List[Dict]) -> List[Dict]:
        """Categorize a list of transactions"""
        return [self.categorize_transaction(transaction.copy()) for transaction in transactions]
