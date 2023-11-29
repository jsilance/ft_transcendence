// import { OrbitControls } from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();

// TO DO: create mutiple cameras and attribute to apropriate user
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;
// 

// Utilisation de webgl
const renderer = new THREE.WebGLRenderer();
// 
// window size
// renderer.setSize(window.innerWidth - 15, window.innerHeight - 16);
renderer.setSize(window.innerWidth - 80, window.innerHeight - 60);
// 

const sceneBox = document.getElementById('scene-box');
sceneBox.appendChild(renderer.domElement);


// creation du plane qui sert de sol
const planeGeometry = new THREE.PlaneGeometry(10, 10);
planeGeometry.rotateX(30);
const planeMaterial = new THREE.MeshBasicMaterial({color: 0x00f0f0});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
scene.add(plane);
// 

// creation du brouillard
const fogColor = "#000";
const fogNear = 2;
const fogFar = 8;
scene.fog = new THREE.Fog(fogColor, fogNear, fogFar);
// 


// initialisation des borders, users et ball
const threeJsShape = []

for (const el of shapes) {
	const {type, color, posx, posy} = el;
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
	console.log(posx);
	shape.position.y = 1;
	shape.position.z = posy;
	console.log(shape);
	
	scene.add(shape);
	threeJsShape.push(shape);
}
// 


// Lumieres
const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(1, 2, 3);
scene.add(directionalLight);
// 


// const controls = new OrbitControls(camera, renderer.domElement);	


// Animations
// TO DO: modifier la position des joueurs en fonctions du websocket
let angle = 0;
let radius = 0.5;

const animate = () => {
	threeJsShape.forEach((shape) => {
		shape.position.x = radius * Math.cos(angle);
		shape.position.z = radius * Math.sin(angle);

		// shape.rotateY(-0.55 * Math.PI / 180);

		angle += 0.03;
	});
	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}
// 

// const animate = function () {
// 	renderer.render(scene, camera);
// 	requestAnimationFrame(animate);
// };

animate();
// document.body.appendChild(renderer.domElement);

