from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command/<string:cmd>', methods=['GET'])
def commands(cmd):
    print('=== Received command: {}'.format(cmd));
    return '';

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8094)
