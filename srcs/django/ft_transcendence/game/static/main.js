// import * as THREE from './threejs/src/Three.js';
// import { Group } from './threejs/src/Three.js';

// Network interractions //
const socket = new WebSocket('ws://' + window.location.host + '/ws/game/');

let othrUsers = [];
let positionX = 0;
let borderSize = 5;
let userPartyId = 0;
let thisUser;

function updatePos(userId)
{
	// actualiser la position du joueur concerné
	socket.addEventListener('message', function (event) {
		const data = JSON.parse(event.data);
		if (elem.userId == userPartyId)
			return (elem.posx);
		return (0);
			// console.log('Message from server ', event.data);
	});
		// return (1);
	return (positionX);
	// return (othrUsers[userId].posx);
}

function sendPos(data)
{
	socket.addEventListener('open', function (event) {
		console.log('connected');
		// console.log(JSON.stringify(data));
		socket.send(JSON.stringify(data));
	});
}

// ---------------------------------------------------------------------------------- //

// Keys interractions //

const keys = {
  left: false,
  right: false
};

document.addEventListener('keydown', handleKeyDown);
document.addEventListener('keyup', handleKeyUp);

function handleKeyDown(event)
{
	if (event.key === 'ArrowLeft')
		keys.left = true;
	else if (event.key === 'ArrowRight')
		keys.right = true;
}

function handleKeyUp(event)
{
	if (event.key === 'ArrowLeft')
		keys.left = false;
	else if (event.key === 'ArrowRight')
		keys.right = false;
}

// ---------------------------------------------------------------------------------- //

// Mise en place three.js

const scene = new THREE.Scene();

// TO DO: create mutiple cameras and attribute to apropriate user
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// console.log(user)

let radius = borderSize / (2 * Math.tan(Math.PI / mapSetting.nbPlayer)) * 2 + 3;
let angle = 360 / (mapSetting.nbPlayer * 2);

for (const el of mapSetting.listOfPlayer)
{
	userPartyId++;
	if (user == el.user)
		break;
	angle += 360 / mapSetting.nbPlayer;
}

console.log("angle: " + angle)
camera.position.x = Math.sin(angle * Math.PI / 180) * radius;
camera.position.z = Math.cos(angle * Math.PI / 180) * radius;
camera.position.y = 2;
// console.log(camera.position);
// ---------------------------------------------------------------------------------- //

// Utilisation de webgl
// const renderer = new THREE.WebGLRenderer();
const renderer = new THREE.WebGLRenderer({antialias: true});
// const renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});

// 
// window size
renderer.setSize(window.innerWidth - 15, window.innerHeight - 16);
// renderer.setSize(window.innerWidth - 80, window.innerHeight - 60);
// ---------------------------------------------------------------------------------- //

const sceneBox = document.getElementById('scene-box');
sceneBox.appendChild(renderer.domElement);


// creation du plane qui sert de sol
const planeGeometry = new THREE.PlaneGeometry(100, 100);
planeGeometry.rotateX(Math.PI / 180 * -90);
const planeMaterial = new THREE.MeshBasicMaterial({color: 0xa04000});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
scene.add(plane);
// ---------------------------------------------------------------------------------- //

// creation du brouillard
// const fogColor = "#000000";
// const fogNear = 2;
// const fogFar = 20;
// scene.fog = new THREE.Fog(fogColor, fogNear, fogFar);
// ---------------------------------------------------------------------------------- //


// initialisation des borders, users et ball
const threeJsShape = []

angle = 0; // -> 3 pl
let borderAngle = 0;
// let playerAngle = 45;
let playerAngle = 360 / (mapSetting.nbPlayer * 2);

let iter = 0;

const UsersGroup = new THREE.Group();
const BordersGroup = new THREE.Group();
scene.add(UsersGroup);
scene.add(BordersGroup);

for (const el of shapes) {
	const {party_id, item_id, type, color, posx, posy} = el;
	let geometry;
	
	switch (type) {
		case 1:
			geometry = new THREE.BoxGeometry(borderSize, 1, 0.1);
			borderAngle += 360 / mapSetting.nbPlayer;
			angle = borderAngle;
			break;
		case 2:
			geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
			playerAngle += 360 / mapSetting.nbPlayer;
			angle = playerAngle;
			break;
		case 3:
			geometry = new THREE.SphereGeometry(0.2);
			break;
	}
				
	// if (type == 2 && iter == userPartyId)
	// {
	// 	// color = "#ff0000";
	// 	console.log(color);
	// }
	
	// choix du shader
	const material = new THREE.MeshPhongMaterial({color: color});
	// 
	const shape = new THREE.Mesh(geometry, material);
	let rradius = borderSize / (2 * Math.tan(Math.PI / mapSetting.nbPlayer)) * 2;
	shape.position.x = Math.cos(angle * Math.PI / 180) * rradius;
	shape.position.z = Math.sin(angle * Math.PI / 180) * rradius;
	shape.lookAt(new THREE.Vector3(0, 0, 0));
	
	if (type == 1)
	BordersGroup.add(shape);
else if (type == 2)
{
		iter++;
		shape.name = iter;
		UsersGroup.add(shape);
	}
	else
		scene.add(shape);
	// threeJsShape.push(shape);
}
// ---------------------------------------------------------------------------------- //


// Lumieres
const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
ambientLight.position.set(camera.position.x, camera.position.y, camera.position.z);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(1, 2, 3);
scene.add(directionalLight);

// ---------------------------------------------------------------------------------- //

camera.lookAt(new THREE.Vector3(0, 0, 0));

// console.log(UsersGroup);

// console.log("UserGroup");
// console.log(UsersGroup.children);
// console.log(scene);
// console.log("UserGroup end");

const animate = () => {
	let it = 0;

	UsersGroup.children.forEach((elem) => {
	if (elem.name == userPartyId)
	{
		if (keys.left)
			positionX -= 0.1;
		else if (keys.right)
			positionX += 0.1;
		// console.log({'userId': userPartyId , 'posx': positionX});
		sendPos(JSON.stringify({'userId': userPartyId , 'posx': positionX}));
	}
	elem.position.x = updatePos();
		// actualiser la position du joueur concerné
	});
	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}

animate();
