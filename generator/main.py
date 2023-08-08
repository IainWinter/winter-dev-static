from winterdev_generator import render_winter_dev_article

test_template = '''
<html>
<head>
	<title>[put](title)</title>
	<link rel="stylesheet" type="text/css" href="css/article_template.css">
</head>
	<div className="main">
		<div className="top">
			<h1 className="title">Winter</h1>
			<div className="nav-section">
				<div className="nav-links">
					<Link className="nav-link" href="/articles">Articles</Link>
					<Link className="nav-link" href="/projects">Projects</Link>
					<Link className="nav-link" href="/support">Support</Link>
				</div>

				<hr className="nav-separator"/>

				<div className="nav-buttons">
					
				</div>
			</div>
		</div>
		<div className="page">
			[put](article)
		</div>
	</div>
</html>
'''

test_article = '''
---
title: EPA: Collision response algorithm for 2D/3D
date: November 17, 2020
thumbnail: 0XQ2FSz3EK8.jpg
published: true
---

[title](EPA: Collision response algorithm for 2D/3D)

Last time we looked at an algorithm for testing collisions between two convex polygons called GJK. It's a useful algorithm for sure, but it doesn't give us enough information to respond to the collisions it detects. In this article I'll describe an extension that allows us to find the correct normal and depth of the collisions. This extension provides the information that the solvers need to resolve a collision as I demonstrated in my original physics engine [link](article, /articles/physics-engine#collision-response).

I call this algorithm an extension because its input is the internal state from GJK. If you recall, we were working with a simplex to try and surround the origin with a triangle in 2D or a tetrahedron in 3D. This algorithm takes the final simplex that contained the origin and finds the normal of collision, aka the shortest vector to nudge the shapes out of each other. The naive solution is to use the normal of the closest face to the origin, but remember, a simplex does not need to contain any of the original polygon's faces, so we could end up with an incorrect normal.

Let's jump into it, it's called the Expanding Polytope Algorithm because it expands the simplex by adding vertices to it until we find the shortest normal from a face that is on the original polygon. For jargon's sake, a [link](simplex, https://en.wikipedia.org/wiki/Simplex) becomes a [link](polytope, https://en.wikipedia.org/wiki/Polytope) after we begin adding more vertices to it. How do we do that? Well we already have the tools from GJK, all we need to do is iterate over the faces and find the closest one. Then we'll use the Support function to find if there is a point  further in the direction of that normal. If there is one, the face of the polytope must be inside the original polygon and can be expanded. If so, we'll add this supporting point and repeat.

In 2D this is easy, we can just add the point and the edges remain intact. In 3D we need to do a little repair job, which is where most of the annoyance comes from. Let's start with the 2D version first, because it shows the algorithm's main pieces, then we'll see how to repair the 3D polytope.

[sub-title](2D in Javascript)

I'm going to venture into a little [link](p5.js, https://p5js.org/) for the 2D version because I've made a small demo with it that you can check out in fullscreen [link](here, /articles/gjk-algorithm/app/demo.html).

[iframe](/articles/gjk-algorithm/app/demo.html)

We'll start with a function that takes in the simplex from GJK and the two shapes that we are testing.

The first step is to find the edge closest to the origin. We'll do this by comparing the dot products between their normals and the vectors from the origin. We only need the closest one, so we'll store it, along with its index and distance in variables, outside the loop to use later.

[code](EPA.js, javascript,
function `f`EPA(`a`polytope, `a`shapeA, `a`shapeB) {
	let `v`minIndex = 0;
	let `v`minDistance = Infinity;
	let `v`minNormal;

	while (`v`minDistance == Infinity) {
		for (let `v`i = 0; `v`i < `a`polytope.`w`length; `v`i++) {
			let `v`j = (`v`i + 1) % `a`polytope.`w`length;

			let `v`vertexI = `a`polytope[`v`i].`f`copy();
			let `v`vertexJ = `a`polytope[`v`j].`f`copy();

			let `v`ij = `v`vertexJ.`f`sub(`v`vertexI);

			let `v`normal = `f`createVector(`v`ij.`w`y, -`v`ij.`w`x).`f`normalize();
			let `v`distance = `v`normal.`f`dot(`v`vertexI);

			if (`v`distance < 0) {
				`v`distance *= -1;
				`v`normal.`f`mult(-1);
			}

			if (`v`distance < `v`minDistance) {
				`v`minDistance = `v`distance;
				`v`minNormal = `v`normal;
				`v`minIndex = `v`j;
			}
		}
)

Finding the normal of a vector in 2D is done by swapping the X and Y components and flipping one of their signs. The handedness, either right or left, depends on which component gets flipped. Depending on the winding order, the handedness that results in an outward facing normal changes, so it's common to add a check to flip it if it's wrong.

[svg](./normal.svg)

Once we have this normal, we can use the Support function to test for a point further out in its direction. If there is one, we'll insert the support point between the vertices in the polytope and repeat. If there isn't one, we know we have found the actual closest normal and can return it. Adding a small amount to the distance is useful to stop repeat collisions that would have moved the shapes an even smaller distance.

[code](EPA.js, javascript no_title,
		let `v`support = `f`support(`a`shapeA, `a`shapeB, `v`minNormal);
		let `v`sDistance = `v`minNormal.`f`dot(`v`support);

		if (`f`abs(`v`sDistance - `v`minDistance) > 0.001) {
		 	`v`minDistance = Infinity;
			`v`polytope.`f`splice(`v`minIndex, 0, `v`support);
		}
	}

	return `v`minNormal.`f`mult(`v`minDistance + 0.001);
}
)

That's it for the 2D version. Now that we've looked at the core of this algorithm, we can make the jump to 3D. The main difference between the two is that in 2D the edges are implied by the order of the vertices, but in 3D we need to explicitly define the faces because each vertex is shared between three or more faces.

[sub-title](3D in C++)

[code](EPA.h, cpp,
`t`CollisionPoints `f`EPA(
	const `t`Simplex& `a`simplex, 
	const `t`Collider& `a`colliderA, 
	const `t`Collider& `a`colliderB)
{
)

In 3D we need to keep track of every face. I've seen some different techniques, but the most straightforward in my opinion is to treat it like a mesh and use an index. We'll start with the polytope like we did in the 2D case, but now we'll also store the faces in a separate list. The most common way to do this is to treat every three indices as a triangle.

This index makes it easy to calculate the normal once per face, instead of with every iteration like in the 2D version, so let's split that into its own function so we can calculate them before we start.

[code](EPA.h_, cpp,
	std::vector<vec3> `v`polytope(`a`simplex.`f`begin(), `a`simplex.`f`end());
	std::vector<size_t> `v`faces = {
		0, 1, 2,
		0, 3, 1,
		0, 2, 3,
		1, 3, 2
	};

	// list: vec4(normal, distance), index: min distance
	auto [`v`normals, `v`minFace] = `f`GetFaceNormals(`v`polytope, `v`faces);
)

We'll add the same main loop from before.

[code](EPA.h_, cpp,
	vec3  `v`minNormal;
	float `v`minDistance = `p`FLT_MAX;
	
	while (`v`minDistance == `p`FLT_MAX) {
		`v`minNormal   = `v`normals[`v`minFace].`f`xyz();
		`v`minDistance = `v`normals[`v`minFace].`w`w;
 
		vec3 `v`support = `f`Support(`a`colliderA, `a`colliderB, `v`minNormal);
		float `v`sDistance = dot(`v`minNormal, `v`support);
 
		if (`f`abs(`v`sDistance - `v`minDistance) > 0.001f) {
			`v`minDistance = `p`FLT_MAX;
)

When expanding the polytope in 3D, we cannot just add a vertex, we need to repair the faces as well. You would think that removing the face and adding three more would be enough, but when two faces result in the same support point being added, duplicate faces end up inside the polytope and cause incorrect results. The solution is to remove not just the current face, but every face that is pointing in the direction of the support point. To repair it afterwards, we'll keep track of the unique edges and use those along with the support point's index to make new faces.

[code](EPA.h_, cpp,
			std::vector<std::pair<size_t, size_t>> `v`uniqueEdges;

			for (size_t `v`i = 0; `v`i < `v`normals.`f`size(); `v`i++) {
				if (`f`SameDirection(`v`normals[`v`i], `v`support)) {
					size_t f = `v`i * 3;

					`f`AddIfUniqueEdge(`v`uniqueEdges, `v`faces, `v`f,     `v`f + 1);
					`f`AddIfUniqueEdge(`v`uniqueEdges, `v`faces, `v`f + 1, `v`f + 2);
					`f`AddIfUniqueEdge(`v`uniqueEdges, `v`faces, `v`f + 2, `v`f    );

					`v`faces[`v`f + 2] = `v`faces.`f`back(); `v`faces.`f`pop_back();
					`v`faces[`v`f + 1] = `v`faces.`f`back(); `v`faces.`f`pop_back();
					`v`faces[`v`f    ] = `v`faces.`f`back(); `v`faces.`f`pop_back();

					`v`normals[`v`i] = `v`normals.`f`back(); // pop-erase
					`v`normals.`f`pop_back();

					`v`i--;
				}
			}
)

Now that we have a list of unique edges, we can add the new faces to a list and add the supporting point to the polytope. Storing the new faces in their own list allows us to calculate only the normals of these new faces.

[code](EPA.h_, cpp,
			std::vector<size_t> `v`newFaces;
			for (auto [`v`edgeIndex1, `v`edgeIndex2] : `v`uniqueEdges) {
				`v`newFaces.`f`push_back(`v`edgeIndex1);
				`v`newFaces.`f`push_back(`v`edgeIndex2);
				`v`newFaces.`f`push_back(`v`polytope.`f`size());
			}
			 
			`v`polytope.`f`push_back(`v`support);

			auto [`v`newNormals, `v`newMinFace] = `f`GetFaceNormals(`v`polytope, `v`newFaces);
)

After we calculate the new normals, we need to find the new closest face. To eke out a little bit more performance, we'll only iterate over the old normals, then we'll compare the closest one to the closest face of the new normals. Finally, we can add these new faces and normals to the end of their respective lists.

[code](EPA.h_, cpp,
			float `v`oldMinDistance = `p`FLT_MAX;
			for (size_t `v`i = 0; `v`i < `v`normals.`f`size(); `v`i++) {
				if (`v`normals[`v`i].w < `v`oldMinDistance) {
					`v`oldMinDistance = `v`normals[`v`i].`w`w;
					`v`minFace = `v`i;
				}
			}
 
			if (`v`newNormals[`v`newMinFace].w < `v`oldMinDistance) {
				`v`minFace = `v`newMinFace + `v`normals.`f`size();
			}
 
			`v`faces  .`f`insert(`v`faces  .`f`end(), `v`newFaces  .`f`begin(), `v`newFaces  .`f`end());
			`v`normals.`f`insert(`v`normals.`f`end(), `v`newNormals.`f`begin(), `v`newNormals.`f`end());
		}
	}
)

Once a supporting point isn't found further from the closest face, we'll return that face's normal and its distance in a CollisionPoints.

[code](EPA.h_, cpp,
	`t`CollisionPoints `v`points;
 
	`v`points.`w`Normal = `v`minNormal;
	`v`points.`w`PenetrationDepth = `v`minDistance + 0.001f;
	`v`points.`w`HasCollision = true;
 
	return `v`points;
}
)

That's it for the main piece of the algorithm.

Don't think I forgot about the helper functions...

GetFaceNormals is just a slightly more complex version of the loop from the 2D version. Instead of i and j, we now get three vertices by first looking up their index in the faces list. In 3D the normal is found by taking the cross product of the vectors between the face's vertices. The winding order is now controlled by the index, instead of where we put some negative sign. Even though it's well defined, we don't check when adding new faces, so we still need the check here. Determining the winding involves finding the normal so there is no reason to not have this check here.

I've chosen to pack the distance and normal into a single vec4 to keep the code shorter.

[code](EPA.h, cpp,
std::pair<std::vector<vec4>, size_t> `f`GetFaceNormals(
	const std::vector<vec3>& `a`polytope,
	const std::vector<size_t>& `a`faces)
{
	std::vector<vec4> `v`normals;
	size_t `v`minTriangle = 0;
	float  `v`minDistance = `p`FLT_MAX;

	for (size_t `v`i = 0; `v`i < `a`faces.`f`size(); `v`i += 3) {
		vec3 `v`a = `a`polytope[`a`faces[`v`i    ]];
		vec3 `v`b = `a`polytope[`a`faces[`v`i + 1]];
		vec3 `v`c = `a`polytope[`a`faces[`v`i + 2]];

		vec3 `v`normal = normalized(cross(`v`b - `v`a, `v`c - `v`a));
		float `v`distance = dot(`v`normal, `v`a);

		if (`v`distance < 0) {
			`v`normal   *= -1;
			`v`distance *= -1;
		}

		`v`normals.`f`emplace_back(`v`normal, `v`distance);

		if (`v`distance < `v`minDistance) {
			`v`minTriangle = `v`i / 3;
			`v`minDistance = `v`distance;
		}
	}

	return { `v`normals, `v`minTriangle };
}
)

AddIfUniqueEdge tests if the reverse of an edge already exists in the list and if so, removes it. If you look at how the winding works out, if a neighboring face shares an edge, it will be in reverse order. Remember, we only want to store the edges that we are going to save because every edge gets removed first, then we repair.

[code](EPA.h, cpp,
void `f`AddIfUniqueEdge(
	std::vector<std::pair<size_t, size_t>>& `a`edges,
	const std::vector<size_t>& `a`faces,
	size_t `a`a,
	size_t `a`b)
{
	auto `v`reverse = std::`f`find(               //      0--<--3
		`a`edges.`f`begin(),                     //     / \ B /   A: 2-0
		`a`edges.`f`end(),                       //    / A \ /    B: 0-2
		std::`f`make_pair(`a`faces[`a`b], `a`faces[`a`a]) //   1-->--2
	);
 
	if (`v`reverse != `a`edges.`f`end()) {
		`a`edges.`f`erase(`v`reverse);
	}
 
	else {
		`a`edges.`f`emplace_back(`a`faces[`a`a], `a`faces[`a`b]);
	}
}
)

That's it for this algorithm, this allows us to handle some interesting collisions in the physics engine.

Let's look at some demos!

[iframe-youtube-video](https://www.youtube.com/embed/0XQ2FSz3EK8?start=330&rel=0)
'''

# read file from article_template.html

template_text = ''
with open('../content/article_template.html', 'r', encoding='utf-8') as f:
	template_text = f.read()

article_test = ''
with open('../content/articles/epa-algorithm.md', 'r', encoding='utf-8') as f:
	article_test = f.read()

out = render_winter_dev_article(template_text, article_test)
with open('../out/articles/epa-algorithm.html', 'w', encoding='utf-8') as f:
	f.write(out)