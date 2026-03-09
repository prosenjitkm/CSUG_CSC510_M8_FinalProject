"""
CSC506 Module 8 Astrology AI
Main Flask Application Entry Point
"""
import logging
from flask import Flask, render_template
from flask_cors import CORS
from controllers.astrology_controller import astrology_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logger.info("Flask application initialized")

# Register blueprints
app.register_blueprint(astrology_bp, url_prefix='/api/astrology')

@app.route('/')
def index():
    """Render astrology application page"""
    logger.info("Astrology page requested at root")
    return render_template('astrology.html')


@app.route('/astrology')
def astrology():
    """Render astrology assistant page"""
    logger.info("Astrology page requested")
    return render_template('astrology.html')

if __name__ == '__main__':
    logger.info("Starting Flask application on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)



