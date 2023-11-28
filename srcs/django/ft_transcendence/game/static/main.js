// import { OrbitControls } from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth - 15, window.innerHeight - 16);

const sceneBox = document.getElementById('scene-box');
sceneBox.appendChild(renderer.domElement);


const planeGeometry = new THREE.PlaneGeometry(10, 10);
planeGeometry.rotateX(30);
const planeMaterial = new THREE.MeshBasicMaterial({color: 0x00f0f0});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
scene.add(plane);

const fogColor = "#000";
const fogNear = 2;
const fogFar = 8;
scene.fog = new THREE.Fog(fogColor, fogNear, fogFar);

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
	
	const material = new THREE.MeshPhongMaterial({color: color});
	const shape = new THREE.Mesh(geometry, material);
	
	shape.position.x = posx;
	console.log(posx);
	shape.position.y = 1;
	shape.position.z = posy;
	console.log(shape);
	
	scene.add(shape);
	threeJsShape.push(shape);
}

const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(1, 2, 3);
scene.add(directionalLight);

// const controls = new OrbitControls(camera, renderer.domElement);	

let angle = 0;
let radius = 1;

const animate = () => {
	threeJsShape.forEach((shape) => {
		shape.position.x = radius * Math.cos(angle);
		shape.position.z = radius * Math.sin(angle);
		// rotate around its center of radius
		shape.rotateY(-0.01);

		// shape.rotateY(-0.023);

		angle += 0.01;
		// shape.rotation.x += 0.01;
		// shape.rotation.y += 0.01;
	});
	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}


// const animate = function () {
// 	renderer.render(scene, camera);
// 	requestAnimationFrame(animate);
// };

animate();
// document.body.appendChild(renderer.domElement);

