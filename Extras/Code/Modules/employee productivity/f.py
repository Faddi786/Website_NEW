import pandas as pd

def search_excel(file_path, date, name, task):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Print the first few rows of the DataFrame
    #print("First few rows of the DataFrame:")
    #print(df.head())

    # Search for rows matching the criteria
    matching_rows = df[(df['Date'] == date) & (df['Name'] == name) & (df['Task'] == task)]

    # Print matching rows
    if not matching_rows.empty:
        print("\nMatching rows found:")
        print(matching_rows.iloc[:, :12])  # Print only the first 12 columns of matching rows

    else:
        print("\nNo matching rows found.")

# Example usage:
file_path = "data4.xlsx"
date = "2024-01-11"  # Specify your date format
name = "PRASAD JADHAV"
task = "Assign Image"

search_excel(file_path, date, name, task)
