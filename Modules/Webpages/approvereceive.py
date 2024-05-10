

@app.route('/approve_receive_request', methods=['POST'])
def approve_receive_request():
    form_data = request.json  # Assuming the form data is sent as JSON
    print("This is the approve_receive_request form data", form_data)
    
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


    # Get the EwayBill value from the first dictionary
    eway_bill_value = form_data[1].get('EwayBill', None)
    formid = form_data[2].get('FormNo', None)
    print("formid", formid)

    text = "Receive Approval Form"
    send_email(text, formid, eway_bill_value,from_person,to_person,from_project ,to_project)
    ''' 
    if form_data:


        # Open inventory.xlsx
        excel_file = "Excel/inventory.xlsx"
        df = pd.read_excel(excel_file)

        # Iterate over the rest of the dictionaries
        for item in form_data[4:]:
            product_id = item['ProductID']
            condition = item['Condition']

            # Update CurrentProject, CurrentOwner, and Condition columns for each product ID
            df.loc[df['ProductID'] == product_id, 'CurrentProject'] = current_project
            df.loc[df['ProductID'] == product_id, 'CurrentOwner'] = current_person
            df.loc[df['ProductID'] == product_id, 'Condition'] = condition

        # Save the updated DataFrame back to the Excel file
        df.to_excel(excel_file, index=False)
        print("Data updated successfully.")

    # Open handover_data.xlsx
    excel_file_handover = "Excel/handover_data.xlsx"
    df_handover = pd.read_excel(excel_file_handover)

    # Check if there is any form data
    if form_data:
        product_ids = [item['ProductID'] for item in form_data[4:]]  # Start extracting from the fourth dictionary onwards
        df_handover = df_handover[~df_handover['ProductID'].isin(product_ids)]  # Remove rows with matching product IDs

        # Save the updated DataFrame back to the Excel file
        df_handover.to_excel(excel_file_handover, index=False)
    '''
    return "Approval to receive items is successfully given.\nName and project transfer has successfully completed.\nThe email is sent.\nThe receiver may proceed to utilize the items.\nThe form will self-destruct, Congrats for the successful transfer."


