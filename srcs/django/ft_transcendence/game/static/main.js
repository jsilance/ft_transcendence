// import * as THREE from './threejs/src/Three.js';
import threeGltfLoader from 'https://cdn.skypack.dev/pin/three-gltf-loader@v1.111.0-nljU36r8PRJpg81IWD7g/mode=imports/optimized/three-gltf-loader.js';

// Network interractions //
const socket = new WebSocket('ws://' + window.location.host + '/ws/game/');

let othrUsers = [];
let positionX = 0;
let borderSize = 5;
let userPartyId = 0;
let thisUser;
let shapesObj = [];
let shapes = [];

// Keys interraction //

let i = 0;
const playerKeys = {};

// add player and define id of player
for (const el of mapSetting.listOfPlayer)
{
	i++;
	if (user == el.user)
	{
		userPartyId = i;
	}
	addPlayer(el.user);
	console.log(el.user);
}

// Function to initialize keys for a new player
function addPlayer(playerId) {
    playerKeys[playerId] = {
        ArrowLeft: false,
        ArrowRight: false
    };
}

// ----------Gestion socket et communication--------------------------------------------------------------------- //

function updatePlayerKey(playerId, key, value) {
    if (playerKeys[playerId]) {
		if (value == "keydown")
        	playerKeys[playerId][key] = true;
		if (value == "keyup")
			playerKeys[playerId][key] = false;
    }
}

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

function handleKeyDown(event) {
    const data = {
        'type': 'playerPaddleUpdate',
        'event': 'keydown',
        'key': event.key
    };
    socket.send(JSON.stringify(data));
}

function handleKeyUp(event) {
    const data = {
        'type': 'playerPaddleUpdate',
        'event': 'keyup',
        'key': event.key
    };
    socket.send(JSON.stringify(data));
}

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
	if (data.type == 'initObject')
	{
		shapesObj = data.shapes;
		shapes = JSON.parse(shapesObj);
		loadShapes(shapes);
	}
    if (data.type == 'playerPaddleUpdate')
    {
		const playerId = data.player;
		const key = data.key;
		const value = data.event;
		updatePlayerKey(playerId, key, value);
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

socket.onopen = function(e) {
	console.log("Connection etablished!");
	socket.send(JSON.stringify({
		'type': 'initObject',
		'id': party_id
	}));
};

socket.onerror = function(e) {
	console.error('Socket encountered error: ', e.message, 'Closing socket');
	socket.close();
};

socket.onclose = function(e) {
    console.error('Socket closed unexpectedly. Attempting to reconnect...');
    setTimeout(function() {
        // Implement reconnection logic here
    }, 1000); // Adjust delay and implement exponential backoff
};
// -------------------------------------------------------------------------------------------------------------- //

// Mise en place three.js

const scene = new THREE.Scene();


const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

camera.position.x = 0;
camera.position.z = 0;
camera.position.y = 10;
camera.lookAt(new THREE.Vector3(0, 0, 0));
// ---------------------------------------------------------------------------------- //

const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight - 80);

// ---------------------------------------------------------------------------------- //

// --------------- Load skybox ------------------------------------------------------ //

function loadSkybox()
{

	let skyboxMaterial = [];

	let texture_ft = new THREE.TextureLoader().load('/static/game/object/mystic_ft.jpg');
	let texture_bk = new THREE.TextureLoader().load('/static/game/object/mystic_bk.jpg');
	let texture_up = new THREE.TextureLoader().load('/static/game/object/mystic_up.jpg');
	let texture_dn = new THREE.TextureLoader().load('/static/game/object/mystic_dn.jpg');
	let texture_rt = new THREE.TextureLoader().load('/static/game/object/mystic_rt.jpg');
	let texture_lf = new THREE.TextureLoader().load('/static/game/object/mystic_lf.jpg');
	
	skyboxMaterial.push(new THREE.MeshBasicMaterial({map: texture_ft}));
	skyboxMaterial.push(new THREE.MeshBasicMaterial({map: texture_bk}));
	skyboxMaterial.push(new THREE.MeshBasicMaterial({map: texture_up}));
	skyboxMaterial.push(new THREE.MeshBasicMaterial({map: texture_dn}));
	skyboxMaterial.push(new THREE.MeshBasicMaterial({map: texture_rt}));
	skyboxMaterial.push(new THREE.MeshBasicMaterial({map: texture_lf}));
	
	for (let i = 0; i < 6; i++)
	skyboxMaterial[i].side = THREE.BackSide;
	
	let skyboxGeo = new THREE.BoxGeometry(1000, 1000, 1000);
	let skybox = new THREE.Mesh(skyboxGeo, skyboxMaterial);
	scene.add(skybox);
}

// ---------------------------------------------------------------------------------- //

const sceneBox = document.getElementById('scene-box');
sceneBox.appendChild(renderer.domElement);

const plane = new THREE.Mesh(
	new THREE.BoxGeometry(20, 0, 15),
	new THREE.MeshPhongMaterial({
		color: 0x5f5f5f,
		side: THREE.DoubleSide
	})
);
plane.position.y = -0.3;
scene.add(plane);
// ---------------------------------------------------------------------------------- //

// initialisation des borders, users et ball

function loadShapes()
{
	// Players --------------------------------
	let player1 = new THREE.Mesh(
		new THREE.BoxGeometry(0.2, 0.5, 3),
		new THREE.MeshPhongMaterial({
			color: 0x5f005f,
			side: THREE.DoubleSide
		})
	);
	player1.name = "player1";
	player1.position.x = -9;
	player1.position.y = 0.5;
	player1.position.z = 0; //playerpos
	scene.add(player1);
	
	
	let player2 = new THREE.Mesh(
		new THREE.BoxGeometry(0.2, 0.5, 3),
		new THREE.MeshPhongMaterial({
			color: 0x5f005f,
			side: THREE.DoubleSide
		})
	);
	player2.name = "player2";
	player2.position.x = 9;
	player2.position.y = 0.5;
	player2.position.z = 0; //playerpos
	scene.add(player2);
	// ---------------------------------------
	
	// Borders --------------------------------
	let bordeurUp = new THREE.Mesh(
		new THREE.BoxGeometry(20, 0.5, 0.1),
		new THREE.MeshPhongMaterial({
			color: 0x9f9f9f,
			side: THREE.DoubleSide
		})
		);
		bordeurUp.name = "borderUp";
		bordeurUp.position.x = 0;
		bordeurUp.position.y = 0;
		bordeurUp.position.z = 7.2;
		scene.add(bordeurUp);
		
		
		let borderDown = new THREE.Mesh(
			new THREE.BoxGeometry(20, 0.5, 0.1),
			new THREE.MeshPhongMaterial({
				color: 0x9f9f9f,
				side: THREE.DoubleSide
			})
		);
		borderDown.name = "borderDown";
		borderDown.position.x = 0;
		borderDown.position.y = 0;
		borderDown.position.z = -7.2;
		scene.add(borderDown);
		// ---------------------------------------
		
		// Ball
		
		let ball = new THREE.Mesh(
			new THREE.SphereGeometry(0.2),
			new THREE.MeshPhongMaterial({
				color: 0x9f9f00,
				side: THREE.DoubleSide
			})
		);
		ball.name = "ball";
		ball.position.x = 0; //ballpos
		ball.position.y = 0.5;
		ball.position.z = 0; //ballpos
		scene.add(ball);
		// ---------------------------------------
}

// ---------------------------------------------------------------------------------- //


// Lumieres
const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
ambientLight.position.set(camera.position.x, camera.position.y, camera.position.z);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(1, 2, 3);
// scene.add(directionalLight);

// ---------------------------------------------------------------------------------- //

let offsetX = [];

// ---------------------------------------------------------------------------------- //

loadSkybox();
loadShapes();

// ---------------------------------------------------------------------------------- //


let nbPlayerCount = 0;
mapSetting.listOfPlayer.forEach((usr) => {nbPlayerCount++});

const animate = () => {
	let it = 0;
	let radius = (borderSize / (2 * Math.tan(Math.PI / mapSetting.nbPlayer)) * 2) + 0.0 + 10 / (mapSetting.nbPlayer ** 2);
	
	// if (mapSetting.nbPlayer == nbPlayerCount)
	// {
		try {
			
		}
		catch (e)
		{
			console.error(e);
		}
	// }

	camera.lookAt(new THREE.Vector3(0, 0, 0));

	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}

animate();