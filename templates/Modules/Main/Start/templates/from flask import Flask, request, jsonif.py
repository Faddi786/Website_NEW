from flask import Flask, request, jsonify
from flask import Flask, request, render_template, jsonify
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('transactionHistory.html')

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

global form_data
@app.route('/send_formid')
def send_formid():
    form_id = request.args.get('form_id')
    print("Received Form ID:", form_id)
    global form_data
    extract_rows = 
    # Do whatever you need to do with the form ID
    return "Form ID received successfully"


@app.route('/get_form_data_for_history')
def get_form_data_for_history():
    global form_data


@app.route('/form_data')
def form_data():
    return render_template('productDetails.html')

@app.route('/transaction_history', methods=['GET'])
def transaction_history():
    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('handover_data.xlsx')
    print("this is the excel data",df)
    # Get the parameters name and project from session data
    #name = request.args.get('name')
    #project = request.args.get('project')

    name = "Umar"
    project = "SOI ASSAM"

    # Filter the DataFrame based on the parameters
    filtered_data = df[(df['FromProject'] == project) | (df['FromPerson'] == name) | (df['ToProject'] == project) | (df['ToPerson'] == name)]
    filtered_data = filtered_data.dropna(subset=['FormID'])

    #print("this is the filtered data",filtered_data)
    
    # Convert the filtered data to JSON format
    json_data = filtered_data.to_json(orient='records')

    return json_data

if __name__ == '__main__':
    app.run(debug=True)