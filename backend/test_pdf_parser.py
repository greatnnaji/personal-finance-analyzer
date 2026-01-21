"""
Test script for PDF parser - helps debug and validate PDF parsing results
"""
import os
import sys
import json
from services.pdf_parser import PDFParser
from services.analyzer import DataAnalyzer
from services.categorizer import TransactionCategorizer

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_pdf_parsing(pdf_path):
    """Test PDF parsing with detailed output"""
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return
    
    print(f"🔍 Testing PDF: {pdf_path}")
    
    try:
        # Step 1: Parse PDF
        print_section("STEP 1: Parsing PDF")
        parser = PDFParser()
        transactions = parser.parse_pdf_file(pdf_path)
        print(f"✅ Successfully parsed {len(transactions)} transactions")
        
        # Step 2: Inspect raw transactions
        print_section("STEP 2: Raw Transaction Data")
        for i, trans in enumerate(transactions[:5]):  # Show first 5
            print(f"\nTransaction {i+1}:")
            print(f"  Date: {trans.get('date')}")
            print(f"  Description: {trans.get('description')}")
            print(f"  Amount: {trans.get('amount')} ({trans.get('type')})")
            print(f"  Category: {trans.get('category')}")
            print(f"  Balance: {trans.get('balance')}")
        
        if len(transactions) > 5:
            print(f"\n... and {len(transactions) - 5} more transactions")
        
        # Step 3: Check for data issues
        print_section("STEP 3: Data Validation")
        issues = []
        
        for i, trans in enumerate(transactions):
            # Check for None or NaN amounts
            amount = trans.get('amount')
            if amount is None or (isinstance(amount, float) and (amount != amount)):  # NaN check
                issues.append(f"Transaction {i+1}: Amount is None or NaN")
            
            # Check for missing descriptions
            if not trans.get('description'):
                issues.append(f"Transaction {i+1}: Missing description")
            
            # Check date format
            try:
                from datetime import datetime
                datetime.fromisoformat(trans.get('date', '').replace('Z', ''))
            except:
                issues.append(f"Transaction {i+1}: Invalid date format")
        
        if issues:
            print("⚠️  Found issues:")
            for issue in issues[:10]:  # Show first 10 issues
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more issues")
        else:
            print("✅ No data validation issues found")
        
        # Step 4: Categorize transactions
        print_section("STEP 4: Categorizing Transactions")
        categorizer = TransactionCategorizer()
        categorized = categorizer.categorize_transactions(transactions)
        
        # Count categories
        from collections import Counter
        category_counts = Counter(t['category'] for t in categorized)
        print("Category distribution:")
        for cat, count in category_counts.most_common():
            print(f"  {cat}: {count} transactions")
        
        # Step 5: Run analyzer
        print_section("STEP 5: Running Analysis")
        analyzer = DataAnalyzer()
        analysis = analyzer.analyze_transactions(categorized)
        
        # Check for NaN in results
        print("\n📊 Analysis Results:")
        print(f"  Total Transactions: {analysis.get('summary', {}).get('total_transactions')}")
        print(f"  Total Income: ${analysis.get('summary', {}).get('total_income', 0):,.2f}")
        print(f"  Total Expenses: ${analysis.get('summary', {}).get('total_expenses', 0):,.2f}")
        print(f"  Net Income: ${analysis.get('summary', {}).get('net_income', 0):,.2f}")
        
        print("\n💰 Top Spending Categories:")
        categories = analysis.get('by_category', {})
        expense_categories = {k: v for k, v in categories.items() if v.get('type') == 'expense'}
        sorted_categories = sorted(expense_categories.items(), 
                                   key=lambda x: x[1].get('total_spent', 0), 
                                   reverse=True)
        
        for cat, data in sorted_categories[:5]:
            total = data.get('total_spent', 0)
            pct = data.get('percentage_of_total', 0)
            # Check for NaN
            if isinstance(total, float) and (total != total):
                print(f"  ⚠️  {cat}: $NaN ({pct}%)")
            elif isinstance(pct, float) and (pct != pct):
                print(f"  ⚠️  {cat}: ${total:,.2f} (NaN%)")
            else:
                print(f"  {cat}: ${total:,.2f} ({pct}%)")
        
        # Check for NaN in category data
        print("\n🔍 Checking for NaN values in analysis:")
        nan_found = False
        for cat, data in categories.items():
            for key, value in data.items():
                if isinstance(value, float) and (value != value):  # NaN check
                    print(f"  ⚠️  NaN found in {cat} - {key}")
                    nan_found = True
        
        if not nan_found:
            print("  ✅ No NaN values found in analysis results")
        
        # Step 6: Save detailed output
        print_section("STEP 6: Saving Results")
        output_file = "test_results.json"
        with open(output_file, 'w') as f:
            json.dump({
                'transactions': categorized,
                'analysis': analysis,
                'validation_issues': issues
            }, f, indent=2, default=str)
        print(f"✅ Detailed results saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Default to sample data if available
        sample_path = "data/sample_data/sample-study-data.csv"
        print("No PDF path provided. Usage: python test_pdf_parser.py <path_to_pdf>")
        print(f"Example: python test_pdf_parser.py data/uploads/statement.pdf")
        sys.exit(1)
    
    test_pdf_parsing(pdf_path)
