from datetime import datetime

class DataValidator:
    @staticmethod
    def is_valid_date(date_str):
        """Check if date string is valid"""
        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_amount(amount):
        """Check if amount is a valid number"""
        try:
            float(amount)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_description(description):
        """Check if description is valid"""
        return isinstance(description, str) and len(description.strip()) > 0