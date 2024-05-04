def extract_between_form_ids(form_id, dataframe):
    # Check if the dataframe is empty
    if dataframe.empty:
        print("DataFrame is empty.")
        return None
    
    # Check if 'FormID' column exists
    if 'FormID' not in dataframe.columns:
        print("Column 'FormID' not found in the DataFrame.")
        return None
    
    # Find row numbers for the given form ID
    first_id_row_num = dataframe[dataframe['FormID'] == form_id].index.tolist()
    
    # Check if the form ID exists
    if not first_id_row_num:
        print(f"Form ID '{form_id}' not found in the DataFrame.")
        return None
    
    # If there are multiple occurrences, take the first one
    first_id_row_num = first_id_row_num[0]
    
    # Search for the next occurrence of the form ID
    second_id_row_num = first_id_row_num + 1
    while second_id_row_num < len(dataframe):
        if dataframe.at[second_id_row_num, 'FormID'] == form_id:
            break
        second_id_row_num += 1
    
    # If second_id_row_num is equal to the length of the dataframe, it means the second ID was not found
    if second_id_row_num == len(dataframe):
        print(f"Second occurrence of Form ID '{form_id}' not found after the first occurrence.")
        return None
    
    # If first_id_row_num is equal to second_id_row_num, return the row with that form ID
    if first_id_row_num == second_id_row_num:
        return dataframe.iloc[[first_id_row_num]]
    
    # Extract rows between the first and second occurrences of the form ID
    return dataframe.iloc[first_id_row_num:second_id_row_num]

# Example usage:
import pandas as pd

# Sample DataFrame
data = {
    'FormID': ['dcb432a1', '', '', 'abc2143d', 'cdb4132a'],
    'Serial': ['1.1', '1.2', '1.3', '2.1', '3.1'],
    'FromProject': ['SOI ASSAM', 'SOI ASSAM', 'SOI ASSAM', 'SOI ASSAM', 'SOI ASSAM'],
    'ToProject': ['SOI Tripura', '', '', 'SOI HP', 'SOI Tripura'],
    'FromPerson': ['Fahad', '', '', 'Umar', 'Umar'],
    'ToPerson': ['Fahad', '', '', 'Umar', 'Fahad']
}

df = pd.DataFrame(data)

form_id = 'abc2143d'  # Specify the form ID to search for

result = extract_between_form_ids(form_id, df)
if result is not None:
    print(result)
