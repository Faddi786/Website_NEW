from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask_cors import CORS  # Import CORS 
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('man.html')

cors = CORS(app, resources={r"/rec-data": {"origins": "*"}})  # Enable CORS for /handover_form route

@app.route('/rec-data', methods=['POST'])
def receive_data():
    data = request.json
    remarks = data.get('remarks')
    dates = data.get('dates')
    
    # Process the data as needed
    print('Received remarks:', remarks)
    print('Received dates:', dates)
    
    # You can return a response if needed
    return 'Data received successfully'

if __name__ == '__main__':
    app.run(debug=True)
