import pandas as pd
from flask import Flask, jsonify

def my_invent_dashboard_function(name):
    try:
        # Get the name from session data

        print("this is the global employee name", name)
        # Read Excel file
        excel_data = pd.read_excel("Excel/inventory.xlsx")
        #print("this is the excel data", excel_data)
        # Replace NaN values with 'NAN'
        excel_data = excel_data.fillna('NAN')
        #print("this is the excel data", excel_data)
        # Filter data based on 'CurrentOwner' column
        filtered_data = excel_data[excel_data['CurrentOwner'] == name]
        #print("this is the filtered data",filtered_data)
        # Remove the last two columns
        print('this is the filtered data',filtered_data)
        # Convert data to list of dictionaries
        data_list = filtered_data.to_dict(orient='records')
        #print("this is the data listttttttttttttttttttttttttt",data_list)
        # Return data as JSON

        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)})

def invent_dashboard_function():
    try:
        # Read Excel file
        excel_data = pd.read_excel("Excel/inventory.xlsx")
        
        # Replace NaN values with 'NAN'
        excel_data = excel_data.fillna('nan')
        
        # Convert data to list of dictionaries
        data_list = excel_data.to_dict(orient='records')

        # Return data as JSON
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)})


def my_project_dashboard_function(project):
    try:
        # Read Excel file
        excel_data = pd.read_excel("Excel/inventory.xlsx")
        
        # Replace NaN values with 'NAN'
        excel_data = excel_data.fillna('nan')
        print('excel data',excel_data)

        # Filter rows where 'FromProject' or 'ToProject' column matches the project variable
        filtered_data = excel_data[(excel_data['CurrentProject'] == project)]
        
        # Convert filtered data to list of dictionaries
        data_list = filtered_data.to_dict(orient='records')

        # Return filtered data as JSON
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)})