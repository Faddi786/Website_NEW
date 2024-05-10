

'''
global extracted_rows
extracted_rows = None

@app.route('/render_receiver')
def render_receiver():
    global extracted_rows
    form_id = request.args.get('formNo')  # Get the value from the URL query parameter
    if form_id:
        extracted_rows = extract_rows_from_excel(form_id)  # Call the function with the extracted form_id
        print("this is the extracted rows from render receiver", extracted_rows)
    else:
        return "Form ID not provided."

    return render_template('Modules/Main/Reciever/form_data.html')

'''

'''



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


'''


'''
@app.route('/approve_receive_request', methods=['POST'])
def approve_receive_request():
    form_data = request.json  # Assuming the form data is sent as JSON
    print("This is the approve_receive_request form data",form_data)
    
    # Open handover_data.xlsx
    excel_file = "Excel/handover_data.xlsx"
    df = pd.read_excel(excel_file)

    # Check if there is any form data
    if form_data:
        product_ids = [item['ProductID'] for item in form_data]
        df = df[~df['ProductID'].isin(product_ids)]  # Remove rows with matching product IDs

        # Save the updated DataFrame back to the Excel file
        df.to_excel(excel_file, index=False)

    return "Data updated successfully."

'''

'''
def extract_rows_from_excel(serial_number, less_df):

    df = less_df
    print("this is the less df", less_df)
    print("this is the serial number we are trying to find in the df", serial_number)


    # Convert "Serial No" column to strings
    df["Serial"] = df["Serial"].astype(str)


    # Extract values from the Serial column
    serial_values = df["Serial"].tolist()
    
    # Correct versions
    corrected_serial_values = correct_versions(serial_values)
    
    # Update the Serial column with corrected values
    df["Serial"] = corrected_serial_values
    

    
    # Filter rows based on serial number
    filtered_df = df[df["Serial"].str.startswith(str(serial_number) + ".")]

    # Replace NaN values with "Nan"
    filtered_df.fillna("Nan", inplace=True)
    
    print("This is the filtered df", filtered_df)
    return filtered_df.to_dict(orient="records")
'''


'''




def extract_rows_first_filter(excel_file, column_name, value):
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print("Excel file not found.")
        return None, None
    except Exception as e:
        print("An error occurred while loading the Excel file:", e)
        return None, None
    
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in the Excel file.")
        return None, None

    # Replace all NaN values in the DataFrame with 'NAN'
    df = df.fillna('nan')

    # Convert both the DataFrame values and the comparison value to lowercase
    df[column_name] = df[column_name].str.lower().str.strip()
    value = value.lower().strip()


    #print("this is the excel data", df)
    print("this column name", column_name)
    print("this is the value we are searching", value)

    filtered_df = df[df[column_name] == value]
    print("lets see this dataframe", filtered_df)
    # Count unique values in the 'FormID' column
    form_id_count = filtered_df['FormID'].nunique()
    
    return filtered_df, form_id_count

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
'''


'''
global extracted_rows_data
extracted_rows_data = None

@app.route('/get_list', methods=['GET'])
def get_list():

    global extracted_rows_data

    # Retrieve the text sent in the query parameter
    text_data = request.args.get('text', '')
    excel = "Excel/handover_data.xlsx"

    if text_data == "Approve Sender Form":
        column_name = "FromProject"
        project = session.get('login_row_data', {}).get('Project', 'Unknown')
        print("this is the project name value that we are trying to search",project)
        extracted_rows_data, form_id_count = extract_rows_first_filter(excel, column_name, project)
        print("This is the extracted rows data from the first filter",extracted_rows_data)
        return str(form_id_count)

    elif text_data == "Receiver Form":
        column_name = "ToPerson"
        project = session.get('login_row_data', {}).get('Name', 'Unknown')
        print("this is the project name value that we are trying to search",project)
        extracted_rows_data, form_id_count = extract_rows_first_filter(excel, column_name, project)
        print("This is the extracted rows data from the first filter",extracted_rows_data)
        return str(form_id_count)

    elif text_data == "Approve Receiver Form":
        column_name = "ToProject"
        project = session.get('login_row_data', {}).get('Project', 'Unknown')
        print("this is the project name value that we are trying to search",project)
        extracted_rows_data, form_id_count = extract_rows_first_filter(excel, column_name, project)
        print("This is the extracted rows data from the first filter",extracted_rows_data)
        return str(form_id_count)

    else:
        # Handle case when text doesn't match any condition
        total_rows = "Unknown text"

    return str(total_rows)

'''

