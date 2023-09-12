let slider_resLon_uvs,
	slider_resLat_uvs;

function initUvSphere(sketch) {
	slider_resLon_uvs = sketch.createSlider(2, 32, 16);
	slider_resLat_uvs = sketch.createSlider(2, 32, 8);

	slider_resLon_uvs.parent('uvsphere-tools-resLon');
	slider_resLat_uvs.parent('uvsphere-tools-resLat');

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

startSketch(initUvSphere, makeUvSphere, 'uvsphere');