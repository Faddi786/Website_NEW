import pandas as pd

def extract_rows_from_excel(form_id):
    global is_approval
    
    # Update with your Excel file path
    excel_file = "Excel/handover_data.xlsx"  
    
    try:
        # Open the Excel file
        xls = pd.ExcelFile(excel_file)
        
        # Read data from the active sheet
        df = pd.read_excel(xls, sheet_name=None)
        
        # Concatenate all sheets into one DataFrame
        df = pd.concat(df, ignore_index=True)
        
        # Convert "Serial" column to strings
        df["Serial"] = df["Serial"].astype(str)
        
        # Extract main digit from the first row's "Serial" column
        main_digit = int(df.loc[df["FormID"] == str(form_id), "Serial"].iloc[0].split('.')[0])
        
        # Filter rows based on the main digit extracted
        main_digit_rows = df[df["Serial"].str.startswith(str(main_digit) + ".")]
        
        # Convert the filtered DataFrame to dictionary records
        records = main_digit_rows.to_dict(orient="records")
        
        return records
    
    except Exception as e:
        return f"Error: {e}"

# Example usage:
form_id = "abcd123"  # Replace with the form ID you want to search for
result = extract_rows_from_excel(form_id)
print(result)
