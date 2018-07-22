import sys
import json
from flask import Flask, render_template
from robot import Robot

app = Flask(__name__, static_url_path='/static', static_folder='static')
robot = Robot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command/<string:cmd>', methods=['GET'])
def command(cmd):
    print('- {}: Received command: {}'.format('App', cmd));
    mth = getattr(robot, cmd, '')
    if mth != '':
        mth()
    return '';

@app.route('/api/motions/', methods=['GET'])
def motions():
    motions = robot.get_motions()
    return json.dumps(motions)

if __name__ == '__main__':
    port = 80
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port)
