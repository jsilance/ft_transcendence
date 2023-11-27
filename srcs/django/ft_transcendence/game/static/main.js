const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);

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
	const {type, color} = el;
	let geometry;
	
	switch (type) {
		case 1:
			geometry = new THREE.SphereGeometry(1, 20, 20);
			break;
		case 2:
			geometry = new THREE.BoxGeometry(1, 1, 1);
			break;
		case 3:
			geometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 32);
			break;
	}
	
	const material = new THREE.MeshPhongMaterial({color: color});
	const shape = new THREE.Mesh(geometry, material);
	
	shape.position.x = (Math.random() - 0.5) * 5;
	shape.position.y = Math.random() * 2 + 0.5;
	shape.position.z = (Math.random() - 0.5) * 5;
	console.log(shape);
	
	scene.add(shape);
	threeJsShape.push(shape);
}

const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(1, 2, 3);
scene.add(directionalLight);


const animate = () => {
	threeJsShape.forEach((shape) => {
		shape.rotation.x += 0.01;
		shape.rotation.y += 0.01;
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

