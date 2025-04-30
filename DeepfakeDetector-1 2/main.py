# Import app object from app.py
from app import app
from routes import setup_routes

# Setup routes
setup_routes(app)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
