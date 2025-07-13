from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from services.file_processor import FileProcessor
from services.data_parser import DataParser
from services.categorizer import TransactionCategorizer
from services.analyzer import DataAnalyzer

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return 'Personal Finance Analyzer API is running.'

# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     try:
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file provided'}), 400
        
#         file = request.files['file']
        
#         if file.filename == '':
#             return jsonify({'error': 'No file selected'}), 400
        
#         # Process the uploaded file
#         processor = FileProcessor(app.config['UPLOAD_FOLDER'])
#         file_path = processor.save_file(file)
        
#         # Parse the file
#         parser = DataParser()
#         transactions = parser.parse_file(file_path)
        
#         # Clean up uploaded file
#         processor.cleanup_file(file_path)
        
#         return jsonify({
#             'success': True,
#             'transactions': transactions,
#             'count': len(transactions)
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
@app.route('/api/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    """Combined endpoint: upload file and return analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Process and parse the uploaded file
        processor = FileProcessor(app.config['UPLOAD_FOLDER'])
        file_path = processor.save_file(file)
        
        parser = DataParser()
        transactions = parser.parse_file(file_path)
        
        # Clean up uploaded file
        processor.cleanup_file(file_path)
        
        # Categorize transactions
        categorizer = TransactionCategorizer()
        categorized_transactions = categorizer.categorize_batch(transactions)
        
        # Analyze the data
        analyzer = DataAnalyzer()
        analysis = analyzer.analyze_transactions(categorized_transactions)
        
        return jsonify({
            'success': True,
            'message': f'Successfully analyzed {len(transactions)} transactions',
            'transactions': categorized_transactions,
            'analysis': analysis,
            'count': len(transactions)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
# @app.route('/api/analyze', methods=['POST'])
# def analyze_transactions():
#     try:
#         data = request.get_json()
#         transactions = data.get('transactions', [])
        
#         if not transactions:
#             return jsonify({'error': 'No transactions provided'}), 400
        
#         # Categorize transactions
#         categorizer = TransactionCategorizer()
#         categorized_transactions = categorizer.categorize_batch(transactions)
        
#         # Analyze the data
#         analyzer = DataAnalyzer()
#         analysis = analyzer.analyze_transactions(categorized_transactions)
        
#         return jsonify({
#             'success': True,
#             'transactions': categorized_transactions,
#             'analysis': analysis
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
