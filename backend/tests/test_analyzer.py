"""
Unit tests for DataAnalyzer
"""

import pytest
from services.analyzer import DataAnalyzer


class TestDataAnalyzer:
    @pytest.fixture
    def analyzer(self):
        """Create an analyzer instance for testing"""
        return DataAnalyzer()

    def test_analyze_empty_transactions(self, analyzer):
        """Test analysis with empty transaction list"""
        result = analyzer.analyze_transactions([])
        assert result == {}

    def test_analyze_single_transaction(self, analyzer, single_transaction):
        """Test analysis with a single transaction"""
        result = analyzer.analyze_transactions(single_transaction)
        assert "summary" in result
        assert result["summary"]["total_transactions"] == 1

    def test_analyze_calculates_totals(self, analyzer, sample_transactions):
        """Test that analysis calculates correct totals"""
        result = analyzer.analyze_transactions(sample_transactions)
        summary = result["summary"]

        assert summary["total_transactions"] == 5
        assert summary["total_income"] > 0
        assert summary["total_expenses"] > 0
        assert summary["net_income"] > 0

    def test_analyze_includes_date_range(self, analyzer, sample_transactions):
        """Test that analysis includes correct date range"""
        result = analyzer.analyze_transactions(sample_transactions)
        summary = result["summary"]

        assert "date_range" in summary
        assert "start" in summary["date_range"]
        assert "end" in summary["date_range"]

    def test_analyze_by_category(self, analyzer, sample_transactions):
        """Test that analysis breaks down by category"""
        result = analyzer.analyze_transactions(sample_transactions)
        assert "by_category" in result

    def test_analyze_by_month(self, analyzer, sample_transactions):
        """Test that analysis breaks down by month"""
        result = analyzer.analyze_transactions(sample_transactions)
        assert "by_month" in result

    def test_analyze_includes_spending_trends(self, analyzer, sample_transactions):
        """Test that analysis includes spending trends"""
        result = analyzer.analyze_transactions(sample_transactions)
        assert "spending_trends" in result

    def test_analyze_includes_top_expenses(self, analyzer, sample_transactions):
        """Test that analysis includes top expenses"""
        result = analyzer.analyze_transactions(sample_transactions)
        assert "top_expenses" in result

    def test_analyze_includes_income_vs_expenses(self, analyzer, sample_transactions):
        """Test that analysis compares income vs expenses"""
        result = analyzer.analyze_transactions(sample_transactions)
        assert "income_vs_expenses" in result

    def test_analyze_calculates_average_transaction(
        self, analyzer, sample_transactions
    ):
        """Test that average transaction is calculated"""
        result = analyzer.analyze_transactions(sample_transactions)
        summary = result["summary"]
        assert "average_transaction" in summary
        assert isinstance(summary["average_transaction"], (int, float))

    def test_analyze_returns_all_sections(self, analyzer, sample_transactions):
        """Test that analysis returns all expected sections"""
        result = analyzer.analyze_transactions(sample_transactions)

        expected_keys = [
            "summary",
            "by_category",
            "by_month",
            "spending_trends",
            "top_expenses",
            "income_vs_expenses",
            "spending_patterns",
            "ai_insights",
        ]

        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
