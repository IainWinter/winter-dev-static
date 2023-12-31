let slider_resLon_uvs,
	slider_resLat_uvs;

function initUvSphere(sketch) {
	slider_resLon_uvs = sketch.createSlider(2, 32, 16);
	slider_resLat_uvs = sketch.createSlider(2, 32, 8);

	addTool('uvsphere', 'Resolution Longitude', slider_resLon_uvs);
	addTool('uvsphere', 'Resolution Latitude', slider_resLat_uvs);

	return [slider_resLon_uvs, slider_resLat_uvs];
}

function makeUvSphere(sketch, lonCount = -1, latCount = -1) {
	if(lonCount == -1) lonCount = slider_resLon_uvs.value();
	if(latCount == -1) latCount = slider_resLat_uvs.value();

	let indexCount = 6 * lonCount * (latCount - 1);
	let vertCount = (latCount + 1) * (lonCount + 1);

	let indices = [];
	let verts = [];
	let uvs   = [];

	// Verts

	let lonStep = Math.PI*2 / lonCount;
	let latStep = Math.PI   / latCount;

	for (let lat = 0, v = 0; lat <= latCount; lat++) {
	for (let lon = 0;        lon <= lonCount; lon++, v++) {
		verts[v] = sketch.createVector(
			Math.cos(lon * lonStep) * Math.sin(lat * latStep),
			Math.sin(lat * latStep - Math.PI / 2),
			Math.sin(lon * lonStep) * Math.sin(lat * latStep)
		);
				
		uvs[v] = sketch.createVector(
			lon / lonCount,
			lat / latCount
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

function getUVSphereTable() {
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

startSketch(initUvSphere, makeUvSphere, getUVSphereTable, 'uvsphere');