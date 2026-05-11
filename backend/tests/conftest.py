"""
Pytest configuration and shared fixtures for backend tests
"""
import pytest
import sys
import os
from pathlib import Path

# Add backend module to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_transactions():
    """Fixture providing sample transaction data for testing"""
    return [
        {
            'date': '2024-01-01',
            'description': 'Starbucks Coffee',
            'debit': 5.50,
            'credit': 0.0,
            'balance': 1000.00,
            'amount': -5.50,
            'type': 'debit',
            'category': 'Food & Dining'
        },
        {
            'date': '2024-01-02',
            'description': 'Payroll Deposit',
            'debit': 0.0,
            'credit': 2000.00,
            'balance': 2994.50,
            'amount': 2000.00,
            'type': 'credit',
            'category': 'Income'
        },
        {
            'date': '2024-01-03',
            'description': 'Walmart Shopping',
            'debit': 125.75,
            'credit': 0.0,
            'balance': 2868.75,
            'amount': -125.75,
            'type': 'debit',
            'category': 'Shopping'
        },
        {
            'date': '2024-01-04',
            'description': 'Shell Gas Station',
            'debit': 55.00,
            'credit': 0.0,
            'balance': 2813.75,
            'amount': -55.00,
            'type': 'debit',
            'category': 'Transportation'
        },
        {
            'date': '2024-01-05',
            'description': 'Hydro One Bill',
            'debit': 120.00,
            'credit': 0.0,
            'balance': 2693.75,
            'amount': -120.00,
            'type': 'debit',
            'category': 'Utilities'
        }
    ]


@pytest.fixture
def empty_transactions():
    """Fixture providing empty transaction list"""
    return []


@pytest.fixture
def single_transaction():
    """Fixture providing a single transaction"""
    return [{
        'date': '2024-01-01',
        'description': 'Test Transaction',
        'debit': 10.00,
        'credit': 0.0,
        'balance': 1000.00,
        'amount': -10.00,
        'type': 'debit',
        'category': 'Other'
    }]
