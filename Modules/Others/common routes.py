@app.route('/send_formid')
def send_formid():
    form_id = request.args.get('form_id')
    print("Received Form ID:", form_id)
    extract_rows_from_excel(form_id)
    # Do whatever you need to do with the form ID
    return "Form ID received successfully"


@app.route('/get_form_data')
def get_form_data():
    global filtered_df
    
    if filtered_df is None:
        print("Filtered DataFrame is not available")
        return jsonify([])

    # Convert DataFrame to JSON string and return
    json_data = filtered_df.to_dict(orient="records")
    return jsonify(json_data)