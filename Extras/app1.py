


@app.route('/register')
def register():
    return render_template('Modules/Main/Start/templates/register.html')

is_approval = False



def approve_extract_rows_from_excel(serial_number):

    # Get the name from session data
    name = session.get('login_row_data', {}).get('Location', 'Unknown')
    
    # Update with your Excel file path
    excel_file = "Excel/approvals.xlsx"  
    
    # Open the Excel file
    xls = pd.ExcelFile(excel_file)
    
    # Find the sheet with the name from the session cookie
    sheet_names = xls.sheet_names
    target_sheet_name = None
    for sheet_name in sheet_names:
        if name.lower() in sheet_name.lower():
            target_sheet_name = sheet_name
            break
    
    if target_sheet_name is None:
        return "Sheet not found for user: {}".format(name)
    
    # Read data from the identified sheet
    df = pd.read_excel(excel_file, sheet_name=target_sheet_name)
    print("This is the df dataaaaa", df )
    # Convert "Serial No" column to strings
    df["Serial No"] = df["Serial No"].astype(str)
    
    # Filter rows based on serial number
    filtered_df = df[df["Serial No"].str.startswith(str(serial_number) + ".")]

    filtered_df.fillna('NAN', inplace=True)

    return filtered_df.to_dict(orient="records")


        
def extract_rows_from_excel(serial_number):
    global is_approval
    # Get the name from session data
    name = session.get('login_row_data', {}).get('Name', 'Unknown')
    
    # Update with your Excel file path
    excel_file = "Excel/handover_data.xlsx"  
    
    # Open the Excel file
    xls = pd.ExcelFile(excel_file)
    
    # Find the sheet with the name from the session cookie
    sheet_names = xls.sheet_names
    target_sheet_name = None
    for sheet_name in sheet_names:
        if name.lower() in sheet_name.lower():
            target_sheet_name = sheet_name
            break
    
    if target_sheet_name is None:
        return "Sheet not found for user: {}".format(name)
    
    # Read data from the identified sheet
    df = pd.read_excel(excel_file, sheet_name=target_sheet_name)
    #print("This is the df dataaaaa", df )
    # Convert "Serial No" column to strings
    df["Serial No"] = df["Serial No"].astype(str)
    
    # Filter rows based on serial number
    filtered_df = df[df["Serial No"].str.startswith(str(serial_number) + ".")]

    # Check if any value in the "Approval" column is True
    if True in filtered_df["Approval"].values:
        is_approval = True
    else:
        is_approval = False
    # Replace NaN values with "Nan"
    filtered_df.fillna("Nan", inplace=True)
    
    # Remove the last column
    #filtered_df = filtered_df.iloc[:, :-2]

    # Print the value of is_approval
    #print("is_approval:", is_approval)
    print("This is the filtered dffffffff",filtered_df)
    return filtered_df.to_dict(orient="records")


@app.route('/approval_acceptance')
def approval_acceptance():
    # Assuming you want to return True
    global is_approval
    print("This is the approval",is_approval)
    return jsonify(is_approval)
    
    
# Load the Excel file
excel_file = "Excel/handover_data.xlsx"
df = pd.read_excel(excel_file)
extracted_rows = None
approve_send_extracted_rows = None


@app.route('/get_button_number', methods=['GET'])
def get_button_number():
    global extracted_rows
    button_number = int(request.args.get('button_number'))
    extracted_rows = extract_rows_from_excel(button_number)
    #print("These are the extracted rowwwwwwwwwwwwwwwwwwwwwwwwwws",extracted_rows)
    return jsonify(extracted_rows)

@app.route('/get_form_data')
def get_form_data():
    global extracted_rows
  
    #print("This is the rowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww whatsasioadhwioe fhweuilbgy",extracted_rows)
    # Convert DataFrame to JSON string and return
    json_data = jsonify(extracted_rows)

    return json_data



@app.route('/approve_send_get_button_number', methods=['GET'])
def approve_send_get_button_number():
    global approve_send_extracted_rows
    button_number = int(request.args.get('button_number'))
    approve_send_extracted_rows = approve_send_extract_rows_from_excel(button_number)
    print("These are the extracted rowwwwwwwwwwwwwwwwwwwwwwwwwws",approve_send_extracted_rows)
    return jsonify(approve_send_extracted_rows)



@app.route('/approve_get_form_data')
def approve_get_form_data():
    global approve_send_extracted_rows

    #print("This is the rowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww whatsasioadhwioe fhweuilbgy",approve_send_extracted_rows)
    # Convert DataFrame to JSON string and return
    json_data = jsonify(approve_send_extracted_rows)

    return json_data



@app.route('/approve_send_form_data_display')
def approve_send_form_data_display():
    return render_template('Modules/Main/Approval/Approval Send/templates/approve_send_form_data.html', data=approve_send_extracted_rows)







@app.route('/approve_send')
def approve_send():
    return render_template('Modules/Main/Approval/Approval Send/templates/approve_send_bar.html')

@app.route('/approve_receive')
def approve_receive():
    return render_template('Modules/Main/Approval/Approval Receive/templates/approve_receive_bar.html')

@app.route('/my_reci')
def my_reci():
    return render_template('Modules/Main/Reciever/my_reci.html')

@app.route('/add_item')
def add_item():
    return render_template('Modules/Secondary/Item/add_item.html')

@app.route('/delete_item')
def delete_item():
    return render_template('Modules/Secondary/Item/delete_item.html')

@app.route('/item_main')
def item_main():
    return render_template('Modules/Secondary/Item/item_main.html')
            
@app.route('/removed_items')
def removed_items():
    return render_template('Modules/Secondary/Item/inventory_dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('Modules/Main/Dashboard/templates/invent.html')


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

def remove_rows_related_to_serial(serial_no):
    # Load the Excel file
    wb = openpyxl.load_workbook('Excel/approvals.xlsx')
    sheet = wb.active
    
    # Find the column indices based on column names in the first row
    headers = [cell.value for cell in sheet[1]]  # Assuming headers are in the first row
    serial_column_index = headers.index('ProductID') + 1  # Adding 1 to convert to 1-based indexing
    serial_no_column_index = headers.index('Serial No') + 1  # Adding 1 to convert to 1-based indexing
    
    # Iterate over the rows in the sheet
    rows_to_remove = []
    for row_index in range(2, sheet.max_row + 1):  # Start from row 2, assuming headers are in row 1
        serial_value = sheet.cell(row=row_index, column=serial_column_index).value
        
        # Check if the serial number matches
        if serial_value == serial_no:
            # Extract the main digit from the 'Serial No' column
            serial_no_value = str(sheet.cell(row=row_index, column=serial_no_column_index).value)
            main_digit = int(serial_no_value.split('.')[0])
            
            # Find all rows with the same main digit and mark them for removal
            for inner_row_index in range(2, sheet.max_row + 1):
                inner_serial_no_value = str(sheet.cell(row=inner_row_index, column=serial_no_column_index).value)
                inner_main_digit = int(inner_serial_no_value.split('.')[0])
                if inner_main_digit == main_digit:
                    rows_to_remove.append(inner_row_index)
    
    # Remove the marked rows
    for row_index in sorted(rows_to_remove, reverse=True):
        sheet.delete_rows(row_index)
    
    # Save the changes
    wb.save('Excel/approvals.xlsx')








def remove_rows_with_changed_date(excel):

    # Load the Excel file
    wb = openpyxl.load_workbook(excel)
    sheet = wb.active
    
    # Find the column indices based on column names in the first row
    headers = [cell.value for cell in sheet[1]]  # Assuming headers are in the first row
    serial_no_column_index = headers.index('Serial No') + 1  # Adding 1 to convert to 1-based indexing
    acceptance_date_column_index = headers.index('Acceptance Date') + 1  # Adding 1 to convert to 1-based indexing
    
    # Get current date
    current_date = dt.now(timezone.utc).date()
    
    # Iterate over the rows in the sheet
    row_index = 2  # Start from row 2, assuming headers are in row 1
    while row_index <= sheet.max_row:
        acceptance_date = sheet.cell(row=row_index, column=acceptance_date_column_index).value
        # Ensure acceptance_date is in datetime format
        if isinstance(acceptance_date, dt):
            acceptance_date = acceptance_date.date()
        
        # Check if acceptance date matches the current date
        if acceptance_date != current_date:
            # Extract the main digit from the 'Serial No' column
            serial_no_value = str(sheet.cell(row=row_index, column=serial_no_column_index).value)
            main_digit = int(serial_no_value.split('.')[0])
            
            # Find all rows with the same main digit and mark them for removal
            rows_to_remove = []
            while row_index <= sheet.max_row:
                inner_serial_no_value = str(sheet.cell(row=row_index, column=serial_no_column_index).value)
                inner_main_digit = int(inner_serial_no_value.split('.')[0])
                if inner_main_digit == main_digit:
                    rows_to_remove.append(row_index)
                    row_index += 1
                else:
                    break
            
            # Remove the marked rows
            for idx in reversed(rows_to_remove):
                sheet.delete_rows(idx)
        else:
            row_index += 1
    
    # Save the changes
    wb.save(excel)

def format_serial_numbers(file_path):
    try:
        # Load the Excel file
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        
        # Find the column index of the 'Serial No' column
        headers = [cell.value for cell in sheet[1]]
        serial_no_column_index = headers.index('Serial No') + 1
        
        # Initialize variables to track the current main digit and subpart
        current_main_digit = None
        current_subpart = None
        
        print("Starting formatting process...")
        
        # Iterate over the rows in the sheet starting from the second row
        for row_index in range(2, sheet.max_row + 1):
            # Get the current serial number from the cell
            serial_no = str(sheet.cell(row=row_index, column=serial_no_column_index).value)
            
            # Split the serial number into main digit and subpart
            main_digit, subpart = map(int, serial_no.split('.'))
            
            # Check if there is a gap in the main digits or if the subpart resets to 1
            if current_main_digit is not None and (main_digit > current_main_digit + 1 or subpart == 1):
                # Reset the current main digit
                current_main_digit = main_digit
            
            # Update the main digit if it's not set
            if current_main_digit is None:
                current_main_digit = main_digit
            
            # Format the serial number with the current main digit and subpart
            formatted_serial_no = f"{current_main_digit}.{subpart}"
            sheet.cell(row=row_index, column=serial_no_column_index).value = formatted_serial_no
            
            print(f"Formatted serial number for row {row_index}: {formatted_serial_no}")
        
        # Save the changes
        wb.save(file_path)
        
        print("Formatting process completed successfully.")
        
    except Exception as e:
        print("An error occurred during formatting:")
        print(e)


def correct_versions(versions):
    try:
        # Extracting major parts
        major_parts = [int(version.split('.')[0]) for version in versions]
        print("Extracted major parts:", major_parts)

        # Mapping major parts to consecutive digits starting from 1
        major_mapping = {}
        mapped_major_parts = []
        counter = 1
        for major in major_parts:
            if major not in major_mapping:
                major_mapping[major] = counter
                counter += 1
            mapped_major_parts.append(major_mapping[major])
        print("Mapped major parts:", mapped_major_parts)

        # Reconstructing the strings with mapped major parts
        mapped_versions = [f"{mapped_major}.{minor}" for mapped_major, minor in zip(mapped_major_parts, [version.split('.')[1] for version in versions])]
        print("Mapped versions:", mapped_versions)

        return mapped_versions
    except Exception as e:
        print("An error occurred in correcting versions:", e)
        return None


def process_excel(file_path):
    try:
        # Load the Excel workbook
        wb = openpyxl.load_workbook(file_path)
        
        # Select the active worksheet
        ws = wb.active
        
        # Find the column index based on column names in the first row
        headers = [cell.value for cell in ws[1]]  # Assuming headers are in the first row
        serial_no_column_index = headers.index('Serial No') + 1  # Adding 1 to convert to 1-based indexing
        print("Serial No column index:", serial_no_column_index)
        
        # Get values from Serial_No column and convert to a list of strings
        serial_nos = [str(cell.value) for row in ws.iter_rows(min_row=2, min_col=serial_no_column_index, max_col=serial_no_column_index) for cell in row if cell.value is not None]
        print("Serial Nos from Excel:", serial_nos)
        
        # Correct the versions
        corrected_versions = correct_versions(serial_nos)
        print("Corrected versions:", corrected_versions)
        
        if corrected_versions is None:
            print("No corrected versions were generated. Exiting...")
            return
        
        # Write corrected values back to Serial_No column
        for i, corrected_version in enumerate(corrected_versions):
            ws.cell(row=i+2, column=serial_no_column_index, value=corrected_version)
        
        # Save the changes
        wb.save(file_path)
        print("Corrections saved to Excel.")
    
    except Exception as e:
        print("An error occurred:", e)



send_items_excel='Excel/send_items.xlsx'
receive_items_excel='Excel/receive_items.xlsx'
approve_send_excel='Excel/approve_send.xlsx'
approve_receive_excel='Excel/approve_receive.xlsx'

def get_total_links(excel):

    remove_rows_with_changed_date(excel)
    
    process_excel(excel)

    # Load the Excel workbook
    wb = openpyxl.load_workbook(excel)
    
    # Example usage
    format_serial_numbers(excel)

    # Get the name from session data
    name = session.get('login_row_data', {}).get('Name', 'Unknown')

    # Access the sheet named 'Tom'
    sheet = wb["Fahad"]
    
    # Get the values from the 'Serial No' column
    serial_numbers = [cell.value for cell in sheet['A'] if cell.value is not None]
    
    # Extract the last number
    last_serial_number = serial_numbers[-1]
    
    # Extract the digit before the decimal point
    last_digit = int(str(last_serial_number).split('.')[0])

    print(last_digit)
    
    return last_digit


@app.route('/get_link_number')
def get_link_number():
    #last_digit = get_total_links()
    #print("This is the total number of digit without floating point",last_digit)
    return str(10)


def get_total_rows(excel):

    process_excel(excel)

    # Load the Excel workbook
    wb = openpyxl.load_workbook(excel)
    
    # Get the name from session data
    location = session.get('login_row_data', {}).get('Location', 'Unknown')
    print(session)
    print(location)
    # Access the sheet named 'Tom'
    sheet = wb[location]
    
    # Get the values from the 'Serial No' column
    serial_numbers = [cell.value for cell in sheet['A'] if cell.value is not None]
    
    # Extract the last number
    last_serial_number = serial_numbers[-1]
    
    # Extract the digit before the decimal point
    last_digit = int(str(last_serial_number).split('.')[0])

    print(last_digit)
    
    return last_digit

@app.route('/get_list')
def get_list():
    #total_rows = get_total_rows()
    #print("This is the total number of digit without floating point for approval send get link number",last_digit)
    return str(10)




# Function to send email with attachment
def send_email(pdf_file):
    # Sender and receiver email addresses
    sender_email = "shaikhfahad687@gmail.com"  # Update with your Gmail address
    receiver_email = "shaikhfahad687@gmail.com"  # Update with the receiver's email address

    # Gmail SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Port for TLS encryption

    # Login credentials (use app password)
    email_password = "rgbbdlhpyleheico"  # Update with your Gmail app password

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Form Data PDF"

    # Attach PDF file
    with open(pdf_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {pdf_file}",
    )

    message.attach(part)

    # Establish a secure connection with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        # Login to the SMTP server
        server.login(sender_email, email_password)
        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

def create_pdf(form_data):
    # Create a PDF
    pdf_file = "form_data.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []

    # Form details
    details = [["Detail", "Value"]]
    for key, value in form_data[0].items():
        details.append([key, value])

    # Item description table
    item_headers = ["Name", "Make", "Model", "ProductID"]
    item_data = [[item["Name"], item["Make"], item["Model"], item["ProductID"]] for item in form_data[1:]]
    item_table = Table([item_headers] + item_data)
    item_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    # Add elements to the PDF
    elements.append(Table(details))
    elements.append(item_table)

    # Build the PDF
    doc.build(elements)

    print("PDF created successfully")



@app.route('/ask_for_send_approval', methods=['POST'])
def ask_for_send_approval():

    form_data = request.json  # Get JSON data from the request
    print("This is the form data",form_data)

    create_pdf(form_data)

    # Call the function to send email with the generated PDF attached
    send_email("form_data.pdf")

    # Mapping of keys to column indices
    key_to_column = {
        'Category': 1,
        'Name': 2,
        'Make': 3,
        'Model': 4,
        'ProductID': 5,
        'Condition': 11,
        'SenderFrontend': 13,
        'SenderBackend': 14,
        'SenderCleanup': 15,
        'SenderRemarks': 16,
    }

    # Define column names
    columns = ['Serial No', 'Category', 'Name', 'Make', 'Model', 'ProductID', 'Handover location', 'Handover authorized by', 'Handover date', 'Receiver Date', 'Acceptance Date', 'Condition', 'Reached', 'SenderFrontend', 'SenderBackend', 'SenderCleanup', 'SenderRemarks', 'ReceiverFrontend', 'ReceiverBackend', 'ReceiverCleanup', 'ReceiverRemarks','Approval','Current Project','Previous Project','Current Owner', 'Previous Owner']

    # Get the name from session data
    name = session.get('login_row_data', {}).get('Name', 'Unknown')

    # Load existing Excel file if it exists, otherwise create an empty DataFrame
    try:
        existing_df = pd.read_excel('Excel/send_items_excel.xlsx', sheet_name=str(name))
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=columns)
    except ValueError:
        existing_df = pd.DataFrame(columns=columns)

    # Create a DataFrame from the form data
    new_data = []
    for item in form_data[1:]:  # Exclude the first row which contains metadata
        new_row = [None] * len(columns)  # Initialize a new row with None values
        for key, value in item.items():
            if key in key_to_column:
                if isinstance(key_to_column[key], int):
                    new_row[key_to_column[key]] = value
                elif isinstance(key_to_column[key], dict):
                    # Set flags for 'frontend', 'backend', and 'cleanup' based on the 'Status' field
                    status_parts = value.split(',')
                    for status_part in status_parts:
                        if status_part.strip() in key_to_column[key]:
                            new_row[key_to_column[key][status_part.strip()]] = 1
        new_data.append(new_row)

    new_df = pd.DataFrame(new_data, columns=columns)

    # Determine the next value for "Serial No" for the new data
    if not existing_df.empty and not existing_df['Serial No'].isnull().all():
        last_serial_no = existing_df['Serial No'].iloc[-1]  # Get the last serial number
        last_serial_no = str(last_serial_no)  # Convert to string explicitly
        match = re.match(r"(\d+)\.(\d+)", last_serial_no)  # Extract numerical parts using regex
        if match:
            last_main_num = int(match.group(1))  # Extract the main number part
            last_sub_num = int(match.group(2))  # Extract the sub number part
        else:
            last_main_num = 0
            last_sub_num = 0
    else:
        last_main_num = 0
        last_sub_num = 0

    # Calculate the total number of rows in the existing DataFrame and new DataFrame combined
    total_rows = len(existing_df) + len(new_df)

    # Determine the current numerical part for the new batch
    current_main_num = last_main_num + 1

    # Reset the subpart if the main part changes
    if current_main_num > last_main_num:
        last_sub_num = 0

    # Iterate over each row of new data and generate serial numbers
    serial_numbers = []
    for i in range(len(new_df)):
        current_sub_num = last_sub_num + i + 1
        new_serial_no = str(current_main_num) + '.' + str(current_sub_num)
        serial_numbers.append(new_serial_no)

    # Add serial numbers to the new data frame
    new_df['Serial No'] = serial_numbers

    # Add current date to the new data frame
    new_df['Handover date'] = datetime.now().date()

    # Concatenate existing and new data frames
    df = pd.concat([existing_df, new_df], ignore_index=True)

    # Write the updated data frame back to the Excel file
    with pd.ExcelWriter('Excel/send_items_excel.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=str(name))

    # Return a success message
    return jsonify({'message': 'Excel file updated successfully'})




@app.route('/update_owner', methods=['POST'])
def update_owner():
    try:
        form_data = request.json  # Get JSON data from the request
        #print("This is the form dataaaaaaaaaaaaaaa",form_data)

        first_item = form_data[0]  # Get the first dictionary

        # Extract all the serial numbers from the entire form_data
        product_serial_list = [item.get('Product_Serial') for item in form_data]
        print("All Product Serials:", product_serial_list)

        # Assuming form_data is a list containing dictionaries
        receiver_person_name = first_item.get('receiverPersonName')  # Extract the 'receiverPersonName' value
        print("Receiver Person Name:", receiver_person_name)

        update_owners(product_serial_list, receiver_person_name)

    except Exception as e:
        # Log the error for debugging purposes
        print("Error processing approval request:", str(e))
        return jsonify({"error": "Bad Request"}), 400

    return "Successfuly updated owner"


def update_excel_with_approval(serial_no):
    # Load the Excel file
    wb = openpyxl.load_workbook('Excel/handover_data.xlsx')
    sheet = wb.active
    
    # Iterate over the rows in the sheet
    for row_index in range(2, sheet.max_row + 1):  # Start from row 2, assuming headers are in row 1
        row = [cell.value for cell in sheet[row_index]]  # Get values of the row
        
        # Check if the serial number is in the row
        if row[0] == serial_no:  # Assuming 'Product_Serial' column is the 17th column
            # Update the Approval column
            sheet.cell(row=row_index, column=21, value=1)  # Assuming 'Approval' column is the 17th column
            break
    
    # Save the changes
    wb.save('Excel/handover_data.xlsx')




def update_owners(serial_nos, receiver_name):
    # Load the Excel file
    wb = openpyxl.load_workbook('Excel/data.xlsx')
    sheet = wb.active
    
    # Find the column indices based on column names in the first row
    headers = [cell.value for cell in sheet[1]]  # Assuming headers are in the first row
    serial_column_index = headers.index('ProductID') + 1  # Adding 1 to convert to 1-based indexing
    current_owner_column_index = headers.index('Current Owner') + 1  # Adding 1 to convert to 1-based indexing
    previous_owner_column_index = headers.index('Previous Owner') + 1  # Adding 1 to convert to 1-based indexing
    
    # Iterate over each serial number in the list
    for serial_no in serial_nos:
        # Iterate over the rows in the sheet
        for row_index in range(2, sheet.max_row + 1):  # Start from row 2, assuming headers are in row 1
            serial_value = sheet.cell(row=row_index, column=serial_column_index).value
            
            # Check if the serial number matches
            if serial_value == serial_no:
                # Get the current owner and update it
                current_owner = sheet.cell(row=row_index, column=current_owner_column_index).value
                sheet.cell(row=row_index, column=current_owner_column_index).value = receiver_name
                
                # Update the previous owner
                sheet.cell(row=row_index, column=previous_owner_column_index).value = current_owner
    
    # Save the changes
    wb.save('Excel/data.xlsx')




@app.route('/accept_items', methods=['POST'])
def accept_items():
    form_data = request.json  # Get JSON data from the request
    if form_data:
        # Retrieve Current Owner and ProductID from the first dictionary
        first_item = form_data[0]
        current_owner = first_item.get('Current Owner')
        product_id = first_item.get('ProductID')
        print("Current Owner:", current_owner)
        print("Product ID:", product_id)

        # Retrieve all ProductIDs and put them in a list
        all_product_ids = [item.get('ProductID') for item in form_data]
        print("All Product IDs:", all_product_ids)
        
        # Do whatever you want with current_owner, product_id, and all_product_ids
    else:
        print("No data received")

    update_owners(all_product_ids, current_owner)
    print("update_owners done")

    update_excel_with_approval(product_id)  # Pass the serial number you want to search for
    print("update_excel_with_approval done")
    
    remove_rows_related_to_serial(product_id)
    print("remove_rows_related_to_serial done")
    return jsonify({'message': 'Excel file updated successfully'})







@app.route('/invent_dashboard')
def invent_dashboard():
    try:
        # Read Excel file
        excel_data = pd.read_excel("inventory.xlsx")
        
        # Replace NaN values with 'NAN'
        excel_data = excel_data.fillna('NAN')
        
        # Convert data to list of dictionaries
        data_list = excel_data.to_dict(orient='records')

        # Return data as JSON
        return jsonify(data_list)
    except Exception as e:
        return jsonify({'error': str(e)})

'''
@app.route('/invent_dashboard')
def invent_dashboard():
    # Read data from Excel file
    df = pd.read_excel('Excel/inventory.xlsx')

    # Add a new column for delete button
    df['Delete'] = '<button class="delete-btn">Delete</button>'

    # Convert DataFrame to HTML table
    table = df.to_html(index=False, escape=False)

    # Pass the HTML table to the template
    return render_template('Modules/Main/Dashboard/invent_dashboard.html', table=table)
'''

@app.route('/invent_personal')
def invent_personal():
    # Read data from Excel file
    df = pd.read_excel('Excel/data.xlsx')

    # Convert DataFrame to HTML table
    table = df.to_html(index=False, escape=False)

    # Pass the HTML table to the template
    return render_template('Modules/Main/Dashboard/invent_personal.html', table=table)



@app.route('/save_table', methods=['POST'])
def save_table():
    # Get table data from AJAX request
    table_data = request.json['table']
    # Convert table data to DataFrame
    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    # Save DataFrame to Excel file
    df.to_excel('table_data.xlsx', index=False)
    # Return success message
    return jsonify({'message': 'Table saved to Excel successfully'})



@app.route('/y')
def y():
    # Read data from Excel file
    df = pd.read_excel('Excel/added_items.xlsx')
    # Convert DataFrame to HTML table
    table = df.to_html(index=False)
    # Pass the HTML table to the template
    return render_template('Modules/Main/Dashboard/invent_dashboard.html', table=table)

@app.route('/z')
def z():
    # Read data from Excel file
    df = pd.read_excel('Excel/deleted_items.xlsx')
    # Convert DataFrame to HTML table
    table = df.to_html(index=False)
    # Pass the HTML table to the template
    return render_template('Modules/Main/Dashboard/invent_dashboard.html', table=table)





@app.route('/add_item_', methods=['POST'])
def add_item_():
    item_description = request.form['item_description']
    make = request.form['make']
    model = request.form['model']
    serial_number = request.form['serial_number']

    # Load the main data Excel file
    wb_main = openpyxl.load_workbook('Excel/data.xlsx')
    ws_main = wb_main.active

    entry_exists = False
    for row in ws_main.iter_rows(min_row=2):
        if (row[1].value == item_description and
            row[2].value == make and
            row[3].value == model and
            row[4].value == serial_number):
            entry_exists = True
            break

    if entry_exists:
        print("Entry already exists!")
        return "Entry already exists!"
    else:
        max_row = ws_main.max_row
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ws_main.cell(row=max_row+1, column=5, value=serial_number)
        ws_main.cell(row=max_row+1, column=2, value=item_description)
        ws_main.cell(row=max_row+1, column=3, value=make)
        ws_main.cell(row=max_row+1, column=4, value=model)
        wb_main.save('Excel/data.xlsx')
        print("Item added successfully!")

        # Check if the added_items.xlsx file exists, if not create it
        if not os.path.isfile('Excel/added_items.xlsx'):
            wb_added = openpyxl.Workbook()
            ws_added = wb_added.active
            ws_added.append(['Name','Item Description', 'Make', 'Model', 'Serial Number', 'Date and Time'])
        else:
            wb_added = openpyxl.load_workbook('Excel/added_items.xlsx')
            ws_added = wb_added.active

        # Get the name from session data
        name = session.get('login_row_data', {}).get('Name', 'Unknown')

        # Append the new row to the added_items.xlsx file
        ws_added.append([name,item_description, make, model, serial_number, current_date_time])
        wb_added.save('Excel/added_items.xlsx')

        return "Item added successfully!"


@app.route('/delete_item_', methods=['POST'])
def delete_item_():
    item_description = request.form['item_description']
    make = request.form['make']
    model = request.form['model']
    serial_number = request.form['serial_number']

    wb = openpyxl.load_workbook('Excel/data.xlsx')
    ws = wb.active

    deleted_item = None
    entry_found = False
    print("Input Values:")
    print("item_description:", item_description)
    print("make:", make)
    print("model:", model)
    print("serial_number:", serial_number)

    # Adjust the loop to start from the second row (index 2) since the first row is headers
    for row in ws.iter_rows(min_row=0, max_row=ws.max_row):

        print("Row Values:")
        print("item_description:", row[1].value)
        print("make:", row[2].value)
        print("model:", row[3].value)
        print("serial_number:", row[4].value)

        if (row[1].value == item_description and
            row[2].value == make and
            row[3].value == model and
            row[4].value == serial_number):
            entry_found = True
            deleted_item = [cell.value for cell in row]  # Storing the deleted item's data
            ws.delete_rows(row[0].row)  # Deleting the entire row where the match is found
            wb.save('Excel/data.xlsx')
            break


    if entry_found:
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Get the name from session data
        name = session.get('login_row_data', {}).get('Name', 'Unknown')
        deleted_item.append(current_date_time)  # Adding current date and time to the deleted item's data
        deleted_item.append(name)
        # Open the existing "deleted_items.xlsx" workbook
        try:
            wb_deleted = openpyxl.load_workbook('Excel/deleted_items.xlsx')
        except FileNotFoundError:
            # If the file doesn't exist, create a new workbook
            wb_deleted = openpyxl.Workbook()
        
        ws_deleted = wb_deleted.active
        # Append the deleted item's data to the existing content
        ws_deleted.append(deleted_item)
        wb_deleted.save('Excel/deleted_items.xlsx')
        print("Item deleted successfully!")
    else:
        print("No such entry found!")

    return "Item deleted successfully!" if entry_found else "No such entry found!"



@app.route('/data')
def agset_data():
    try:
        # Read Excel file
        df = pd.read_excel('Excel/data.xlsx')
        df = df.replace({np.nan: ''})

        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        print("This is dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,", data)
        return jsonify(data)
    except Exception as e:
        print(e)  # Print the error for debugging purposes
        return {'error': 'Internal Server Error'}, 500  # Return a 500 status code and an error message




@app.route('/handover_form', methods=['POST'])
def handover_form():
    # Access the form data
    project_name = request.form['projectName']
    origin_site = request.form['originSite']
    destination_site = request.form['destinationSite']
    handover_person_name = request.form['handoverPersonName']
    receiver_person_name = request.form['receiverPersonName']
    count = int(request.form['count'])
    product_names = request.form.getlist('productName')
    conditions = request.form.getlist('Condition')
    remarks = request.form.getlist('remarks')


    # Printing the received data
    print("Project Name:", project_name)
    print("Origin Site:", origin_site)
    print("Destination Site:", destination_site)
    print("Handover Person Name:", handover_person_name)
    print("Receiver Person Name:", receiver_person_name)
    print("Count:", count)
    for i in range(count):
        print(f"Product {i+1}: {product_names[i]}")
        print(f"Condition {i+1}: {conditions[i]}")
        print(f"Remarks {i+1}: {remarks[i]}")
        
    
    # Here you can process the received data further, such as saving it to a database
    
    return "Form submitted successfully"



def send_to_excel(data):
    try:
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)
        
        # Save DataFrame to Excel
        df.to_excel('Excel/dashboard.xlsx', index=False)
        
        return {"message": "Data sent to dashboard.xlsx successfully!"}
    except Exception as e:
        return {"error": "Error saving data to Excel: {}".format(e)}


@app.route('/send_data', methods=['POST'])
def receive_data_from_form():
    json_data = request.json
    print(json_data)
    if not json_data:
        return jsonify({"error": "No JSON data received"})
    
    result = send_to_excel(json_data)
    return jsonify(result)


@app.route('/receive_data')
def read_excel_table():
    # Replace "output.xlsx" with the actual file path
    file_path = r"Excel/dashboard.xlsx"
    print("congrats and hushh we reached here f08`qaqaeor drones table ")
    try:
        print("hahah")
        # Read Excel file, skipping the first row (header) and starting from row 2
        data_df = pd.read_excel(file_path, skiprows=1, header=None)

        # Replace empty values with 'NAN'
        data_df.fillna('', inplace=True)

        total_rows = data_df.shape[0]  # Access the first element of the shape tuple

        print("Total number of rows:", total_rows)

        # Convert DataFrame to JSON and return
        print(data_df)
        return jsonify(data_df.values.tolist())
    except Exception as e:
        return jsonify({'error': str(e)})






