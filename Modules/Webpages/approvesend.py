import pandas as pd
from ..Others import common_functions

def approve_send_request_function(form_data):
    if form_data:
        last_dict = form_data[-1]  # Get the last dictionary from the list

        # Assign the values of the last dictionary to the global variables
        from_person = last_dict.get('FromPerson')
        to_person = last_dict.get('ToPerson')
        from_project = last_dict.get('FromProject')
        to_project = last_dict.get('ToProject')

        # Optionally, you can print the values for verification
        print("From Person:", from_person)
        print("To Person:", to_person)
        print("From Project:", from_project)
        print("To Project:", to_project)

    # Open handover_data.xlsx
    excel_file = "Excel/handover_data.xlsx"
    df = pd.read_excel(excel_file)

    # Check if there is any form data
    if form_data:
        # Get the EwayBill value and FormNo from the form data
        eway_bill_value = form_data[0].get('EwayBill', None)
        formid = form_data[1].get('FormNo', None)
        print("formid", formid)
        print("This is the ewaybill noooo", eway_bill_value)
        


        # If EwayBill value is present, find the index of the row where 'FormNo' matches the received value
        if eway_bill_value:
            form_row_index = df.index[df['FormID'] == formid].tolist()
            if form_row_index:
                df.loc[form_row_index[0], 'EwayBillNo'] = eway_bill_value
        
        # Update the 'ApprovalToSend' column for the row where 'FormNo' matches the received value
        form_row_index = df.index[df['FormID'] == formid].tolist()
        if form_row_index:
            df.loc[form_row_index[0], 'ApprovalToSend'] = 'yes'
        
        # Save the updated DataFrame back to the Excel file
        df.to_excel(excel_file, index=False)

        text = "Send Approval Form"
        common_functions.send_email(text, formid, eway_bill_value,from_person,to_person,from_project ,to_project)


    else:
        return "No data provided."





def disapprove_send_request_function(form_data):
    # Read the Excel file into a DataFrame
    df = pd.read_excel('Excel/handover_data.xlsx')

    # Convert the list of dictionaries to a DataFrame
    form_df = pd.DataFrame(form_data)

    # Remove rows where 'ProductID' matches the one received in the form data
    df = df[~df['ProductID'].isin(form_df['ProductID'])]

    # Write the updated DataFrame back to the Excel file
    with pd.ExcelWriter('Excel/handover_data.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

