"""
Enhanced PDF parser with validation and debugging
"""
import os
from datetime import datetime
from typing import List, Dict
import pypdf
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv
import json
import glob

# Load environment variables
load_dotenv()

class PDFParserDebug:
    """PDF Parser with built-in debugging and validation"""
    
    DEBUG_DIR = 'utils'
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        
        self.llm = ChatOpenAI(
            temperature=0.0,
            model="openai/gpt-4o-mini",
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        self.response_schemas = [
            ResponseSchema(
                name="date",
                description="Transaction date in YYYY-MM-DD format"
            ),
            ResponseSchema(
                name="description",
                description="Transaction description or merchant name"
            ),
            ResponseSchema(
                name="debit",
                description="Withdrawal amount as a positive number. If no withdrawal, output 0.0"
            ),
            ResponseSchema(
                name="credit",
                description="Deposit amount as a positive number. If no deposit, output 0.0"
            ),
            ResponseSchema(
                name="balance",
                description="Account balance after transaction as a number"
            )
        ]
        
        self.output_parser = StructuredOutputParser.from_response_schemas(
            self.response_schemas
        )
        self.format_instructions = self.output_parser.get_format_instructions()
    
    def validate_transaction(self, trans: Dict, index: int) -> List[str]:
        """Validate a single transaction and return list of issues"""
        issues = []
        
        # Check amount
        if 'amount' not in trans:
            issues.append(f"Trans {index}: Missing 'amount' field")
        elif trans['amount'] is None:
            issues.append(f"Trans {index}: Amount is None")
        elif isinstance(trans['amount'], float) and trans['amount'] != trans['amount']:  # NaN check
            issues.append(f"Trans {index}: Amount is NaN")
        
        # Check description
        if not trans.get('description'):
            issues.append(f"Trans {index}: Missing or empty description")
        
        # Check date
        if not trans.get('date'):
            issues.append(f"Trans {index}: Missing date")
        else:
            try:
                datetime.fromisoformat(trans['date'].replace('Z', ''))
            except:
                issues.append(f"Trans {index}: Invalid date format: {trans['date']}")
        
        # Check type
        if trans.get('type') not in ['Debit', 'Credit']:
            issues.append(f"Trans {index}: Invalid type: {trans.get('type')}")
        
        # Check category
        if not trans.get('category'):
            issues.append(f"Trans {index}: Missing category")
        
        return issues
    
    def cleanup_debug_files(self):
        """Remove all debug JSON files from utils folder"""
        debug_patterns = [
            os.path.join(self.DEBUG_DIR, 'debug_raw_transactions.json'),
            os.path.join(self.DEBUG_DIR, 'debug_validation_report.json'),
            os.path.join(self.DEBUG_DIR, 'debug_standardized_transactions.json'),
            os.path.join(self.DEBUG_DIR, 'test_results.json')
        ]
        
        removed_count = 0
        for pattern in debug_patterns:
            for file_path in glob.glob(pattern):
                try:
                    os.remove(file_path)
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️  Could not remove {file_path}: {e}")
        
        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} debug file(s)")
        return removed_count
    
    def parse_and_validate(self, pdf_path: str, save_debug=True) -> tuple:
        """Parse PDF and return (transactions, validation_report)"""
        print(f"\n{'='*60}")
        print(f"🔍 PARSING PDF WITH VALIDATION")
        print(f"{'='*60}")
        print(f"File: {pdf_path}\n")
        
        validation_report = {
            'file': pdf_path,
            'timestamp': datetime.now().isoformat(),
            'steps': [],
            'issues': [],
            'statistics': {}
        }
        
        try:
            # Step 1: Extract text
            print("📄 Step 1: Extracting text from PDF...")
            pdf_reader = pypdf.PdfReader(pdf_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if not text.strip():
                raise Exception("No text could be extracted from PDF")
            
            print(f"✅ Extracted {len(text)} characters")
            validation_report['steps'].append({
                'step': 'text_extraction',
                'status': 'success',
                'text_length': len(text)
            })
            
            # Step 2: LLM parsing
            print("\n🤖 Step 2: Parsing with LLM...")
            raw_transactions = self._parse_with_llm(text)
            print(f"✅ LLM returned {len(raw_transactions)} transactions")
            validation_report['steps'].append({
                'step': 'llm_parsing',
                'status': 'success',
                'transaction_count': len(raw_transactions)
            })
            
            # Save raw LLM output for debugging
            if save_debug:
                os.makedirs(self.DEBUG_DIR, exist_ok=True)
                debug_file = os.path.join(self.DEBUG_DIR, 'debug_raw_transactions.json')
                with open(debug_file, 'w') as f:
                    json.dump(raw_transactions, f, indent=2)
                print(f"💾 Saved raw LLM output to: {debug_file}")
            
            # Step 3: Convert to standard format
            print("\n🔄 Step 3: Converting to standard format...")
            standardized = []
            conversion_issues = []
            
            for idx, trans in enumerate(raw_transactions):
                try:
                    debit = float(trans.get('debit', 0))
                    credit = float(trans.get('credit', 0))
                    
                    # Validate debit/credit values
                    if debit != debit or credit != credit:  # NaN check
                        conversion_issues.append(f"Trans {idx+1}: NaN in debit/credit values")
                        continue
                    
                    if debit > 0:
                        amount = -debit
                        trans_type = 'Debit'
                    elif credit > 0:
                        amount = credit
                        trans_type = 'Credit'
                    else:
                        conversion_issues.append(f"Trans {idx+1}: No amount (debit={debit}, credit={credit})")
                        continue
                    
                    # Parse date
                    date_str = trans.get('date', '')
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                    except:
                        try:
                            date = datetime.strptime(date_str, '%m/%d/%Y')
                        except:
                            date = datetime.now()
                            conversion_issues.append(f"Trans {idx+1}: Invalid date, using current date")
                    
                    standardized_trans = {
                        'date': date.isoformat(),
                        'description': trans.get('description', 'Unknown'),
                        'amount': amount,
                        'type': trans_type,
                        'category': 'Uncategorized',
                        'balance': float(trans.get('balance', 0)),
                        'original_data': trans
                    }
                    
                    standardized.append(standardized_trans)
                    
                except Exception as e:
                    conversion_issues.append(f"Trans {idx+1}: {str(e)}")
            
            print(f"✅ Converted {len(standardized)} transactions")
            if conversion_issues:
                print(f"⚠️  {len(conversion_issues)} conversion issues")
            
            validation_report['steps'].append({
                'step': 'conversion',
                'status': 'success',
                'converted_count': len(standardized),
                'issues': conversion_issues
            })
            
            # Step 4: Validate transactions
            print("\n🔍 Step 4: Validating transactions...")
            all_validation_issues = []
            for idx, trans in enumerate(standardized):
                issues = self.validate_transaction(trans, idx+1)
                all_validation_issues.extend(issues)
            
            if all_validation_issues:
                print(f"⚠️  Found {len(all_validation_issues)} validation issues:")
                for issue in all_validation_issues[:10]:
                    print(f"  - {issue}")
                if len(all_validation_issues) > 10:
                    print(f"  ... and {len(all_validation_issues) - 10} more")
            else:
                print("✅ All transactions passed validation")
            
            validation_report['issues'] = all_validation_issues
            
            # Statistics
            validation_report['statistics'] = {
                'total_transactions': len(standardized),
                'debit_count': sum(1 for t in standardized if t['type'] == 'Debit'),
                'credit_count': sum(1 for t in standardized if t['type'] == 'Credit'),
                'total_debits': sum(-t['amount'] for t in standardized if t['amount'] < 0),
                'total_credits': sum(t['amount'] for t in standardized if t['amount'] > 0),
                'validation_issues': len(all_validation_issues)
            }
            
            print("\n📊 Summary Statistics:")
            for key, value in validation_report['statistics'].items():
                if isinstance(value, float):
                    print(f"  {key}: ${value:,.2f}")
                else:
                    print(f"  {key}: {value}")
            
            # Save report
            if save_debug:
                os.makedirs(self.DEBUG_DIR, exist_ok=True)
                report_file = os.path.join(self.DEBUG_DIR, 'debug_validation_report.json')
                with open(report_file, 'w') as f:
                    json.dump(validation_report, f, indent=2, default=str)
                print(f"\n💾 Saved validation report to: {report_file}")
                
                trans_file = os.path.join(self.DEBUG_DIR, 'debug_standardized_transactions.json')
                with open(trans_file, 'w') as f:
                    json.dump(standardized, f, indent=2, default=str)
                print(f"💾 Saved standardized transactions to: {trans_file}")
            
            print(f"\n{'='*60}")
            print("✅ PARSING COMPLETE")
            print(f"{'='*60}\n")
            
            return standardized, validation_report
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            validation_report['steps'].append({
                'step': 'error',
                'status': 'failed',
                'error': str(e)
            })
            return [], validation_report
    
    def _parse_with_llm(self, pdf_text: str) -> List[Dict]:
        """Use LLM to extract transactions"""
        extraction_template = """
You are a financial data extraction assistant. Extract ALL transactions from the following bank statement text.

For each transaction, extract:
- date: Transaction date in YYYY-MM-DD format
- description: Transaction description or merchant name
- debit: Withdrawal amount (positive number, or 0.0 if not a withdrawal)
- credit: Deposit amount (positive number, or 0.0 if not a deposit)
- balance: Account balance after transaction

IMPORTANT: 
- Extract EVERY transaction you find in the text
- Return a list of transactions as JSON array
- Use YYYY-MM-DD date format
- If year is not in the text, use 2024
- Amounts should be positive numbers only
- If a field is not found, use reasonable defaults

Bank statement text:
{text}

{format_instructions}

Return the output as a JSON array with key "transactions" containing all extracted transactions.
"""
        
        prompt = ChatPromptTemplate.from_template(template=extraction_template)
        messages = prompt.format_messages(
            text=pdf_text[:15000],
            format_instructions=self.format_instructions
        )
        
        response = self.llm.invoke(messages)
        
        # Parse response
        llm_output = response.content
        
        if "```json" in llm_output:
            json_start = llm_output.find("```json") + 7
            json_end = llm_output.find("```", json_start)
            json_str = llm_output[json_start:json_end].strip()
        else:
            json_str = llm_output.strip()
        
        parsed = json.loads(json_str)
        
        if isinstance(parsed, dict) and "transactions" in parsed:
            return parsed["transactions"]
        elif isinstance(parsed, list):
            return parsed
        else:
            raise Exception("Unexpected response format from LLM")


# CLI usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_parser_debug.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    parser = PDFParserDebug()
    transactions, report = parser.parse_and_validate(pdf_path)
    
    print(f"\n✅ Parsed {len(transactions)} valid transactions")
    if report['issues']:
        print(f"⚠️  {len(report['issues'])} issues found - check utils/debug_validation_report.json")
    
    # Clean up debug files after analysis
    print("\n")
    parser.cleanup_debug_files()
