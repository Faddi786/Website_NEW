from flask import Flask, request, jsonify
import subprocess
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mail.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.form.to_dict()

    # Extract attachments
    attachments = request.files.getlist("attachments")

    # Create a temporary directory to store attachments
    temp_dir = "temp_attachments"
    os.makedirs(temp_dir, exist_ok=True)

    attachment_paths = []
    for attachment in attachments:
        attachment_path = os.path.join(temp_dir, attachment.filename)
        attachment.save(attachment_path)
        attachment_paths.append(attachment_path)

    # Call the sendm.py script with the provided parameters
    email_script = 'sendm.py'
    recipient_email = data.get('to')
    sender_email = data.get('from')
    password = data.get('password')
    subject = data.get('subject')
    message = data.get('message')

    # Call the script using subprocess
    subprocess.run(['python', email_script, sender_email, password, recipient_email, subject, message, attachment_paths] )

    return jsonify({'message': 'Email sent successfully'})

if __name__ == '__main__':
    app.run(debug=True)
