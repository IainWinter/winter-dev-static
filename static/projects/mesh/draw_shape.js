let themeStroke = 0;

function defineSketch(initializer, generator) {
	return function(sketch) {
		sketch.mesh = undefined;
		sketch.inputs = [];

		sketch.setup = function() {
			sketch.createCanvas(500, 500, sketch.WEBGL);
			sketch.frameRate(30);
			sketch.noFill();
			sketch.smooth();
			
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

			sketch.camera(0, 0, 150, 0, 0, 0, 0, 1, 0);
			sketch.scale(50);

			sketch.clear();
			
			sketch.rotateX(angle);
			sketch.rotateY(angle);
			//sketch.rotateZ(angle);
			
			sketch.stroke(themeStroke);

			drawIndexedList(sketch, sketch.mesh[0], sketch.mesh[1]);
		}
	};
}

function startSketch(initializer, generator, populateTable, id) {
	// assume that this is on a page with a table with id 'shape-table'
	// and its the only table

	// this is removed
	// let tableDOM = document.getElementById('shape-table');

	// if (tableDOM) {
	// 	let table = populateTable();

	// 	for (let row of table) {
	// 		let rowDOM = tableDOM.insertRow(-1); // Insert a new row at the end of the table

	// 		for (let cell of row) {
	// 			let cellDOM = rowDOM.insertCell();
	// 			cellDOM.innerHTML = cell;
	// 		}
	// 	}
	// }

	return new p5(defineSketch(initializer, generator), id);
}

function drawIndexedList(sketch, index, verts) {
	for(let i = 0; i < index.length; i+=3) {
		let p1 = verts[index[i]];
		let p2 = verts[index[i + 1]];
		let p3 = verts[index[i + 2]];

		sketch.line(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z);
		sketch.line(p1.x, p1.y, p1.z, p3.x, p3.y, p3.z);
		sketch.line(p2.x, p2.y, p2.z, p3.x, p3.y, p3.z); // draws every line 3 times, could do better
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

function setThemeStroke(theme) {
	themeStroke = theme == "light" ? 0 : 245;
}

setThemeStroke(localStorage.getItem("theme"));
subscribeToThemeChange(setThemeStroke);