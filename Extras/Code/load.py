from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np  # Import numpy for handling NaN values

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ex.html')

@app.route('/data')
def get_data():
    try:
        # Read Excel file
        df = pd.read_excel('data.xlsx')
        df = df.replace({np.nan: ''})

        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        
        return jsonify(data)
    except Exception as e:
        print(e)  # Print the error for debugging purposes
        return jsonify({'error': 'Internal Server Error'}), 500  # Return a 500 status code and an error message


if __name__ == '__main__':
    app.run(debug=True)
