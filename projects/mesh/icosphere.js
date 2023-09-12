const IcoVertCount  = 22;
const IcoIndexCount = 60;

const ICO_X = .525731112119133606;
const ICO_Z = .850650808352039932;

let IcoVerts;
let IcoUvs;
let IcoIndex;

let slider_res;

// Initializer

function initIcoSphere(sketch) {
	IcoVerts = [
		sketch.createVector(-0.003619, -0.525716, -0.85064),
		sketch.createVector(-0.531561, -0.84702,   0.0),
		sketch.createVector( 0.850626, -0.005838, -0.52572),
		sketch.createVector( 0.519874, -0.854242, -0.0),
		sketch.createVector( 0.531561,  0.84702,  -0.0),
		sketch.createVector(-0.531561, -0.84702,   0.0),
		sketch.createVector( 0.850626, -0.005838,  0.52572),
		sketch.createVector(-0.003618, -0.525716,  0.85064),
		sketch.createVector( 0.531561,  0.84702,  -0.0),
		sketch.createVector(-0.531561, -0.84702,   0.0),
		sketch.createVector( 0.003619,  0.525716,  0.85064),
		sketch.createVector(-0.850626,  0.005838,  0.52572),
		sketch.createVector( 0.531561,  0.84702,  -0.0),
		sketch.createVector(-0.531561, -0.84702,   0.0),
		sketch.createVector(-0.519874,  0.854242,  0.0),
		sketch.createVector(-0.850626,  0.005838, -0.52572),
		sketch.createVector( 0.531561,  0.84702,  -0.0),
		sketch.createVector(-0.531561, -0.84702,   0.0),
		sketch.createVector( 0.003618,  0.525716, -0.85064),
		sketch.createVector(-0.003619, -0.525716, -0.85064),
		sketch.createVector( 0.531561,  0.84702,  -0.0),
		sketch.createVector( 0.850626, -0.005838, -0.52572)
	]

	IcoUvs = [
		sketch.createVector(0.0,      0.157461),
		sketch.createVector(0.090909, 0.0),
		sketch.createVector(0.090909, 0.314921),
		sketch.createVector(0.181818, 0.157461),
		sketch.createVector(0.181818, 0.472382),
		sketch.createVector(0.272727, 0.0),
		sketch.createVector(0.272727, 0.314921),
		sketch.createVector(0.363636, 0.157461),
		sketch.createVector(0.363636, 0.472382),
		sketch.createVector(0.454545, 0.0),
		sketch.createVector(0.454545, 0.314921),
		sketch.createVector(0.545454, 0.157461),
		sketch.createVector(0.545454, 0.472382),
		sketch.createVector(0.636363, 0.0),
		sketch.createVector(0.636363, 0.314921),
		sketch.createVector(0.727272, 0.157461),
		sketch.createVector(0.727272, 0.472382),
		sketch.createVector(0.818181, 0.0),
		sketch.createVector(0.818181, 0.314921),
		sketch.createVector(0.90909,  0.157461),
		sketch.createVector(0.90909,  0.472382),
		sketch.createVector(1.0,      0.314921)
	]

	IcoIndex = [
		0,1,3,    //Top
		3,5,7,
		7,9,11,
		11,13,15,
		15,17,19, 
		0,3,2,    // Middle
		2,3,6,
		3,7,6,
		6,7,10,
		7,11,10,
		10,11,14,
		11,15,14,
		14,15,18,
		15,19,18,
		18,19,21,  
		2,6,4,    // Bottom
		6,10,8,
		10,14,12,
		14,18,16,
		18,21,20 
	];

	slider_res = sketch.createSlider(0, 3, 1);
  	slider_res.parent('icosphere-tools-res');
  	
  	return [slider_res];
}

// Generator

function makeIcoSphere(sketch, resolution = -1) {
		if(resolution === -1) {
			resolution = slider_res.value();
		}

		let indices = IcoIndex.slice();
		let verts = IcoVerts.slice();
		let uvs   = IcoUvs.slice();

		// Verts & Index

		let currentIndexCount = [IcoIndexCount];
		let currentVertCount  = [IcoVertCount];
		for (let i = 0; i < resolution; i++) {
			SubDevideVerts(indices, verts, uvs, currentIndexCount, currentVertCount);
		}

		// Makes it a sphere

		for (let i = 0; i < verts.length; i++) {
			verts[i].normalize();
		}

		return [indices, verts, uvs];
}

// Helper functions

function SubDevideVerts(index, verts, uvs, currentIndexCount, currentVertCount) {
	let lookup = {};
	let nextIndex = [];
	let nextIndexCount = 0;

	for(let i = 0; i < currentIndexCount[0]; i += 3) {
		let mid0 = CreateVertexForEdge(lookup, verts, uvs, index[i],     index[i + ((i + 1) % 3)], currentVertCount);
		let mid1 = CreateVertexForEdge(lookup, verts, uvs, index[i + 1], index[i + ((i + 2) % 3)], currentVertCount);
		let mid2 = CreateVertexForEdge(lookup, verts, uvs, index[i + 2], index[i + ((i + 3) % 3)], currentVertCount);

		nextIndex[nextIndexCount++] = index[i];	    nextIndex[nextIndexCount++] = mid0; nextIndex[nextIndexCount++] = mid2;
		nextIndex[nextIndexCount++] = index[i + 1]; nextIndex[nextIndexCount++] = mid1; nextIndex[nextIndexCount++] = mid0;
		nextIndex[nextIndexCount++] = index[i + 2]; nextIndex[nextIndexCount++] = mid2; nextIndex[nextIndexCount++] = mid1;
		nextIndex[nextIndexCount++] = mid0;	        nextIndex[nextIndexCount++] = mid1; nextIndex[nextIndexCount++] = mid2;
	}

	for(let i in nextIndex) {
		index[i] = nextIndex[i];
	}

	currentIndexCount[0] = nextIndexCount;
}

function CreateVertexForEdge(lookup, verts, uvs, first, second, currentVertCount) {
	let key = first < second ? [first, second] : [second, first];

	let myVertCount = currentVertCount[0];

	if(!(key in lookup)) {
		verts[currentVertCount[0]  ] = verts[first].copy().add(verts[second]).mult(.5);
		uvs  [currentVertCount[0]++] = uvs  [first].copy().add(uvs  [second]).mult(.5);
	} else {
		lookup[key] = myVertCount;		
	}


	return myVertCount;
}

startSketch(initIcoSphere, makeIcoSphere, 'icosphere');