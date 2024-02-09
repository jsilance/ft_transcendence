const socket = new WebSocket('ws://' + window.location.host + '/ws/game/');

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

function handleKeyDown(event) {
    const data = {
        'type': 'paddle',
        'event': 'keydown',
        'key': event.key,
        'session_id': document.getElementById('session_id').value,
        'player_id': document.getElementById('player_id').value,
    };
    socket.send(JSON.stringify(data));
};

function handleKeyUp(event) {
    const data = {
        'type': 'paddle',
        'event': 'keyup',
        'key': event.key,
        'session_id': document.getElementById('session_id').value,
        'player_id': document.getElementById('player_id').value,
    };
    socket.send(JSON.stringify(data));
}

// Keys interractions //

const keys = {
	left: false,
	right: false
};

function updateKeyDown(data)
{
	if (data.key === 'ArrowLeft')
	    keys.left = true;
	else if (data.key === 'ArrowRight')
	    keys.right = true;
}

function updateKeyUp(data)
{
	if (data.key === 'ArrowLeft')
	    keys.left = false;
	else if (data.key === 'ArrowRight')
	    keys.right = false;
}

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type == 'paddle')
    {
        if (data.event == 'keydown')
            updateKeyDown(data.key);
        if (data.event == 'keyup')
            updateKeyUp(data.key);
    }
    if (data.type == 'ball')
    {
        const ball = data.ball;
    }
    if (data.type == 'score')
    {
        const score = data.score;
    }
    if (data.type == 'winner')
    {
        const winner = data.winner;
    }
    if (data.type == 'game_over')
    {
        const game_over = data.game_over;
    }
};