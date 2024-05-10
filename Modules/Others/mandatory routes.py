@app.route('/get_username')
def get_username():

    name = session.get('login_row_data', {}).get('Name', 'Unknown')


    return jsonify({'username': name})
        # Get the name from session data

@app.route('/login', methods=['POST'])
def login():

    # Load the user_data Excel file
    user_data = pd.read_excel("Excel/login_details.xlsx")


    user_id = request.form['id']
    password = request.form['password']
    print(user_id,password)

    # Check if ID and password exist in the user_data DataFrame
    matched_rows = user_data[(user_data['ID'] == user_id) & (user_data['Password'] == password)]

    if not matched_rows.empty:
        # Extract type of account
        account_type = matched_rows.iloc[0]['Type Of Account']
        
        # Store the entire row data in session
        session['login_row_data'] = matched_rows.iloc[0].to_dict()
        print("this is session dataaa  ", session['login_row_data'])

        # Redirect based on account type
        if account_type == 'Manager':
            return redirect(url_for('manager'))

        elif account_type == 'Employee':
            return redirect(url_for('employee'))

        else:
            return "Unknown account type"

    else:
        return "Account not found"

