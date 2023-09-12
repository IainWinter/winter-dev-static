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

function getPlaneTable() {
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
		[10, 10, v(10, 10), i(10, 10)],
		["x", "y", 
			'<math><mo>(</mo><mi>x</mi><mo>*</mo><mi>y</mi><mo>)</mo><mo>*</mo><mn>6</mn></math>', 
			'<math><mo>(</mo><mi>x</mi><mo>+</mo><mn>1</mn><mo>)</mo><mo>*</mo><mo>(</mo><mi>y</mi><mo>+</mo><mn>1</mn><mo>)</mo></math>']
	];

	return table;
}

startSketch(initPlane, makePlane, getPlaneTable, 'plane');