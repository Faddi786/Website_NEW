import pandas as pd

def transfer_progress_table_data_function(name,project):

        df = pd.read_excel('Excel/handover_data.xlsx')  # Update with your file path
        
        # Filter rows where FormID column is not null
        filtered_df = df[df['FormID'].notnull()]
        
        # Convert filtered data to JSON
        json_data = filtered_df.to_json(orient='records')
        
        return json_data



def approval_table_function(project,name):
    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('Excel/handover_data.xlsx')

    # Filter the DataFrame based on the parameters
    From_df = df[(df['FromProject'] == project)]
    To_df = df[(df['ToProject'] == project)]  
    
    # Filter the DataFrame based on the parameters
    From_df = df[(df['FromPerson'] == name)]
    To_df = df[(df['ToPerson'] == name)]  

    # Update columns in the DataFrames
    To_df["ApprovalType"] = "Receive"
    From_df["ApprovalType"] = "Send"

    # Append To_df to From_df
    From_df = pd.concat([From_df, To_df])

    # Sort the DataFrame based on "FormID"
    From_df = From_df.sort_values("SenderDate")

    # Convert the filtered data to JSON format
    json_data = From_df.to_json(orient='records')

    return json_data

'''
modify the code that i 

i want that the code should open excel
take two variable, name and project
match the name variable in fromperson column
match the name variable in toperson column  
match the project variable fromproject  column
match the project variable toproject column
and filter them if it matches
so we have 4 different dataframes 
then create a new column called 'ApprovalType' in all 4 dfs 
and for fromproject fromperson put value as 'Send'
and for toperson toproject column put value as 'Receive'
then concatenate the 4 dfs

where we have a dictionary where keys are the values from the form id column of the df and value is a list contaninig different numbers where that particula form id was found in the formid column
so in this way we can have a dictionary where we know how many formids are there and each formid is present in how many rows in the df

then later stage would be to check whether the list has more than 1 value in it
if it has more than 1 value that means that formid is present at multiple rows in the df
so we must exclude the first value in the list and push all the later values into a list called 'rows to remove', and we must do this for the keys in the dictionary
that will tell us that these rows have formid which are already present before, so we leave the first instance of the formid but remove the later instances of it]

and return the df
'''