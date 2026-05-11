"""
Unit tests for TransactionCategorizer
"""

import pytest
from services.categorizer import TransactionCategorizer


class TestTransactionCategorizer:
    @pytest.fixture
    def categorizer(self):
        """Create a categorizer instance for testing"""
        return TransactionCategorizer()

    def test_categorize_food_transaction(self, categorizer):
        """Test categorization of food & dining transactions"""
        transaction = {
            "description": "Starbucks Coffee",
            "type": "debit",
            "amount": -5.50,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Food & Dining"

    def test_categorize_grocery_transaction(self, categorizer):
        """Test categorization of grocery transactions"""
        transaction = {
            "description": "Costco Supermarket",
            "type": "debit",
            "amount": -125.00,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Groceries"

    def test_categorize_gas_transaction(self, categorizer):
        """Test categorization of transportation transactions"""
        transaction = {
            "description": "Shell Gas Station",
            "type": "debit",
            "amount": -55.00,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Transportation"

    def test_categorize_entertainment_transaction(self, categorizer):
        """Test categorization of entertainment transactions"""
        transaction = {
            "description": "Netflix Subscription",
            "type": "debit",
            "amount": -15.99,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Entertainment"

    def test_categorize_income_transaction(self, categorizer):
        """Test categorization of income transactions"""
        transaction = {
            "description": "Payroll Deposit",
            "type": "credit",
            "amount": 2000.00,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Income"

    def test_categorize_utilities_transaction(self, categorizer):
        """Test categorization of utility transactions"""
        transaction = {
            "description": "Hydro One Bill",
            "type": "debit",
            "amount": -120.00,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Utilities"

    def test_categorize_case_insensitive(self, categorizer):
        """Test that categorization is case-insensitive"""
        transaction = {
            "description": "STARBUCKS COFFEE",
            "type": "debit",
            "amount": -5.50,
        }
        result = categorizer.categorize_transaction(transaction)
        assert result["category"] == "Food & Dining"

    def test_categorize_unknown_transaction(self, categorizer):
        """Test categorization of unknown transactions"""
        transaction = {
            "description": "Unknown Merchant XYZ",
            "type": "debit",
            "amount": -50.00,
        }
        result = categorizer.categorize_transaction(transaction)
        # Should either categorize as Other or return the transaction
        assert "category" in result

    def test_categorizer_returns_transaction_dict(self, categorizer):
        """Test that categorizer returns a valid transaction dict"""
        transaction = {
            "description": "Amazon Shopping",
            "type": "debit",
            "amount": -75.50,
        }
        result = categorizer.categorize_transaction(transaction)
        assert isinstance(result, dict)
        assert "category" in result
