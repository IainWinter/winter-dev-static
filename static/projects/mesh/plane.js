let resX, resZ;

function initPlane(sketch) {
	resX = sketch.createSlider(1, 15, 5);
	resZ = sketch.createSlider(1, 15, 5);

	addTool('plane', 'Resolution X', resX);
	addTool('plane', 'Resolution Z', resZ);

	return [resX, resZ];
}

function makePlane(sketch, xCount = -1, zCount = -1) {
	if(xCount == -1) xCount = resX.value();
	if(zCount == -1) zCount = resZ.value();

	let indexCount = 6 * xCount * zCount;
	let vertCount  = (xCount + 1) * (zCount + 1);

	let indices = [];
	let verts   = [];
	let uvs     = [];

	let stepX = 2.0 / xCount;
	let stepZ = 2.0 / zCount;

	let stepU = 1.0 / xCount;
	let stepV = 1.0 / zCount;

	let offset = sketch.createVector(-1, 0, -1);

	for (let x = 0; x <= xCount; x++) {
		for (let z = 0; z <= zCount; z++) {
			let i = z + x * (zCount + 1);

			verts[i] = offset.copy().add(sketch.createVector(x * stepX, 0, z * stepZ));
			uvs  [i] = sketch.createVector(x * stepU, (zCount - z) * stepV);
		}
	}

	let i = 0, v = 0;
	do {
		indices[i++] = v;
		indices[i++] = v + 1; 
		indices[i++] = v + zCount + 1;

		indices[i++] = v + 1;
		indices[i++] = v + zCount + 2; 
		indices[i++] = v + zCount + 1;

		v++;
		if ((v + 1) % (zCount + 1) == 0) {
			v++;
		}
	}while(v <= vertCount - (zCount + 3));

	return [indices, verts, uvs, 0.7];
}

startSketch(initPlane, makePlane, 'plane');