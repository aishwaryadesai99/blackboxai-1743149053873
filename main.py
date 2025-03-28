from flask import Flask, jsonify
from database import init_db
from config import Config
from app.routes import main_bp
from datetime import datetime
import logging

app = Flask(__name__)
app.register_blueprint(main_bp)
init_db(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('security-payroll')

@app.route('/')
def home():
    return jsonify({
        "message": "Security Company Payroll System",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
