This is a test

[code](Plane.h, cpp,
#pragma once

#include "glm/vec3.hpp"
#include "glm/vec2.hpp"
#include "glm/geometric.hpp"
#include `l`<`l`vector`l`>

using namespace `w`glm;

struct `t`Plane {
	std::vector<int> `w`index;
	std::vector<vec3> `w`pos;
	std::vector<vec2> `w`uvs;
};

`t`Plane `f`MakePlane(int `a`xCount, int `a`yCount);
)

[code](Plane.cpp, cpp,
#include "plane.h"

`t`Plane `f`MakePlane(int `a`xCount, int `a`yCount) {
	// For each count in either direction, two triangles are added to the mesh.
	// The xCount and yCount are the number of quads, not vertices, so one more vertex is needed in each direction.

	if (`a`xCount == 0 || `a`yCount == 0) {
		return {};
	}

	const int `v`totalIndexCount = 6 * `a`xCount * `a`yCount;
	const int `v`totalVertexCount = (`a`xCount + 1) * (`a`yCount + 1);

	const vec3 `v`offset = vec3(-1, -1, 0); // Make the plane span (-1, -1, 0) to (1, 1, 0)
	const float `v`xStep = 2.0f / `a`xCount;
	const float `v`yStep = 2.0f / `a`yCount;

	const float `v`uStep = 1.0f / `a`xCount; // But UVs always span (0, 0) to (1, 1)
	const float `v`vStep = 1.0f / `a`yCount;

	`t`Plane `v`plane;

	`v`plane.`w`index.`f`resize(`v`totalIndexCount);
	`v`plane.`w`pos.`f`resize(`v`totalVertexCount);
	`v`plane.`w`uvs.`f`resize(`v`totalVertexCount);

	for (int `v`x = 0; `v`x <= `a`xCount; `v`x++)
	for (int `v`y = 0; `v`y <= `a`yCount; `v`y++)
	{
		int `v`i = `v`y + `v`x * (`a`yCount + 1);

		`v`plane.`w`pos[`v`i] = vec3(`v`x * `v`xStep, `v`y * `v`yStep, 0) + `v`offset;
		`v`plane.`w`uvs[`v`i] = vec2(`v`x * `v`uStep, (`a`yCount - y) * `v`vStep);
	}

	//        --------- xCount --------->
	//        v          v + 1        v + 2
	//    |   *------------*------------*
	//    |   |          / |          / |
	// yCount |       /    |       /    |
	//    |   |    /       |    /       |
	//   \ /  | /          | /          |
	//        *------------*------------*
	//    v + yc + 1   v + yc + 2   v + yc + 3

	int `v`i = 0;
	for (int `v`v = 0; `v`v < `v`totalVertexCount - `a`yCount - 2; `v`v++) {
		// If at the final row, jump to next column
		if ((`v`v + 1) % (`a`yCount + 1) == 0) {
			`v`v++;
		}

		`v`plane.`w`index[`v`i++] = `v`v;
		`v`plane.`w`index[`v`i++] = `v`v + 1;
		`v`plane.`w`index[`v`i++] = `v`v + `a`yCount + 1;

		`v`plane.`w`index[`v`i++] = `v`v + 1;
		`v`plane.`w`index[`v`i++] = `v`v + `a`yCount + 2;
		`v`plane.`w`index[`v`i++] = `v`v + `a`yCount + 1;
	}

	return `v`plane;
}
)