let slider_res_cap, 
	slider_height, 
	slider_radius;

function initCapsule(sketch) {
	slider_res_cap = sketch.createSlider(2, 15, 5);
	slider_height  = sketch.createSlider(1, 2, 2, .1);
	slider_radius  = sketch.createSlider(.1, 1, .5, .1);

	addTool('capsule', 'Resolution', slider_res_cap);
	addTool('capsule', 'Height', slider_height);
	addTool('capsule', 'Radius', slider_radius);

	return [slider_res_cap, slider_height, slider_radius];
}

function makeCapsule(sketch, resolution = -1, height = -1, radius = -1) {
	if(resolution == -1) resolution = slider_res_cap.value();
	if(height == -1)     height     = slider_height .value();
	if(radius == -1)     radius     = slider_radius .value();

	let lonCount = resolution;
	let latCount = resolution;

	if(latCount % 2 == 0) latCount++;

	let indexCount = 6 * lonCount  * (latCount - 1);
	let vertCount = (lonCount + 1) * (latCount + 1);

	let indices = [];
	let verts = [];
	let uvs   = [];

	// Verts

	let yOff = (height - radius * 2.0) * 0.5;
	if (yOff < 0) yOff = 0;

	let lonStep = Math.PI*2 / lonCount;
	let latStep = Math.PI   / latCount;
	let xStep   = 1.0       / lonCount;

	for (let lat = 0, v = 0; lat <= latCount; lat++) {
	for (let lon = 0;        lon <= lonCount; lon++, v++) {
		verts[v] = sketch.createVector(
			Math.cos(lon * lonStep) * Math.sin(lat * latStep),
			Math.sin(lat * latStep - Math.PI/2),
			Math.sin(lon * lonStep) * Math.sin(lat * latStep)
		);
		
		verts[v].mult(radius);

		if (lat > latCount / 2) verts[v].y += yOff;
		else                    verts[v].y -= yOff;

		uvs[v] = sketch.createVector(
			1.0 - xStep * lon,
			(verts[v].y + height) * 0.5 / height
		);
	}
	}

	// Index

	let i = 0;
	let v = lonCount + 1;
	for (let lon = 0; lon < lonCount; lon++, v++) {
		indices[i++] = lon;
		indices[i++] = v;
		indices[i++] = v + 1;
	}

	v = lonCount + 1;
	for (let lat = 1; lat < latCount - 1; lat++, v++) {
	for (let lon = 0; lon < lonCount;     lon++, v++) {
		indices[i++] = v;
		indices[i++] = v + lonCount + 1;
		indices[i++] = v + 1;
		indices[i++] = v + 1;
		indices[i++] = v + lonCount + 1;
		indices[i++] = v + lonCount + 2;
	}
	}

	for (let lon = 0; lon < lonCount; lon++, v++) {
		indices[i++] = v;
		indices[i++] = v + lonCount + 1;
		indices[i++] = v + 1;
	}

	return [indices, verts, uvs];
}

function getCapsuleTable() {
	function v(x, z) {
		return (x + 1) * (z + 1);
	}

	function i(x, z) {
		return x * z * 6;
	}

	let table = [
		["X", "Z", "Vertx", "Index"],
		[1, 1, v(1, 1), i(1, 1)],
		[1, 2, v(1, 2), i(1, 2)],
		[1, 3, v(1, 3), i(1, 3)],
		[2, 2, v(2, 2), i(2, 2)],
		[2, 3, v(2, 3), i(2, 3)],
		[5, 5, v(5, 5), i(5, 5)],
		[10, 10, v(10, 10), i(10, 10)]
	];

	return table;
}

startSketch(initCapsule, makeCapsule, getCapsuleTable, 'capsule');