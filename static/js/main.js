// Global Variables
const directionMap = {
    'up': 'forward',
    'down': 'back',
    'left': 'left',
    'right': 'right',
}
let manager;
let lastCommand;

// Send Command Function
function sendCommand(cmd) {
    if (cmd && cmd != lastCommand) {
        //console.log(cmd);
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.open('GET', '/api/command/' + cmd, true);
        xmlHttp.send(null);
        lastCommand = cmd;
    }
}

function sendCommandDelayed(cmd, delay) {
    setTimeout(function () {
        sendCommand(cmd);
    }, delay);
}

function sendSequence(lst) {
    let d = 0;
    lst.forEach(function (cmd) {
        sendCommandDelayed(cmd[0], d);
        d += cmd[1];
    });
    sendCommandDelayed('stop', d);
}

// Add Active Class To Button
function activeButton(buttonClass) {
    document.querySelector('.' + buttonClass).classList.add('button-active');
}

// Button Listeners
function buttonMouseDown() {
    let direction;
    const classes = this.classList.values();
    for(let className of classes) {
        if (className != 'button') direction = className;
    }
    sendCommand(directionMap[direction]);
}

function buttonMouseUp() {
    sendCommand('stop');
}

function buttonKeyDown(event) {
    switch(event.key) {
        case 'ArrowUp':
            sendCommand('forward');
            activeButton('up');
            break;
        case 'ArrowDown':
            sendCommand('back');
            activeButton('down');
            break;
        case 'ArrowLeft':
            sendCommand('left');
            activeButton('left');
            break;
        case 'ArrowRight':
            sendCommand('right');
            activeButton('right');
            break;
    }
}

function buttonKeyUp() {
    sendCommand('stop');
    document.querySelectorAll('.button-active').forEach(el => {
        el.classList.remove('button-active');
    });
}

// Joystick Functions
function activateJoystick() {
    manager = nipplejs.create({
        mode: 'static',
        zone: document.querySelector('.joystick'),
        position: {left: '50%', top: '50%'},
        restOpacity: 0.8,
    });

    manager.on('dir', (event, data) => {
        const direction = data.direction.angle;
        sendCommand(directionMap[direction]);
    }).on('end', event => {
        sendCommand('stop');
    });
}

function deactivateJoystick() {
    manager.destroy();
}

// Button Functions
function activateButtons() {
    document.querySelectorAll('.button').forEach(button => {
        button.addEventListener('mousedown', buttonMouseDown);
        button.addEventListener('mouseup', buttonMouseUp);
    });
    document.addEventListener('keydown', buttonKeyDown);
    document.addEventListener('keyup', buttonKeyUp);
}

function deactivateButtons() {
    document.querySelectorAll('.button').forEach(button => {
        button.removeEventListener('mousedown', buttonMouseDown);
        button.removeEventListener('mouseup', buttonMouseUp);
    });
    document.removeEventListener('keydown', buttonKeyDown);
    document.removeEventListener('keyup', buttonKeyUp);
}

// Toggle Switch Listener
document.querySelector('input[name=switch-input]').addEventListener('change', function() {
    if (this.checked) {
        // Remove Buttons
        deactivateButtons();
        document.querySelector('.buttons').classList.add('hidden');
        // Add Joystick
        document.querySelector('.joystick').classList.remove('hidden');
        activateJoystick();
    }
    else {
        // Remove Joystick
        deactivateJoystick();
        document.querySelector('.joystick').classList.add('hidden');
        // Add Buttons
        document.querySelector('.buttons').classList.remove('hidden');
        activateButtons();
    }
});

// Activate Buttons
activateButtons();

document.querySelector('#make_square').addEventListener('click', function() {
    let square = [];
    for (let i = 0; i < 4; i++) {
        square.push(['forward', 1000]);
        square.push(['right', 2000]);
    }
    sendSequence(square);
});

document.querySelector('#make_circle').addEventListener('click', function() {
    let circle = [];
    for (let i = 0; i < 32; i++) {
        circle.push(['forward', 250]);
        circle.push(['right', 250]);
    }
    sendSequence(circle);
});

// Get Motions Function
function showMotions() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let response = JSON.parse(xmlHttp.responseText);
            let trajectory = response.path;
            let angle = response.direction;

            // compute the boundaries to scale the trajectory
            let boundaries = [Infinity, Infinity, -Infinity, -Infinity]; // left, top, right, bottom
            trajectory.forEach(point => {
                boundaries[0] = Math.min(boundaries[0].toFixed(6), point[0]);
                boundaries[2] = Math.max(boundaries[2].toFixed(6), point[0]);
                boundaries[1] = Math.min(boundaries[1].toFixed(6), point[1]);
                boundaries[3] = Math.max(boundaries[3].toFixed(6), point[1]);
            });
            if (boundaries[2] === boundaries[0]) {
                boundaries[2] = boundaries[0] + 1;
            }
            if (boundaries[3] === boundaries[1]) {
                boundaries[3] = boundaries[1] + 1;
            }

            // compute the scaleing factors
            const svgElement = document.querySelector('#trajectory>svg');
            let scale = Math.min(
                svgElement.clientWidth * 0.9 / (boundaries[2] - boundaries[0]),
                svgElement.clientHeight * 0.9 / (boundaries[3] - boundaries[1])
            );
            let offset = [
                svgElement.clientWidth * 0.05 - boundaries[0] * scale,
                svgElement.clientHeight * 0.05 - boundaries[1] * scale
            ]

            // scale the trajectory
            let points = '';
            let last_point = [0, 0];
            trajectory.forEach(point => {
                let pt = computePosition(point, scale, offset);
                points += pt[0] + ',' + pt[1] + ' ';

                // remember the last point to draw the arrow
                last_point = pt;
            });

            // draw the trajectory
            document.getElementById('trajectory_path').setAttribute('points', points)

            // draw the pointer
            let transform = 'translate(' + (last_point[0] - 6) + ',' + last_point[1] + ') rotate(' + (angle + 90) + ' 6 0)'
            document.getElementById('trajectory_pointer').setAttribute('transform', transform);
        }
    };
    xmlHttp.open('GET', '/api/trajectory/', true);
    xmlHttp.send(null);
}

function computePosition(point, scale, offset) {
    return [
        point[0] * scale + offset[0],
        point[1] * scale + offset[1]
    ];
}

setInterval(function () {
    showMotions();
}, 1000);
