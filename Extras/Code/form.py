from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('handoverform.html')
    
@app.route('/page1')
def page1():
    return render_template('peritem.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
