import os
from datetime import datetime
from typing import List, Dict
import pypdf
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDFParser:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize OpenRouter with API key from environment
        self.llm = ChatOpenAI(
            temperature=0.0,
            model="openai/gpt-4o-mini",  # OpenRouter model format
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Define output schema for transaction extraction
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
                description="Withdrawal amount as a positive number.  If no withdrawal, output 0.0"
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
        self.format_instructions = self. output_parser.get_format_instructions()
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try: 
            pdf_reader = pypdf.PdfReader(pdf_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if not text. strip():
                raise Exception("No text could be extracted from PDF")
            
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def parse_transactions_from_text(self, pdf_text: str) -> List[Dict]:
        """Use LLM to extract structured transaction data from PDF text"""
        
        # Create prompt template
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
        
        # Format the prompt with the PDF text
        messages = prompt.format_messages(
            text=pdf_text[: 15000],  # Limit text to avoid token limits
            format_instructions=self.format_instructions
        )
        
        try:
            # Call the LLM
            response = self.llm. invoke(messages)
            
            # Parse the response
            parsed_output = self._parse_llm_response(response. content)
            
            return parsed_output
            
        except Exception as e:
            raise Exception(f"Error parsing transactions with LLM: {str(e)}")
    
    def _parse_llm_response(self, llm_output: str) -> List[Dict]:
        """Parse LLM response into list of transaction dictionaries"""
        import json
        
        try: 
            # Try to parse as JSON
            if "```json" in llm_output: 
                # Extract JSON from markdown code block
                json_start = llm_output.find("```json") + 7
                json_end = llm_output.find("```", json_start)
                json_str = llm_output[json_start:json_end]. strip()
            else:
                json_str = llm_output. strip()
            
            parsed = json.loads(json_str)
            
            # Handle different response formats
            if isinstance(parsed, dict) and "transactions" in parsed: 
                transactions = parsed["transactions"]
            elif isinstance(parsed, list):
                transactions = parsed
            else: 
                raise Exception("Unexpected response format from LLM")
            
            return transactions
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
    
    def convert_to_standard_format(self, transactions: List[Dict]) -> List[Dict]:
        """Convert parsed transactions to standard format expected by analyzer"""
        standardized = []
        
        for idx, trans in enumerate(transactions):
            try:
                # Determine amount and type
                debit = float(trans. get('debit', 0))
                credit = float(trans. get('credit', 0))
                
                if debit > 0:
                    amount = -debit  # Negative for expenses
                    trans_type = 'Debit'
                elif credit > 0:
                    amount = credit  # Positive for income
                    trans_type = 'Credit'
                else: 
                    continue  # Skip if no amount
                
                # Parse date
                date_str = trans.get('date', '')
                try:
                    date = datetime. strptime(date_str, '%Y-%m-%d')
                except: 
                    # Try alternative formats
                    try:
                        date = datetime. strptime(date_str, '%m/%d/%Y')
                    except:
                        date = datetime.now()
                
                standardized_trans = {
                    'date':  date.isoformat(),
                    'description': trans.get('description', 'Unknown'),
                    'amount': amount,
                    'type': trans_type,
                    'category': 'Uncategorized',
                    'balance': float(trans.get('balance', 0)),
                    'original_data':  trans
                }
                
                standardized.append(standardized_trans)
                
            except Exception as e:
                print(f"Warning:  Skipping transaction {idx + 1}: {str(e)}")
                continue
        
        return standardized
    
    def parse_pdf_file(self, pdf_path: str) -> List[Dict]:
        """Main method to parse PDF and return standardized transactions"""
        print(f"Parsing PDF file: {pdf_path}")
        
        # Step 1: Extract text from PDF
        pdf_text = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(pdf_text)} characters from PDF")
        
        # Step 2: Use LLM to parse transactions
        raw_transactions = self.parse_transactions_from_text(pdf_text)
        print(f"Extracted {len(raw_transactions)} transactions using LLM")
        
        # Step 3: Convert to standard format
        standardized_transactions = self.convert_to_standard_format(raw_transactions)
        print(f"Standardized {len(standardized_transactions)} transactions")
        
        if not standardized_transactions:
            raise Exception("No valid transactions found in PDF")
        
        return standardized_transactions