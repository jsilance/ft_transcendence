// Network interractions //
const socket = new WebSocket('ws://' + window.location.host + '/ws/game/');

let positionX = 0;

function updatePos()
{
	// actualiser la position du joueur concerné
	socket.addEventListener('message', function (event) {
		const data = JSON.parse(event.data);
		const text = data.message;
		positionX = data.posx;
		console.log(text);
		return (positionX);
	});
	return (positionX);
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

console.log(user)

let radius = 7;
let angle = 0;

if (user === 'root')
{
	angle = 0;
}
else
{
	angle = 45;
}

camera.position.x = Math.sin(angle) * radius;
camera.position.z = Math.cos(angle) * radius;
camera.position.y = 1;
console.log(camera.position);
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
const planeGeometry = new THREE.PlaneGeometry(10, 10);
planeGeometry.rotateX(Math.PI / 180 * -90);
const planeMaterial = new THREE.MeshBasicMaterial({color: 0x00f0f0});
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

// radius = 1 * mapSetting

for (const el of shapes) {
	const {party_id, item_id, type, color, posx, posy} = el;
	let geometry;
	
	switch (type) {
		case 1:
			geometry = new THREE.BoxGeometry(5, 0.1, 0.1);
			break;
		case 2:
			geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
			break;
		case 3:
			geometry = new THREE.SphereGeometry(0.2);
			break;
	}
	
	// choix du shader
	const material = new THREE.MeshPhongMaterial({color: color});
	// 
	const shape = new THREE.Mesh(geometry, material);
	
	shape.position.x = posx;
	shape.position.z = posy;
	console.log(type);

	// shape.position.x = Math.cos(360 / mapSetting.nbPlayer * Math.PI / 180) * radius;
	// console.log(Math.cos(360 / int(mapSetting.nbPlayer) * Math.PI / 180) * radius);
	// console.log(JSON.parse(mapSetting));
	console.log(mapSetting); //probleme ici avec \ necessaire pour le " -> voir db
	shape.position.y = 0.2;
	// shape.rotateY(item_id * (Math.PI / 180));
	// shape.position.z = Math.sin(360 / mapSetting.nbPlayer * Math.PI / 180) * radius;
	
	scene.add(shape);
	threeJsShape.push(shape);
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

const animate = () => {
	threeJsShape.forEach((shape) => {
		if (keys.left)
			positionX -= 0.1;
		else if (keys.right)
			positionX += 0.1;
		// actualiser la position du joueur concerné
		sendPos(JSON.stringify({'posx': positionX}));
		shape.position.x = updatePos();
	});
	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}

animate();
