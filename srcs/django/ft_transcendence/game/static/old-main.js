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
        // 'session_id': document.getElementById('session_id').value,
        // 'player_id': document.getElementById('player_id').value,
    };
	// updatePlayerKey("hgeissle", event.key, true);
	// socket.send("keydown");
    socket.send(JSON.stringify(data));
}

function handleKeyUp(event) {
    const data = {
        'type': 'playerPaddleUpdate',
        'event': 'keyup',
        'key': event.key
        // 'session_id': document.getElementById('session_id').value,
        // 'player_id': document.getElementById('player_id').value,
    };
	// updatePlayerKey("hgeissle", event.key, false);
	// socket.send("keyup");
    socket.send(JSON.stringify(data));
}

socket.onmessage = function(event) {
	// console.log(event.data);
    const data = JSON.parse(event.data);
	if (data.type == 'initObject')
	{
		shapesObj = data.shapes;
		shapes = JSON.parse(shapesObj);
		// console.log(shapesObj);
		loadShapes(shapes);
	}
    if (data.type == 'playerPaddleUpdate')
    {
		const playerId = data.player;
		const key = data.key;
		const value = data.event;
		console.log(playerId, key, value);
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
let radius = (mapSetting.nbPlayer > 2) ? borderSize / (2 * Math.tan(Math.PI / mapSetting.nbPlayer)) * 2 + 3 : 5;
let angle = (360 / mapSetting.nbPlayer) * userPartyId + (360 / mapSetting.nbPlayer) / 2;

camera.position.x = Math.cos(angle * Math.PI / 180) * radius;
camera.position.z = Math.sin(angle * Math.PI / 180) * radius;
camera.position.y = 3;
camera.lookAt(new THREE.Vector3(0, 0, 0));
// console.log(camera.position);
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

// --------------- Load GLB Ball ---------------------------------------------------- //
/*
// let loader = new THREE.GLTFLoader();
const loader = new threeGltfLoader();
loader.load('/static/game/object/torus.glb', (gltf) => {
	scene.add(glhf.scene);
});*/
// ---------------------------------------------------------------------------------- //


const sceneBox = document.getElementById('scene-box');
sceneBox.appendChild(renderer.domElement);


const planeGeometry = new THREE.CylinderGeometry(radius, radius, 0.1, mapSetting.nbPlayer * 2);

const planeMaterial = new THREE.MeshPhongMaterial({color: 0x5f5f5f});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.position.y = -0.3;
scene.add(plane);
// ---------------------------------------------------------------------------------- //

// creation du brouillard
// const fogColor = "#505050";
// const fogNear = 20;
// const fogFar = 2000;
// scene.fog = new THREE.Fog(fogColor, fogNear, fogFar);
// ---------------------------------------------------------------------------------- //


// initialisation des borders, users et ball
const threeJsShape = []

angle = 0; // -> 3 pl
let borderAngle = 0;
// let playerAngle = 45;
let playerAngle = 360 / (mapSetting.nbPlayer * 2);

const UsersGroup = new THREE.Group();
const BordersGroup = new THREE.Group();
scene.add(UsersGroup);
scene.add(BordersGroup);

function loadShapes(shapes)
{
	for (const el of shapes) {
		const {pparty_id, item_id, type, color, posx, posy} = el;
		let geometry;
		
		// console.log(type);
		switch (type) {
			case 1:
				geometry = new THREE.BoxGeometry(borderSize, 1, 0.1);
				borderAngle = (360 / mapSetting.nbPlayer) * item_id;
				angle = borderAngle;
				break;
			case 2:
				geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
				playerAngle = (360 / mapSetting.nbPlayer) * item_id + (360 / mapSetting.nbPlayer) / 2;
				angle = playerAngle;
				break;
			case 3:
				geometry = new THREE.SphereGeometry(0.2);
				break;
		}
					
		// choix du shader
		
		let material;
		
		if (type == 2 && item_id == userPartyId)
		{
			material = new THREE.MeshPhongMaterial({color: "#ff0000"});
			positionX = angle;
		}
		else
		material = new THREE.MeshPhongMaterial({color: color});
		
		
		const shape = new THREE.Mesh(geometry, material);
		let rradius = (mapSetting.nbPlayer > 2) ? borderSize / (2 * Math.tan(Math.PI / mapSetting.nbPlayer)) * 2 : 2.5;
		rradius += (type == 2) ? 1 : 0;
		shape.position.x = Math.cos(angle * Math.PI / 180) * rradius;
		shape.position.z = Math.sin(angle * Math.PI / 180) * rradius;
		shape.lookAt(new THREE.Vector3(0, 0, 0));
			
		if (type == 1)
		BordersGroup.add(shape);
		else if (type == 2)
		{
			shape.name = item_id;
			UsersGroup.add(shape);
		}
		else
		{
			shape.position.x = 0;
			shape.position.z = 0;
			scene.add(shape);
		}
		console.log(shape.position);
		// threeJsShape.push(shape);
	}
}
// ---------------------------------------------------------------------------------- //

// ---------------------------------------------------------------------------------- //

function loadNames(gusers)
{
	gusers.forEach(guser => {
		var div = document.createElement('div');
		
	});

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

function g_start()
{
	console.log("message");
}

// ---------------------------------------------------------------------------------- //

loadSkybox();
loadShapes([]);

// ---------------------------------------------------------------------------------- //


let nbPlayerCount = 0;
mapSetting.listOfPlayer.forEach((usr) => {nbPlayerCount++});

try {
	console.log(UsersGroup.children);
	UsersGroup.children.forEach((elem) => {
		if (!mapSetting.listOfPlayer[elem.name])
			throw ("empty");
		thisUser = (mapSetting.listOfPlayer[elem.name]).user;
		offsetX[thisUser] = parseInt(elem.name) * (360 / nbPlayerCount);
		console.log("Offset for", thisUser, "is", offsetX[thisUser]);
	})
}
catch (e)
{
	console.error(e);
	console.log("ERROR");
}

const animate = () => {
	let it = 0;
	let radius = (borderSize / (2 * Math.tan(Math.PI / mapSetting.nbPlayer)) * 2) + 0.0 + 10 / (mapSetting.nbPlayer ** 2);
	
	if (mapSetting.nbPlayer == nbPlayerCount)
	{
		try {
			UsersGroup.children.forEach((elem) => {
				// console.log(elem.position);
				// console.log(mapSetting.listOfPlayer.filter(x => x==2).length);
				thisUser = (mapSetting.listOfPlayer[elem.name]).user;
				// console.log("this user:", thisUser, "offset:", offsetX[thisUser]);
				if (playerKeys[thisUser].ArrowLeft && offsetX[thisUser] < (16 - parseInt(mapSetting.nbPlayer) + 2))
				{
					offsetX[thisUser] += 3 / radius;
					console.log("Left");
				}
				else if (playerKeys[thisUser].ArrowRight && offsetX[thisUser] > (-16 + parseInt(mapSetting.nbPlayer) - 2))
				{
					offsetX[thisUser] -= 3 / radius;
					console.log("Right");
				}
				// elem.position.x = 0;
				elem.position.x = Math.cos((parseInt(positionX) + parseInt(offsetX[thisUser])) * Math.PI / 180) * radius;
				console.log(elem.position.x);
				// elem.position.z = 0;
				console.log(offsetX[thisUser]);
				elem.position.z = Math.sin((parseInt(positionX) + parseInt(offsetX[thisUser])) * Math.PI / 180) * radius;
				console.log(elem.position.z);
				elem.lookAt(new THREE.Vector3(0, 0, 0));
			});
		}
		catch (e)
		{
			console.error(e);
		}
	}
	else
	{
		// vue du lobby en mode attente
		// if (ready < nb.player)
		// {
			radius = 30;
			camera.position.x = Math.sin(angle * Math.PI / 180) * radius;
			camera.position.z = Math.cos(angle * Math.PI / 180) * radius;
			camera.position.y = 5;
			angle += 0.1;
		// }
	}

	camera.lookAt(new THREE.Vector3(0, 0, 0));

	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}

animate();