import sys
import json
from flask import Flask, render_template
from robot import Robot

app = Flask(__name__, static_url_path='/static', static_folder='static')
robot = Robot('robot')

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

@app.route('/api/trajectory/', methods=['GET'])
def trajectory():
    trajectory = robot.get_trajectory()
    return json.dumps(trajectory)

if __name__ == '__main__':
    port = 80
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
