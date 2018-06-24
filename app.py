from flask import Flask, render_template
from robot import Robot

app = Flask(__name__)
robot = Robot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command/<string:cmd>', methods=['GET'])
def commands(cmd):
    print('=== Received command: {}'.format(cmd));
    mth = getattr(robot, cmd, '')
    if mth != '':
        mth()
    return '';

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)