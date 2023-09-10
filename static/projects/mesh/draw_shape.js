function defineSketch(initializer, generator) {
	return function(sketch) {
		let mesh = undefined;
		let img  = undefined;
		let useImg = false;

		sketch.setup = () => {
			sketch.createCanvas(350, 350, sketch.WEBGL);
			sketch.setAttributes('antialias', true);

			img = sketch.loadImage("/prims/imgs/uv.png");

			if(initializer !== undefined) {
				let sliders = initializer(sketch);
				for(let i in sliders) {
					sliders[i].input(update);
				}
			}
		}

		sketch.draw = () => {

			// if(sketch.keyIsDown(85)) {
			// 	useImg = !useImg;
			// }

			if(sketch.frameCount > 3 && 1/(sketch.deltaTime*1000) > sketch.frameRate()*2) {
				sketch.frameRate(sketch.frameRate() * 0.9);
			}

			if(mesh == undefined) {
				mesh = generator(sketch);
				console.log(mesh[0].length, mesh[1].length);
			}

			let index = mesh[0];
			let verts = mesh[1];
			let uvs   = mesh[2];
			let scale = mesh.length > 3 ? mesh[3] : 1.0;

			sketch.camera(0, 0, 200, 0, 0, 0, 0, 1, 0);

			sketch.clear();
			sketch.noFill();
			sketch.stroke(245);

			sketch.rotateY(sketch.frameCount/120/sketch.PI);
			sketch.rotateX(sketch.PI/6);

			sketch.rotateZ(sketch.frameCount/120/sketch.PI);

			sketch.scale(100 * scale);

			drawIndexedList(sketch, useImg ? img : undefined, index, verts, uvs);
		}

		let update = () => {
			mesh = undefined;
		}
	};
}

function startSketch(initializer, generator, id) {
	new p5(defineSketch(initializer, generator), id);
}

function drawIndexedList(sketch, img, index, verts, uvs) {
	sketch.beginShape(sketch.TRIANGLES);
	
	if(img == undefined) {
		sketch.noFill();
	}

	else {
		sketch.texture(img);
	}

	for(let i = 0; i < index.length; i+=3) {
		let p1 = verts[index[i]];
		let p2 = verts[index[i + 1]];
		let p3 = verts[index[i + 2]];

		let uv1 = uvs[index[i]];
		let uv2 = uvs[index[i + 1]];
		let uv3 = uvs[index[i + 2]];

		if(img == undefined) {
			sketch.vertex(p1.x, p1.y, p1.z);
			sketch.vertex(p2.x, p2.y, p2.z);
			sketch.vertex(p3.x, p3.y, p3.z);
		}

		else {
			sketch.vertex(p1.x, p1.y, p1.z, uv1.x*1024, uv1.y*1024);
			sketch.vertex(p2.x, p2.y, p2.z, uv2.x*1024, uv2.y*1024);
			sketch.vertex(p3.x, p3.y, p3.z, uv3.x*1024, uv3.y*1024);
		}
	}

	sketch.endShape();
}