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
        console.log(cmd);
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.open('GET', '/api/command/' + cmd, true);
        xmlHttp.send(null);
        lastCommand = cmd;
    }
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

// Get Motions Function
function showMotions() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let trajectory = JSON.parse(xmlHttp.responseText).path;
            let points = '';

            const svgElement = document.querySelector('#trajectory>svg');

            trajectory.forEach(point => {
                const calculatedLocation = point;
                points += calculatedLocation[0] +
                    ',' +
                    calculatedLocation[1] +
                    ' ';

            command = 'L';
            });

            document.getElementById('trajectory_path').setAttribute('points', points);
        }
    };
    xmlHttp.open('GET', '/api/trajectory/', true);
    xmlHttp.send(null);
}

function computedPosition(svgElement, point) {
    return [
        (svgElement.clientHeight / 2) + point[0],
        (svgElement.clientWidth / 2) + point[1],
    ];
}

setInterval(function () {
    showMotions();
}, 3000);
