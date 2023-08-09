class Shape {
	constructor() {
		this.o = 255;
		this.t = 255;
		this.c = 230; // color grey
	}

	hidenow() { this.t = this.o = 0; }
	hide() { this.t = 0; }
	show() { this.t = 255; }

	draw() {
		this.o = lerp(this.o, this.t, 0.1);

		if (this.mydraw !== undefined) {
			this.mydraw();
		}
	}
}

class Polygon extends Shape {
	constructor(x = 0, y = 0, n = "") {
		super();
		this.x = x;
		this.y = y;
		this.p = [];
		this.n = n;
		this.no = 255;
		this.nt = 255;

		this.mycenter = createVector(0, 0);
	}

	mydraw() {
		noFill()
		stroke(this.c, this.o);
		strokeWeight(2);

		for (let i = 0; i < this.p.length; i++) {
			let j = (i + 1) % this.p.length;
			line(this.x + this.p[i].x, this.y + this.p[i].y, this.x + this.p[j].x, this.y + this.p[j].y);
		}

		fill(230, this.o);
		noStroke();

		for (let i = 0; i < this.p.length; i++) {
			ellipse(this.x + this.p[i].x, this.y + this.p[i].y, 5, 5);
		}

		noStroke();
		fill(this.c, this.no * this.o);

		if (this.mycenter.x == 0) {
			this.mycenter = this.center();
		}

		else {
			this.mycenter.x = lerp(this.mycenter.x, this.center().x, 0.1);
			this.mycenter.y = lerp(this.mycenter.y, this.center().y, 0.1);
		}

		push();
		scale(1, -1);
		textSize(24);
		text(this.n, this.mycenter.x - 5, -this.mycenter.y + 5);
		pop();

		this.no = lerp(this.no, this.nt, 0.1);
	}

	genVectorList(other) {
		let vectors = [];


		for (let j = 0; j < other.p.length; j++) {
			for (let i = 0; i < this.p.length; i++) {
				let v = new Vector(
					other.x + other.p[j].x,
					other.y + other.p[j].y,
					(this.x + this.p[i].x) - (other.x + other.p[j].x),
					(this.y + this.p[i].y) - (other.y + other.p[j].y)
				);

				vectors.push(v);
			}
		}

		return vectors;
	}

	genSimpleVectorList(other) {
		let vectors = [];

		for (let i = 0; i < this.p.length; i++) {
			let v = new Vector(
				other.x + other.p[i].x,
				other.y + other.p[i].y,
				(this.x + this.p[i].x) - (other.x + other.p[i].x),
				(this.y + this.p[i].y) - (other.y + other.p[i].y)
			);

			vectors.push(v);
		}

		return vectors;
	}

	genDifference(other) {
		let p = [];
		for (var i = 0; i < this.p.length; i++) {
			for (var j = 0; j < other.p.length; j++) {
				p[i + j * this.p.length] = [
					(this.x + this.p[i].x) - (other.x + other.p[j].x),
					(this.y + this.p[i].y) - (other.y + other.p[j].y)
				];
			}
		}

		let hull = d3.polygonHull(p);

		let shape = new Polygon(0, 0, this.n + " - " + other.n);
		for (let i = 0; i < hull.length; i++) {
			shape.p[i] = createVector(hull[i][0], hull[i][1]);
		}

		return shape;
	}

	getFurthestPoint(d) {
		let point, maxDistance = -Infinity;

		for (let i in this.p) {
			let p = this.p[i].copy();
			p.x += this.x; p.y += this.y;

			let distance = p.dot(d);
			if (distance > maxDistance) {
				maxDistance = distance;
				point = p;
			}
		}

		return point;
	}

	center() {
		let v = createVector(0, 0);
		for (let i in this.p) {
			v.x += this.p[i].x;
			v.y += this.p[i].y;
		}

		v.x /= this.p.length;
		v.y /= this.p.length;

		v.x += this.x;
		v.y += this.y;

		return v;
	}

	showName() {
		this.nt = 255;
	}

	hideName() {
		this.nt = 0;
	}
}

function CreateSquare(x = 0, y = 0, n = "") {
	let shape = new Polygon(x, y, n);

	shape.p = [createVector(-50, 50),
	createVector(-50, -50),
	createVector(50, -50),
	createVector(50, 50)];

	return shape;
}

function CreateTriangle(x = 0, y = 0, r = 0, n = "") {
	let shape = new Polygon(x, y, n);

	shape.p = [createVector(-50, -50).rotate(r),
	createVector(0, 50).rotate(r),
	createVector(50, -50).rotate(r)];

	return shape;
}

class Vector extends Shape {
	constructor(x = 0, y = 0, vx = 100, vy = 100, n = "") {
		super();
		this.x = x;
		this.y = y;
		this.vx = vx;
		this.vy = vy;
		this.n = n;
	}

	mydraw() {
		strokeWeight(1);
		stroke(255, 100, 100, this.o);
		fill(255, 100, 100, this.o);

		line(this.x, this.y, this.x + this.vx, this.y + this.vy);

		push();
		translate(this.x, this.y);
		rotate(atan2(this.vy, this.vx));
		translate(sqrt(this.vx * this.vx + this.vy * this.vy), 0);
		triangle(0, 0, -10, 5, -10, -5);
		pop();

		noStroke();
		push();
		translate(this.x + this.vx, this.y + this.vy);
		scale(1, -1);
		text(this.n, -this.vx / 20, -10);
		pop();
	}
}

class Grid extends Shape {
	constructor() {
		super();
		this.s = 100;
	}

	mydraw() {
		stroke(100, this.o);
		strokeWeight(0.5);

		let wid = width;
		let hei = height;

		for (let w = this.s; w < wid; w += this.s) line(w, -hei, w, hei);
		for (let w = -this.s; w > -wid; w -= this.s) line(w, -hei, w, hei);
		for (let h = this.s; h < hei; h += this.s) line(-wid, h, wid, h);
		for (let h = -this.s; h > -hei; h -= this.s) line(-wid, h, wid, h);

		stroke(170, this.o);
		strokeWeight(1.5);

		line(-wid, 0, wid, 0);
		line(0, -hei, 0, hei);
	}
}