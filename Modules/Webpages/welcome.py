@app.route('/get_username')
def get_username():

    name = session.get('login_row_data', {}).get('Name', 'Unknown')


    return jsonify({'username': name})
        # Get the name from session data