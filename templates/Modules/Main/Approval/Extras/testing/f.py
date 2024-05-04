import pandas as pd

def get_manager_location(manager_name):
    # Load the Excel file
    df = pd.read_excel("managers.xlsx")
    
    # Check if manager_name exists in the first column
    if manager_name in df.iloc[:, 0].values:
        # Get the index of the row where manager_name exists
        index = df.index[df.iloc[:, 0] == manager_name].tolist()[0]
        
        # Get the location from the second column of that row
        location = df.iloc[index, 1]
        
        return location
    else:
        return "Manager not found in the list"

# Assign the manager's name
manager_name = "Manager1"

excel = "data.xlsx"
# Read all sheets from the Excel file
xls = pd.ExcelFile(excel)

# Get employee names
employee_names_df = get_manager_location(manager_name)
employee_names = employee_names_df['Employee Names'].tolist()

# Dictionary to store the grouped dataframes for each sheet
result = {}

# Iterate over each sheet
for sheet_name in xls.sheet_names:
    # Check if any of the employee names are present in the sheet name
    matching_names = [name for name in employee_names if name in sheet_name]
    if matching_names:
        # Read data from the sheet
        df = pd.read_excel(excel, sheet_name=sheet_name)
        
        # Extracting the main serial number
        df['Main Serial'] = df['Serial No'].astype(str).str.split('.').str[0]
        
        # Grouping the dataframe by Main Serial and creating a dictionary of dataframes
        dfs = {serial: group.drop(columns=['Serial No', 'Main Serial']) for serial, group in df.groupby('Main Serial')}
        
        # Add the dictionary of dataframes to the result dictionary with sheet name as key
        result[sheet_name] = dfs


# Print the result
print(result)

