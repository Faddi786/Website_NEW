import pandas as pd

def extract_rows(excel_file, column_name, value):
    # Load the Excel file into a DataFrame
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print("Excel file not found.")
        return None
    except Exception as e:
        print("An error occurred while loading the Excel file:", e)
        return None
    
    # Check if the specified column exists
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in the Excel file.")
        return None
    
    # Filter rows where the specified column matches the given value
    filtered_df = df[df[column_name] == value]
    
    # Return the filtered DataFrame
    return filtered_df

# Example usage:
excel_file = "Excel/handover_data.xlsx"  # Replace with your Excel file path
column_name = "FromProject"  # Replace with the column name
value = "SOI ASSAM"  # Replace with the value to search for

result_df = extract_rows(excel_file, column_name, value)
if result_df is not None:
    print(result_df)
