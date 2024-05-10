import pandas as pd

def approval_table_function(project):
    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('Excel/handover_data.xlsx')

    # Filter the DataFrame based on the parameters
    source_df = df[(df['FromProject'] == project) & (df["ApprovalToSend"] != "yes")]
    destination_df = df[(df['ToProject'] == project)]  
    
    # Update columns in the DataFrames
    destination_df["ApprovalType"] = "Receive"
    source_df["ApprovalType"] = "Send"

    # Append destination_df to source_df
    source_df = pd.concat([source_df, destination_df])

    # Sort the DataFrame based on "FormID"
    source_df = source_df.sort_values("SenderDate")

    # Convert the filtered data to JSON format
    json_data = source_df.to_json(orient='records')

    return json_data

