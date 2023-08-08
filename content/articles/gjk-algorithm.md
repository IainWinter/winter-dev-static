---
title: "GJK: Collision detection algorithm in 2D/3D"
date: August 29, 2020
thumbnail: MDusDn8oTSE.jpg
published: true
---

# GJK: Collision detection algorithm in 2D/3D

![iframe-youtube-video](https://www.youtube.com/embed/MDusDn8oTSE?rel=0)

In my last article, I only covered sphere vs. sphere collisions because they are the simplest to compute. Spheres are nice and all, but there comes a time when more complex shapes are needed. One popular algorithm for testing collisions is the Gilbert–Johnson–Keerthi algorithm, or GJK for short. With it we can detect collisions between any two convex polygons.

The GJK algorithm is very useful and widely used, but no good visualization or concise explanations exist for some reason. A few years ago, I listened and relistened to a video by [Casey Muratori](https://www.youtube.com/watch?v=Qupqu1xe7Io) that explains the algorithm in great detail and goes through some smart insights that give a good mental image of how it works. Yet I have found no full interactive visualizations. Let’s jump into it!

## Difference between spheres and polygons

Testing for a collision between spheres is easy because there are only two points in the system. This leaves us with a single vector that we can compare against the sum of their radii to determine if there is a collision.

![local-iframe](/articles/gjk-algorithm/app/circles.html)

With polygons we cannot make such simplifications. They are made from multiple vertices, removing any apparent way of finding their distance and clear radius property to compare against. We need a smarter way of testing for a collision.

Like we subtracted the points in the sphere system, let’s see what happens if we subtract the vertices of the polygons.

![local-iframe](/articles/gjk-algorithm/app/sub_poly.html)

Subtracting two polygons with the same number of vertices is straightforward, but if we want to support various polygons, we need to subtract each vertex from every vertex on the other polygon. Because there are multiple vertices, we are not left with a single vector, but many that form another polygon. This results in a cloud of $A*B$ number vertices that we need to process further to select the outer convex hull from.

This outer hull is known as the [Minkowski difference](https://en.wikipedia.org/wiki/Minkowski_addition). It represents the distance between every point of the two polygons. We are going to use it to turn two polygons into one that we can analyze to detect a collision. The key is that if the origin is inside the difference, there must have been two points that subtracted to 0; meaning there is overlap somewhere.

![local-iframe](/articles/gjk-algorithm/app/mink_diff.html)

## Abstracting shapes into supporting points

The Minkowski difference is nice for visualization, but far too expensive to compute in real time; we need a way to simplify it.

The GJK algorithm is only concerned with the outer hull of our cloud of vertices, so it would give a substantial speed up if we could cut down on the time spent finding them. Let’s think about what puts a vertex on the hull. If we look closer, notice that those vertices have the most extreme components. They got to their locations from subtraction between two other vertices, so for one to be the most extreme, it must have come from the most extreme vertices on the source polygons. If we define ‘most extreme’ as the furthest in some direction, we can play with the math to get this speed increase.

Finding the furthest vertex is done by iterating over the set of vertices and finding the one with the largest dot product in a direction. Let $\vec D$ be the direction and $A−B$ be the cloud of vertices.

$$
\max\{\vec{D}\cdot{(A-B)}\}
$$

Computing $A-B$ took $A*B$ number of steps; making this function an $O(n^2)$ operation. Luckily for us, we can distribute and never have to compute the full difference.

If we distribute the dot product and max function we’re left with this:

$$
\max\{(\vec{D}\cdot{A})-(\vec{D}\cdot{B})\}
$$

$$
\max\{\vec{D}\cdot{A}\}-\max\{(-\vec{D})\cdot{B}\}
$$

Now all we need is $A+B$ steps; turning our quadratic time function into a linear one.

We need to reverse the direction for $A$ when we distribute max because we want to retain the max value. We want the lest extreme vertex from $B$ to subtract from the most extreme vertex from $A$.

![](/articles/gjk-algorithm/supports.jpg)

These vertices are referred to as [supporting points](https://en.wikipedia.org/wiki/Support_function) and give a view into the Minkowski difference without ever calculating more than we need.

Let’s look at the implementation -- I’m going to continue to use the Collider structs from the [physics engine](/articles/physics-engine) article for consistency, but will only include the new pieces from this article.

We’ll start by adding a function that finds the support point in a given direction. Let’s call it FindFurthestPoint. If we have other special types of colliders like spheres, capsules, or planes, we can override this function allowing them to be used with GJK as well.

~~~Collider.h cpp
struct `t`Collider {
	virtual vec3 `f`FindFurthestPoint(vec3 `a`direction) const = 0;
};
~~~

Next, we’ll make a MeshCollider with a list of vertices to act as our polygon. FindFurthestPoint needs to loop over each vertex and compare the distance along the direction. We’ll keep track of the max vertex & distance to compare. Once we have iterated over all the points, we’ll return the max point.

~~~MeshCollider.h cpp
struct `t`MeshCollider : `t`Collider
{
private:
	std::vector<vec3> m_vertices;
 
public:
	vec3 `f`FindFurthestPoint(vec3 `a`direction) const override
	{
		vec3  `v`maxPoint;
		float `v`maxDistance = -`p`FLT_MAX;
 
		for (vec3 `v`vertex : m_vertices) {
			float `v`distance = dot(`v`vertex, `a`direction);
			if (`v`distance > `v`maxDistance) {
				`v`maxDistance = `v`distance;
				`v`maxPoint = `v`vertex;
			}
		}
 
		return `v`maxPoint;
	}
};
~~~

We can roll all of this into a function called Support that will take two colliders and a direction and return the vertex on the Minkowski difference.

~~~GJK.h cpp
vec3 `f`Support(const `t`Collider& `a`colliderA, const `t`Collider& `a`colliderB, vec3 `a`direction)
{
	return `a`colliderA.`f`FindFurthestPoint( `a`direction)
	     - `a`colliderB.`f`FindFurthestPoint(-`a`direction);
}
~~~

With these functions, we have abstracted away not only any convex polygon, but any collider type that implements FindFurthestPoint into a single function that we can use in the algorithm.

## GJK: Surrounding the origin

The goal of the GJK algorithm is to determine if the origin is within the Minkowski difference. This would be easy, but we’ve thrown out the complete difference for the sake of performance. We only have the Support function that gives us one vertex at a time. We need to iteratively search for and build up what’s referred to as a [simplex](https://en.wikipedia.org/wiki/Simplex) around the origin.

A simplex is defined as a shape that has $N+1$ number of vertices with $N$ being the number of dimensions. Practically, this represents the simplest shape that can ‘select’ a region in space. For example, in 2D a triangle is the simplest shape that can select an area containing a specific point. These shapes have simple tests that we can use to determine which vertex, edge, or face is closest to the origin. Depending on which feature is closest, we’ll remove, add, or swap points to make the simplex closer to the origin. If we find that the closest feature is already the closest possible, but the origin is not inside, we know there is no collision. Otherwise, if we find the origin inside the simplex we know there has been a collision.

We get the vertices for the simplex from the Support function, so we need to find the direction to the origin from the closest feature. Searching towards the origin allows the algorithm to converge quickly. Let’s look an example. We’ll start with an arbitrary vertex then add or remove vertices every iteration until we surround the origin or find it’s impossible.

![local-iframe](/articles/gjk-algorithm/app/slide-show.html)

We can see that there are two cases that we need to deal with: a line and triangle. We need one more case in the form of a tetrahedron to select a volume if we want 3D collision detection.

![](/articles/gjk-algorithm/flow.svg)

To represent the simplex, let’s make a wrapper struct around an std::array. This will allow us to keep track of the number of points, while keeping the memory on the stack for quick access.

~~~Simplex.h cpp
struct `t`Simplex {
private:
	std::array<vec3, 4> m_points;
	int m_size;

public:
	`f`Simplex()
		: m_size (0)
	{}

	`t`Simplex& operator=(std::initializer_list<vec3> `a`list) 
	{
		for (vec3 `v`point : `a`list)
			m_points[m_size++] = `v`point;

		return *this;
	}

	void `f`push_front(vec3 `a`point) 
	{
		m_points = { `a`point, m_points[0], m_points[1], m_points[2] };
		m_size = std::`f`min(m_size + 1, 4);
	}

	vec3& operator[](int `a`i) { return m_points[`a`i]; }
	size_t `f`size() const { return m_size; }

	auto `f`begin() const { return m_points.`f`begin(); }
	auto `f`end() const { return m_points.`f`end() - (4 - m_size); }
};
~~~

We need at least one vertex to start, so we’ll manually add it. The search direction for the first vertex doesn’t matter, but you may get less iterations with a smarter choice. I’m going to use unit x (1, 0, 0) for no particular reason.

~~~GJK.h cpp
bool `f`GJK(const `t`Collider& `a`colliderA, const `t`Collider& `a`colliderB)
{
	// Get initial support point in any direction
	vec3 `v`support = `f`Support(`a`colliderA, `a`colliderB, vec3(1, 0, 0));
~~~

Now that we have one point, we can add it to the simplex and set the search direction towards the origin.

~~~GJK.h cpp no_title
	// Simplex is an array of points, max count is 4
	`f`Simplex `v`points;
	`v`points.`f`push_front(`v`support);

	// New direction is towards the origin
	vec3 `v`direction = -`v`support;
~~~

In a loop, we’ll add another point. The exit condition is that this new point is not in front of the search direction. This would exit if the direction finds a vertex that was already the furthest one along it.

~~~GJK.h cpp no_title
	while (true) {
		`v`support = `f`Support(`a`colliderA, `a`colliderB, `v`direction);
 
		if (dot(`v`support, `v`direction) <= 0) {
			return false; // no collision
		}

		`v`points.`f`push_front(`v`support);
~~~

Now that we have a line, we’ll feed it into a function that updates the simplex and search direction. It’ll return true or false to signify a collision.

~~~GJK.h cpp no_title
		if (`f`NextSimplex(`v`points, `v`direction)) {
			return true;
		}
	}
}
~~~

That’s all for the main loop. It’s dead simple in the world of algorithms, but the real work is in the NextSimplex function. We need a series of different checks for each shape of simplex to see what the new simplex should be and what direction we’ll search in next.

The NextSimplex function will act as a dispatcher to three other functions, one for each shape.

~~~GJK.h cpp
bool `f`NextSimplex(`t`Simplex& `a`points, vec3& `a`direction)
{
	switch (`a`points.`f`size()) {
		case 2: return `f`Line       (`a`points, `a`direction);
		case 3: return `f`Triangle   (`a`points, `a`direction);
		case 4: return `f`Tetrahedron(`a`points, `a`direction);
	}
 
	// never should be here
	return false;
}
~~~

We can add one more helper function to help lessen the headache from these next functions.

~~~GJK.h cpp no_title
bool `f`SameDirection(const vec3& `a`direction, const vec3& `a`ao)
{
	return dot(`a`direction, `a`ao) > 0;
}
~~~

We’ll start with the line case. There are three possible regions that the origin could be in, but realistically only two. We started with point B, and searched in the direction of A, which means that the origin cannot be in the red region. This leaves us with one check between the vector AB and AO. If AO is inside the green region, we move on. If AO is in the blue region, we’ll come back to the line case, but B will be replaced.

~~~GJK.h cpp no_title
bool `f`Line(`t`Simplex& `a`points, vec3& `a`direction)
{
	vec3 `v`a = `a`points[0];
	vec3 `v`b = `a`points[1];

	vec3 `v`ab = `v`b - `v`a;
	vec3 `v`ao =   - `v`a;
 
	if (`f`SameDirection(`v`ab, `v`ao)) {
		`a`direction = cross(cross(`v`ab, `v`ao), `v`ab);
	}

	else {
		`a`points = { `v`a };
		`a`direction = `v`ao;
	}

	return false;
}
~~~

![article-embed-half](/articles/gjk-algorithm/line.jpg)

In this case, AO is in the same direction as AB, so we know it’s in the green region. We’ll set the search direction pointing towards the origin and move on. In 2D, you would not need to use cross products, but in 3D the origin could be anywhere in a cylinder around the line, so we need them to get the correct direction.

The triangle case has seven regions, but again we can cull out some impossibilities. Yellow, red, and purple cannot have the origin because the new point we added was A, meaning that the origin cannot be in the direction of the BC face. That leaves us with four regions we need to check.

If the origin is outside the triangle on the AC face, we’ll check if it’s also in the direction of AC. If it is, then we’ll remove B from the simplex and move on, if not, we’ll do a line case between AB. If the origin was not in the direction of the AC face, we’ll check the AB face. If it’s there, we’ll do the same line case between AB. Finally, if both checks fail, we know it must be inside the triangle. In 2D we would be done and could return true, but in 3D we need to check if the origin is above or below the triangle and move on.

~~~GJK.h cpp no_title
bool `f`Triangle(`t`Simplex& `a`points, vec3& `a`direction)
{
	vec3 `v`a = `a`points[0];
	vec3 `v`b = `a`points[1];
	vec3 `v`c = `a`points[2];

	vec3 `v`ab = `v`b - `v`a;
	vec3 `v`ac = `v`c - `v`a;
	vec3 `v`ao =   - `v`a;
 
	vec3 `v`abc = cross(`v`ab, `v`ac);
 
	if (`f`SameDirection(cross(`v`abc, `v`ac), `v`ao)) {
		if (`f`SameDirection(`v`ac, `v`ao)) {
			`a`points = { `v`a, `v`c };
			`a`direction = cross(cross(`v`ac, `v`ao)), `v`ac);
		}

		else {
			return `f`Line(`a`points = { `v`a, `v`b }, `a`direction);
		}
	}
 
	else {
		if (`f`SameDirection(cross(`v`ab, `v`abc), `v`ao)) {
			return `f`Line(`a`points = { `v`a, `v`b }, `a`direction);
		}

		else {
			if (`f`SameDirection(`v`abc, `v`ao)) {
				`a`direction = `v`abc;
			}

			else {
				`a`points = { `v`a, `v`c, `v`b };
				`a`direction = -`v`abc;
			}
		}
	}

	return false;
}
~~~

![article-embed-half](/articles/gjk-algorithm/triangle.jpg)

The tetrahedron case is the most complex, but almost entirely made up of triangle cases. We don’t need to test for the origin below the tetrahedron for the same reason as before. We only need to determine which face, if any, the origin is in the direction of. If there is one, we’ll go back to the triangle case with that face as the simplex, but if not, we know it must be inside the tetrahedron and we’ll return true.

~~~GJK.h cpp no_title
bool `f`Tetrahedron(`t`Simplex& `a`points, vec3& `a`direction)
{
	vec3 `v`a = `a`points[0];
	vec3 `v`b = `a`points[1];
	vec3 `v`c = `a`points[2];
	vec3 `v`d = `a`points[3];

	vec3 `v`ab = `v`b - `v`a;
	vec3 `v`ac = `v`c - `v`a;
	vec3 `v`ad = `v`d - `v`a;
	vec3 `v`ao =   - `v`a;
 
	vec3 `v`abc = cross(`v`ab, `v`ac);
	vec3 `v`acd = cross(`v`ac, `v`ad);
	vec3 `v`adb = cross(`v`ad, `v`ab);
 
	if (`f`SameDirection(`v`abc, `v`ao)) {
		return `f`Triangle(`a`points = { `v`a, `v`b, `v`c }, `a`direction);
	}
		
	if (`f`SameDirection(`v`acd, `v`ao)) {
		return `f`Triangle(`a`points = { `v`a, `v`c, `v`d }, `a`direction);
	}
 
	if (`f`SameDirection(`v`adb, `v`ao)) {
		return `f`Triangle(`a`points = { `v`a, `v`d, `v`b }, `a`direction);
	}
 
	return true;
}
~~~

![article-embed-half](/articles/gjk-algorithm/tetrahedron.jpg)

With that final case, we have completed the GJK algorithm. As you can see it is not that complex looking at it from a geometric point of view. This algorithm only gives you a yes/no answer about a collision, so you cannot respond to it. In the next article I will cover an algorithm that uses the simplex and similar principles to find the collision normal then maybe get into rotational physics. Thanks for reading!

Here is a demo that will let you play around with the algorithm and let you inspect each iteration, here's the [full version](/articles/gjk-algorithm/app/demo.html) if you want a better look...

![local-iframe](/articles/gjk-algorithm/app/demo.html)