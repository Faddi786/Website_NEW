from flask import Flask
import pandas as pd

app = Flask(__name__)

def extract_employee_data(employee_df):
    # Load employee_data.xlsx
    employee_data_file = "employee_data.xlsx"
    xls = pd.ExcelFile(employee_data_file)
    
    # Initialize an empty DataFrame to store extracted data
    extracted_data = pd.DataFrame()
    
    # Iterate over each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Check if the sheet name matches any employee name
        if sheet_name in employee_df['Employee Names'].values:
            # Read data from the sheet into a DataFrame
            sheet_data = pd.read_excel(employee_data_file, sheet_name=sheet_name)
            # Add a column to indicate the employee name
            sheet_data['Employee Name'] = sheet_name
            # Concatenate the sheet data to the extracted_data DataFrame
            extracted_data = pd.concat([extracted_data, sheet_data], ignore_index=True)
    
    return extracted_data

def get_employee_names(filename):
    # Load Excel file into a DataFrame
    df = pd.read_excel(filename)
    
    # Check if 'Manager1' exists in the first row
    if 'Manager1' in df.iloc[0]:
        # Extract employee names from the 'Manager2' column
        employee_names = df['Manager1'].dropna().tolist()
        return pd.DataFrame({'Employee Names': employee_names})
    else:
        return pd.DataFrame({'Employee Names': []})

@app.route('/')
def index():
    # Assuming your Excel file is named 'managers.xlsx' and located in the same directory as this script
    filename = 'managers.xlsx'
    
    # Get the DataFrame of employee names
    employee_df = get_employee_names(filename)
    
    # Extract employee data from employee_data.xlsx
    extracted_employee_data = extract_employee_data(employee_df)
    
    # Group extracted data by the main digit of 'Serial No'
    grouped_data = extracted_employee_data.groupby(extracted_employee_data['Serial No'].astype(str).str.split('.').str[0])
    
    # Create a dictionary to store smaller DataFrames
    smaller_dfs = {}
    
    # Iterate over groups and store smaller DataFrames
    for group_name, group_df in grouped_data:
        smaller_dfs[group_name] = group_df
    
    # Create a larger DataFrame with key-value pair
    larger_df = pd.DataFrame(columns=['Key', 'Data'])
    
    for key, value in smaller_dfs.items():
        larger_df = pd.concat([larger_df, pd.DataFrame({'Key': key, 'Data': [value]})], ignore_index=True)
    
    # Initialize an empty dictionary to store larger DataFrames
    data_dict = {}

# Outer loop to iterate over smaller_dfs
    for key, value in smaller_dfs.items():
    # Initialize larger_df for each iteration
        larger_df = pd.DataFrame()
    
    # Concatenate value to larger_df
    larger_df = pd.concat([larger_df, pd.DataFrame({'Key': key, 'Data': [value]})], ignore_index=True)
    print(larger_df)
    '''
    # Store larger_df in data_dict with key as a digit
    data_dict[int(key)] = larger_df
    print("Larger DataFrame total value:")
    print(len(data_dict))

    print("\nLarger DataFrame:")
    for key, value in data_dict.items():
        print(f"Key: {key}")
        # Determine the number of rows in the DataFrame
        num_rows = len(value)
        chunk_size = 1000  # Adjust the chunk size according to your preference
        num_chunks = num_rows // chunk_size + 1
        
        # Print DataFrame in chunks
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, num_rows)
            print(value.iloc[start_idx:end_idx])




    #print(data_dict)
    # Print larger DataFrame

    #print(df1)
    #print("\n")
    # Print the DataFrame corresponding to the 8th key
    #print("DataFrame for 8th key:")
    #print(larger_df.loc[larger_df['Key'] == '8', 'Data'].values[0])
    #print("\n")
    # Print the DataFrame corresponding to the 8th key
    #print("DataFrame for 2nd key:")
    #print(larger_df.loc[larger_df['Key'] == '2', 'Data'].values[0])
    #print("\n")
'''
    return 'Check the console for the list of employee names.'

if __name__ == '__main__':
    app.run(debug=True)
