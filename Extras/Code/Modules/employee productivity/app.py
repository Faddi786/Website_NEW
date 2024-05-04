from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('database.html')

def accumulate_employee_data(employee_name, excel_file, header_row=4):
    # Read Excel file into a DataFrame, specifying the header row
    df = pd.read_excel(excel_file, header=header_row)
    
    # Filter DataFrame for rows with the specified employee name
    employee_data = df[df['Name'] == employee_name]
    
    # Return the accumulated data as a DataFrame
    return employee_data.to_dict(orient='records')

@app.route('/get-employee-data', methods=['GET'])
def get_employee_data():
    # Get the employee name from the query parameters
    employee_name = request.args.get('employee_name')
    
    # Specify the path to your Excel file
    excel_file = 'data.xlsx'
    
    # Call the function to accumulate data
    accumulated_data = accumulate_employee_data(employee_name, excel_file)
    
    return jsonify(accumulated_data)

if __name__ == '__main__':
    app.run(debug=True)
