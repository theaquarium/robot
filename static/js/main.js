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
function command(cmd) {
    if (cmd && cmd != lastCommand) {
        console.log(cmd);
        const xmlHttp = new XMLHttpRequest();
        xmlHttp.open('GET', '/api/command/' + cmd, true);
        xmlHttp.send(null);
        lastCommand = cmd;
    }
}

// Get Motions Function
function show_motions() {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var motions = xmlHttp.responseText;
            document.getElementById('motions').innerHTML = motions;
        }
    };
    xmlHttp.open('GET', '/api/motions/', true);
    xmlHttp.send(null);
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
    command(directionMap[direction]);
}

function buttonMouseUp() {
    command('stop');
}

function buttonKeyDown(event) {
    switch(event.key) {
        case 'ArrowUp':
            command('forward');
            activeButton('up');
            break;
        case 'ArrowDown':
            command('back');
            activeButton('down');
            break;
        case 'ArrowLeft':
            command('left');
            activeButton('left');
            break;
        case 'ArrowRight':
            command('right');
            activeButton('right');
            break;
    }
}

function buttonKeyUp() {
    command('stop');
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
        command(directionMap[direction]);
    }).on('end', event => {
        command('stop');
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


setInterval(function () {
    show_motions();
}, 3000);
