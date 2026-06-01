import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from services.file_processor import FileProcessor
from services.data_parser import DataParser
from services.pdf_parser import PDFParser
from services.categorizer import TransactionCategorizer
from services.analyzer import DataAnalyzer

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def get_int_env(name, default):
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def build_cors_config():
    origins = os.getenv("CORS_ORIGINS", "*")
    if origins.strip() == "*":
        return {"origins": "*"}

    parsed_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
    return {"origins": parsed_origins}


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://personal-finance-analyzer-one.vercel.app"]}}, supports_credentials=True)

    app.config["UPLOAD_FOLDER"] = os.getenv(
        "UPLOAD_FOLDER", str(BASE_DIR / "data" / "uploads")
    )
    app.config["MAX_CONTENT_LENGTH"] = get_int_env(
        "MAX_CONTENT_LENGTH", 16 * 1024 * 1024
    )

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    register_routes(app)
    return app


def register_routes(app):
    @app.route("/")
    def index():
        return "Personal Finance Analyzer API is running."

    @app.route("/api/upload-and-analyze", methods=["POST"])
    def upload_and_analyze():
        """Combined endpoint: upload file and return analysis"""
        try:
            if "file" not in request.files:
                return jsonify({"error": "No file provided"}), 400

            file = request.files["file"]

            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400

            processor = FileProcessor(app.config["UPLOAD_FOLDER"])
            file_path = processor.save_file(file)

            try:
                try:
                    if file_path.endswith(".pdf"):
                        pdf_parser = PDFParser()
                        transactions = pdf_parser.parse_pdf_file(file_path)
                    else:
                        parser = DataParser()
                        transactions = parser.parse_file(file_path)

                    categorizer = TransactionCategorizer()
                    categorized_transactions = categorizer.categorize_batch(transactions)

                    analyzer = DataAnalyzer()
                    analysis = analyzer.analyze_transactions(categorized_transactions)

                    return jsonify(
                        {
                            "success": True,
                            "message": f"Successfully analyzed {len(transactions)} transactions",
                            "transactions": categorized_transactions,
                            "analysis": analysis,
                            "count": len(transactions),
                        }
                    )
                except RuntimeError as e:
                    # Likely missing API key or other runtime errors from LLM init
                    return jsonify({"error": str(e)}), 400
            finally:
                processor.cleanup_file(file_path)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"})


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=get_int_env("FLASK_PORT", 5050),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
