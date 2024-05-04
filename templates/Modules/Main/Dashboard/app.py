from flask import Flask, jsonify
import pandas as pd
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('invent.html')

@app.route('/invent_dashboard')
def invent_dashboard():
    try:
        # Read Excel file
        excel_data = pd.read_excel("inventory.xlsx")
        
        # Replace NaN values with 'NAN'
        excel_data = excel_data.fillna('NAN')
        
        # Convert data to list of dictionaries
        data_list = excel_data.to_dict(orient='records')

        # Return data as JSON
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the Flask app
