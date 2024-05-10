import pandas as pd
from ..Others import common_functions

def recieve_items_table_data_function(name):
    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('Excel/handover_data.xlsx')

    # Filter the DataFrame based on the parameters
    filtered_data = df[(df['ToPerson'] == name) & (df['AskReceiveApproval'] != "yes")]
    
    # Convert the filtered data to JSON format
    json_data = filtered_data.to_json(orient='records')

    return json_data


def receive_approval_request_function(form_data):
    if form_data:
        last_dict = form_data[0]  # Get the last dictionary from the list

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

    # Get the EwayBill value from the first dictionary
    eway_bill_value = form_data[1].get('EwayBill', None)
    formid = form_data[2].get('FormNo', None)

    print("formid",formid)
    print("ewaybill no",eway_bill_value)
    
    text = "Receive Form"

    common_functions.send_email(text, formid, eway_bill_value,from_person,to_person,from_project ,to_project)

    
    # Check if there is any form data
    if form_data:
        for item in form_data[3:]:  # Start iterating from the third dictionary onwards
            product_id = item['ProductID']
            receiver_condition = item['ReceiverCondition']
            receiver_remarks = item['ReceiverRemarks']

            # Find the row with the matching ProductID and update ReceiverCondition and ReceiverRemarks
            df.loc[df['ProductID'] == product_id, 'ReceiverCondition'] = receiver_condition
            df.loc[df['ProductID'] == product_id, 'ReceiverRemarks'] = receiver_remarks

        # Update the 'AskReceiveApproval' column to 'yes' for the first product
        first_product_id = form_data[3]['ProductID']  # Get the product ID from the third dictionary
        df.loc[df['ProductID'] == first_product_id, 'AskReceiveApproval'] = 'yes'

        # Save the updated DataFrame back to the Excel file
        df.to_excel(excel_file, index=False)

