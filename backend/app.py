from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Initialize Flask application
app = Flask(__name__, static_folder='../frontend/build')
CORS(app)  # This will enable CORS for all routes

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serve the frontend application.
    This route will serve the built React app and handle client-side routing.
    """
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/echo', methods=['POST'])
def echo():
    """
    Echo API endpoint.
    This route receives a POST request and returns the same data in the response.
    """
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
    