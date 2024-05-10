import pandas as pd

def transaction_history_table_function(name,project):

    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('Excel/handover_data.xlsx')
    print("this is the excel data",df)

    # Filter the DataFrame based on the parameters
    filtered_data = df[(df['FromProject'] == project) | (df['FromPerson'] == name) | (df['ToProject'] == project) | (df['ToPerson'] == name)]

    filtered_data = filtered_data.dropna(subset=['FormID'])

    
    # Convert the filtered data to JSON format
    json_data = filtered_data.to_json(orient='records')

    return json_data
