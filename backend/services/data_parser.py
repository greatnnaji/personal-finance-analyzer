import pandas as pd
from datetime import datetime
from utils.validators import DataValidator

class DataParser:
    def __init__(self):
        self.validator = DataValidator()
        
        # Expected column names (case-insensitive)
        self.required_columns = ['date', 'description', 'amount', 'type']
    
    def parse_file(self, file_path):
        """Parse uploaded file and return standardized transaction list"""
        try:
            # Read file
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Validate format
            self._validate_format(df)
            
            # Clean column names
            df.columns = df.columns.str.lower().str.strip()
            
            # Parse and validate data
            transactions = []
            for index, row in df.iterrows():
                try:
                    transaction = self._parse_row(row, index + 1)
                    if transaction:
                        transactions.append(transaction)
                except Exception as e:
                    print(f"Warning: Skipping row {index + 1}: {str(e)}")
            
            if not transactions:
                raise Exception("No valid transactions found in file")
            
            print(f"Parsed {len(transactions)} transactions successfully")
            return transactions
            
        except Exception as e:
            raise Exception(f"Error parsing file: {str(e)}")
    
    def _validate_format(self, df):
        print( "Validating file format...")
        """Validate that file has expected format"""
        if df.empty:
            raise Exception("File is empty")
        
        # Check columns (case-insensitive)
        df_columns = [col.lower().strip() for col in df.columns]
        missing_columns = [col for col in self.required_columns if col not in df_columns]
        
        if missing_columns:
            raise Exception(f"Missing required columns: {', '.join(missing_columns)}. "
                          f"Expected format: Date,Description,Amount,Type")
    
    def _parse_row(self, row, row_number):
        """Parse individual row into standardized transaction"""
        # Extract and validate data
        date = self._parse_date(row['date'], row_number)
        description = self._parse_description(row['description'], row_number)
        amount = self._parse_amount(row['amount'], row_number)
        trans_type = self._parse_type(row['type'], row_number)
        
        # Create standardized transaction
        transaction = {
            'date': date.isoformat(),
            'description': description,
            'amount': amount,
            'type': trans_type,
            'category': 'Uncategorized',  # Will be categorized later
            'original_data': row.to_dict()
        }
        
        return transaction
    
    def _parse_date(self, date_value, row_number):
        """Parse date in YYYY-MM-DD format"""
        if pd.isna(date_value):
            raise Exception(f"Row {row_number}: Date is empty")
        
        date_str = str(date_value).strip()
        
        try:
            # Expect YYYY-MM-DD format
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise Exception(f"Row {row_number}: Invalid date format '{date_str}'. Expected YYYY-MM-DD")
    
    def _parse_description(self, description_value, row_number):
        """Parse and validate description"""
        if pd.isna(description_value):
            raise Exception(f"Row {row_number}: Description is empty")
        
        description = str(description_value).strip()
        if not description:
            raise Exception(f"Row {row_number}: Description is empty")
        
        return description
    
    def _parse_amount(self, amount_value, row_number):
        """Parse and validate amount"""
        if pd.isna(amount_value):
            raise Exception(f"Row {row_number}: Amount is empty")
        
        try:
            amount = float(amount_value)
            return amount
        except (ValueError, TypeError):
            raise Exception(f"Row {row_number}: Invalid amount '{amount_value}'. Must be a number")
    
    def _parse_type(self, type_value, row_number):
        """Parse and validate transaction type"""
        if pd.isna(type_value):
            raise Exception(f"Row {row_number}: Type is empty")
        
        trans_type = str(type_value).strip().title()  # Convert to Title Case
        
        if trans_type not in ['Debit', 'Credit']:
            raise Exception(f"Row {row_number}: Invalid type '{trans_type}'. Must be 'Debit' or 'Credit'")
        
        return trans_type
