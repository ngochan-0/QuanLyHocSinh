from app import app
from flask import render_template

@app.route('/', methods=['get'])
def home():
    return render_template('home.html')




@app.route('/login', methods=['post', 'get'])
def signin():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)