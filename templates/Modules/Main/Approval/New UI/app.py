from flask import Flask, request, jsonify
from flask import Flask, request, render_template, jsonify
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('approvalTable.html')

less_df = pd.DataFrame()  # Initialize less_df as an empty DataFrame

@app.route('/approval_table', methods=['GET'])
def approval_table():
    global less_df

    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('handover_data.xlsx')

    # Get the project from session data
    project = "SOI ASSAM"

    # Filter the DataFrame based on the parameters
    source_df = df[(df['FromProject'] == project) & (df["ApprovalToSend"] == "yes")]
    destination_df = df[(df['FromProject'] == project)].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Update columns in the DataFrames
    destination_df["ApprovalType"] = "Recieve"
    source_df["ApprovalType"] = "Send"

    # Append destination_df to source_df
    source_df = pd.concat([source_df, destination_df])

    # Sort the DataFrame based on "FormID"
    source_df = source_df.sort_values("FormID")

    # Convert the filtered data to JSON format
    json_data = source_df.to_json(orient='records')

    return json_data



@app.route('/product_details')
def product_details():
    return render_template('productDetails.html')


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


def extract_rows_from_excel(form_id):
    global less_df
    df = less_df
    print("this is the less df", less_df)
    print("this is the form ID we are trying to find in the df", form_id)

    # Filter rows based on form ID
    formid_filtered_df = df[df["FormID"] == form_id]

    if formid_filtered_df.empty:
        print("Form ID not found in the DataFrame")
        return []

    # Get the main digit from the first row where form ID matches
    main_digit = int(str(formid_filtered_df["Serial"].iloc[0]).split(".")[0])

    # Filter rows based on the main digit
    filtered_df = df[df["Serial"].astype(str).str.split(".").str[0] == str(main_digit)]

    # Replace NaN values with "Nan"
    filtered_df.fillna("Nan", inplace=True)

    print("This is the filtered df", filtered_df)
    return filtered_df.to_dict(orient="records")



extract_rows =[]
@app.route('/send_formid')
def send_formid():
    form_id = request.args.get('form_id')
    print("Received Form ID:", form_id)
    global extract_rows
    extract_rows = extract_rows_from_excel(form_id)
    # Do whatever you need to do with the form ID
    return "Form ID received successfully"


@app.route('/get_form_data_for_history')
def get_form_data_for_history():
    global extract_rows
    return jsonify(extract_rows)


@app.route('/form_data')
def form_data():
    return render_template('productDetails.html')



if __name__ == '__main__':
    app.run(debug=True)