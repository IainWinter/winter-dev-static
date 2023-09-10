function defineSketch(initializer, generator) {
	return function(sketch) {
		sketch.mesh = undefined;
		sketch.inputs = [];

		sketch.setup = function() {
			sketch.createCanvas(350, 350, sketch.WEBGL);
			sketch.frameRate(75);

			let inputs = initializer(sketch);

			for (let input of inputs) {
				sketch.inputs.push({
					input: input,
					value: input.value(),
				});
			}
		}

		sketch.draw = function() {
			let regenerateMesh = sketch.mesh === undefined;

			for (let input of sketch.inputs) {
				let value = input.input.value(); // compare against cache. This stinks idk 
				if (input.value != value) {      // how to use .changed as it only gets called on drag end
					input.value = value;
					regenerateMesh = true;
				}
			}

			if (regenerateMesh) {
				sketch.mesh = generator(sketch);
			}

			let angle = sketch.frameCount/120/sketch.PI;

			sketch.camera(0, 0, 200, 0, 0, 0, 0, 1, 0);

			sketch.clear();
			sketch.noFill();
			sketch.stroke(245);

			sketch.rotateX(angle);
			sketch.rotateY(angle);
			//sketch.rotateZ(angle);

			sketch.scale(50);

			drawIndexedList(sketch, sketch.mesh[0], sketch.mesh[1]);
		}
	};
}

function startSketch(initializer, generator, id) {
	return new p5(defineSketch(initializer, generator), id);
}

function drawIndexedList(sketch, index, verts) {
	for(let i = 0; i < index.length; i+=3) {
		let p1 = verts[index[i]];
		let p2 = verts[index[i + 1]];
		let p3 = verts[index[i + 2]];

		//let depth = p1.copy().add(p2).add(p3).div(3).z;
		//sketch.stroke(255*depth);

		sketch.line(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z);
		sketch.line(p1.x, p1.y, p1.z, p3.x, p3.y, p3.z);
		sketch.line(p2.x, p2.y, p2.z, p3.x, p3.y, p3.z); // draws every line 3 times
	}
}

function addTool(shapeId, toolName, tool) {
	let div = document.createElement('div');
	div.classList = ["shape-tool"];
	div.innerHTML = `<p>${toolName}</p>`
	div.appendChild(tool.elt);
	
	let shapeDOM = document.getElementById(`${shapeId}-tools`);
	shapeDOM.appendChild(div);
}