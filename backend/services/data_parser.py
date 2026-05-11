import pandas as pd
import pdfplumber
from datetime import datetime
from utils.validators import DataValidator

class DataParser:
    def __init__(self):
        self.validator = DataValidator()
        
        # Define possible header names for each field type
        self.header_patterns = {
            'date': [
                'date', 'transaction date'
            ],
            'description': [
                'description', 'transaction description', 'details', 'transaction details'
            ],
            'amount': [
                'amount', 'transaction amount'
            ],
            'debit': [
                'debit', 'withdrawal', 'withdrawals'
            ],
            'credit': [
                'credit', 'credits', 'deposit', 'deposits', 'credit amount', 'income'
            ],
            'balance': [
                'balance', 'current balance', 'available balance', 'account balance'
            ]
        }
    
    def parse_file(self, file_path):
        """Parse uploaded PDF file and return standardized transaction list"""
        try:
            print(f"Parsing PDF file: {file_path}")
            
            # Extract tables from PDF
            with pdfplumber.open(file_path) as pdf:
                all_transactions = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    print(f"Processing page {page_num}...")
                    tables = page.extract_tables()
                    print(tables)
                    
                    for table_num, table in enumerate(tables, 1):
                        if not table or len(table) < 2:  # Need at least header + 1 row
                            continue
                        
                        print(f"Found table {table_num} with {len(table)} rows on page {page_num}")
                        
                        # Convert table to DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        # Map columns to standard fields
                        column_mapping = self._identify_columns(df)
                        
                        if column_mapping:
                            transactions = self._parse_dataframe(df, column_mapping)
                            all_transactions.extend(transactions)
                            print(f"Extracted {len(transactions)} transactions from table {table_num}")
            
            if not all_transactions:
                raise Exception("No valid transactions found in PDF")
            
            print(f"Total parsed {len(all_transactions)} transactions successfully")
            return all_transactions
            
        except Exception as e:
            raise Exception(f"Error parsing PDF file: {str(e)}")
    
    def _identify_columns(self, df):
        """Identify which columns correspond to which fields"""
        if df.empty:
            return None
        
        # Clean column names
        df.columns = [str(col).lower().strip() if col else '' for col in df.columns]
        
        column_mapping = {}
        
        # Find matches for each field type
        for field, patterns in self.header_patterns.items():
            for col in df.columns:
                if any(pattern in col for pattern in patterns):
                    column_mapping[field] = col
                    break
        
        # Must have at least date and description
        if 'date' not in column_mapping or 'description' not in column_mapping:
            print(f"Warning: Could not identify required columns. Found: {column_mapping}")
            return None
        
        # Check if we have amount OR both debit/credit
        has_amount = 'amount' in column_mapping
        has_debit_credit = 'debit' in column_mapping and 'credit' in column_mapping
        
        if not has_amount and not has_debit_credit:
            print(f"Warning: No amount or debit/credit columns found")
            return None
        
        print(f"Identified columns: {column_mapping}")
        return column_mapping
    
    def _parse_dataframe(self, df, column_mapping):
        """Parse DataFrame using the identified column mapping"""
        transactions = []
        
        for index, row in df.iterrows():
            try:
                transaction = self._parse_row_with_mapping(row, index + 1, column_mapping)
                if transaction:
                    transactions.append(transaction)
            except Exception as e:
                print(f"Warning: Skipping row {index + 1}: {str(e)}")
        
        return transactions
    
    def _parse_row_with_mapping(self, row, row_number, column_mapping):
        """Parse individual row using column mapping"""
        # Extract date
        date = self._parse_date_flexible(row[column_mapping['date']], row_number)
        
        # Extract description
        description = self._parse_description(row[column_mapping['description']], row_number)
        
        # Extract amount and type
        if 'amount' in column_mapping:
            # Single amount column
            amount = self._parse_amount(row[column_mapping['amount']], row_number)
            # Try to determine type from amount sign or default to debit
            trans_type = 'Credit' if amount > 0 else 'Debit'
            amount = abs(amount)
        else:
            # Separate debit/credit columns
            debit_val = row[column_mapping['debit']]
            credit_val = row[column_mapping['credit']]
            
            # Determine which column has a value
            debit_amount = self._parse_amount_optional(debit_val)
            credit_amount = self._parse_amount_optional(credit_val)
            
            if debit_amount is not None and debit_amount != 0:
                amount = abs(debit_amount)
                trans_type = 'Debit'
            elif credit_amount is not None and credit_amount != 0:
                amount = abs(credit_amount)
                trans_type = 'Credit'
            else:
                raise Exception(f"Row {row_number}: No valid amount in debit or credit columns")
        
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
    
    def _parse_date_flexible(self, date_value, row_number):
        """Parse date with flexible format detection"""
        if pd.isna(date_value) or not str(date_value).strip():
            raise Exception(f"Row {row_number}: Date is empty")
        
        date_str = str(date_value).strip()
        
        # Try multiple date formats
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%Y/%m/%d',
            '%d %b %Y',
            '%d %B %Y',
            '%b %d, %Y',
            '%B %d, %Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise Exception(f"Row {row_number}: Could not parse date '{date_str}'")
    
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
        if pd.isna(amount_value) or str(amount_value).strip() == '':
            raise Exception(f"Row {row_number}: Amount is empty")
        
        try:
            # Remove currency symbols and commas
            amount_str = str(amount_value).replace('$', '').replace(',', '').replace('€', '').replace('£', '').strip()
            amount = float(amount_str)
            return amount
        except (ValueError, TypeError):
            raise Exception(f"Row {row_number}: Invalid amount '{amount_value}'. Must be a number")
    
    def _parse_amount_optional(self, amount_value):
        """Parse amount that may be empty (for debit/credit columns)"""
        if pd.isna(amount_value) or str(amount_value).strip() == '':
            return None
        
        try:
            # Remove currency symbols and commas
            amount_str = str(amount_value).replace('$', '').replace(',', '').replace('€', '').replace('£', '').strip()
            return float(amount_str)
        except (ValueError, TypeError):
            return None
