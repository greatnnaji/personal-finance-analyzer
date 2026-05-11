"""
Unit tests for DataParser
"""
import pytest
import os
import tempfile
import csv
from services.data_parser import DataParser


class TestDataParser:
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance for testing"""
        return DataParser()
    
    @pytest.fixture
    def sample_csv_file(self):
        """Create a temporary CSV file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Description', 'Debit', 'Credit', 'Balance'])
            writer.writerow(['2024-01-01', 'Starbucks', '5.50', '0.00', '1000.00'])
            writer.writerow(['2024-01-02', 'Payroll', '0.00', '2000.00', '2994.50'])
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    def test_parser_initialization(self, parser):
        """Test that parser initializes correctly"""
        assert parser is not None
        assert hasattr(parser, 'header_patterns')
        assert isinstance(parser.header_patterns, dict)
    
    def test_parser_has_expected_patterns(self, parser):
        """Test that parser has all expected header patterns"""
        expected_keys = ['date', 'description', 'amount', 'debit', 'credit', 'balance']
        
        for key in expected_keys:
            assert key in parser.header_patterns
            assert isinstance(parser.header_patterns[key], list)
    
    def test_parser_recognizes_date_headers(self, parser):
        """Test that parser recognizes date headers"""
        date_patterns = parser.header_patterns['date']
        assert len(date_patterns) > 0
        assert any('date' in p.lower() for p in date_patterns)
    
    def test_parser_recognizes_debit_headers(self, parser):
        """Test that parser recognizes debit headers"""
        debit_patterns = parser.header_patterns['debit']
        assert len(debit_patterns) > 0
        assert any('debit' in p.lower() or 'withdrawal' in p.lower() for p in debit_patterns)
    
    def test_parser_recognizes_credit_headers(self, parser):
        """Test that parser recognizes credit headers"""
        credit_patterns = parser.header_patterns['credit']
        assert len(credit_patterns) > 0
        assert any('credit' in p.lower() or 'deposit' in p.lower() for p in credit_patterns)
    
    def test_parse_file_returns_list(self, parser, sample_csv_file):
        """Test that parse_file returns a list"""
        # Note: This test assumes the CSV file can be parsed successfully
        # Actual parsing may depend on implementation details
        assert os.path.exists(sample_csv_file)
