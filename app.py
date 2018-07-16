import sys
from flask import Flask, render_template
from robot import Robot

app = Flask(__name__, static_url_path='/static', static_folder='static')
robot = Robot()

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/static/<path:path>')
#def send_static(path):
#    return send_from_directory('static', path)

@app.route('/api/command/<string:cmd>', methods=['GET'])
def commands(cmd):
    print('=== Received command: {}'.format(cmd));
    mth = getattr(robot, cmd, '')
    if mth != '':
        mth()
    return '';

if __name__ == '__main__':
    port = 80
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port)
