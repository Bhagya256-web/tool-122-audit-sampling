import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.report import report_bp
from routes.health import health_bp
from routes.analyse import analyse_bp
from services.security import apply_security_headers
from services.embeddings import load_model
from services.chroma_seeder import seed_chromadb

load_dotenv()

app = Flask(__name__)

# Apply security headers to all responses
apply_security_headers(app)

# Rate limiting: 30 requests per minute per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri=os.getenv("REDIS_URL", "memory://"),
)

# Register blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)
app.register_blueprint(health_bp)
app.register_blueprint(analyse_bp)

# Pre-load models and seed data at startup
with app.app_context():
    load_model()
    seed_chromadb()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)