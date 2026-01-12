"""
CSC506 Module 8 Portfolio System
Main Flask Application Entry Point
"""
import logging
from flask import Flask, render_template
from flask_cors import CORS
from controllers.sorting_controller import sorting_bp
from controllers.set_controller import set_bp
from controllers.stack_controller import stack_bp
from controllers.queue_controller import queue_bp
from controllers.tree_controller import tree_bp
from controllers.graph_controller import graph_bp
from controllers.hash_table_controller import hash_table_bp
from controllers.performance_controller import performance_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

logger.info("Flask application initialized")

# Register blueprints
app.register_blueprint(sorting_bp, url_prefix='/api/sorting')
app.register_blueprint(set_bp, url_prefix='/api/set')
app.register_blueprint(stack_bp, url_prefix='/api/stack')
app.register_blueprint(queue_bp, url_prefix='/api/queue')
app.register_blueprint(tree_bp, url_prefix='/api/tree')
app.register_blueprint(graph_bp, url_prefix='/api/graph')
app.register_blueprint(hash_table_bp, url_prefix='/api/hashtable')
app.register_blueprint(performance_bp, url_prefix='/api/performance')

@app.route('/')
def index():
    """Render main application page"""
    logger.info("Index page requested")
    return render_template('index.html')

if __name__ == '__main__':
    logger.info("Starting Flask application on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)



