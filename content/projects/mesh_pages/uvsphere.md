[code](UVSphere.h, cpp,
#pragma once

#include "glm/vec2.hpp"
#include "glm/vec3.hpp"
#include "glm/geometric.hpp"
#include `l`<`l`vector`l`>

using namespace `w`glm;

struct `t`UVSphere {
	std::vector<int> `w`index;
	std::vector<vec3> `w`pos;
	std::vector<vec2> `w`uvs;
};

`t`UVSphere `f`MakeUVSphere(int `a``a`latCount, int `a``a`latCount);
)

[code](UVSphere.cpp, cpp,
#include "uvsphere.h"

static const float `n`pi = 3.1415927f;

`t`UVSphere `f`MakeUVSphere(int `a`latCount, int `a`lonCount) {
	if (`a`latCount < 2 || `a`lonCount < 2) {
		return {};
	}

	// Each longitudinal count makes two triangles (6 indices) for every
	// lateral count except for the top and bottom poles, which only make
	// one triangle per longitudinal count.

	// UV maps require two vertices with the same position, but different UVs
	// so we need counts + 1.

	const int `v`totalIndexCount = 6 * (`a`latCount - 1) * `a`lonCount;
	const int `v`totalVertexCount = (`a`latCount + 1) * (`a`lonCount + 1);
	const float `v`latStep = `n`pi / `a`latCount;
	const float `v`lonStep = 2 * `n`pi / `a`lonCount;
 
	`t`UVSphere `v`sphere;

	`v`sphere.`w`index.`f`resize(`v`totalIndexCount);
	`v`sphere.`w`pos.`f`resize(`v`totalVertexCount);
	`v`sphere.`w`uvs.`f`resize(`v`totalVertexCount);
 
	int `v`currentVertex = 0;
	int `v`currentIndex = 0;

	for (int `v`lat = 0; `v`lat <= `a`latCount; `v`lat++) {
		for (int `v`lon = 0; `v`lon <= `a`lonCount; `v`lon++) {
			`v`sphere.`w`pos[`v`currentVertex] = vec3(
				cos(`v`lon * `v`lonStep) * sin(`v`lat * `v`latStep),
				sin(`v`lon * `v`lonStep) * sin(`v`lat * `v`latStep),
				cos(`v`lat * `v`latStep - `n`pi)
			);

			`v`sphere.`w`uvs[`v`currentVertex] = vec2(
				1.f - (float)`v`lon / `a`lonCount,
				(float)`v`lat / `a`latCount
			);

			`v`currentVertex += 1;
		}
	}
 
	// Top cap
	//
	// One triangle connects the first lateral layer to the second per longitudinal count.
	// Even though the top points all have the same position, their UVs are different,
	// so each triangle uses a different point.
	//
	//          -------- lonCount -------->
	//                      lon
	//    |                  *
	//    |                / | \
	//    1             /    |    \
	//    |          /       |       \
	//    |       /                     \
	//   \ /     *------------*------------*
	//           v          v + 1        v + 2
 
	int `v`v = `a`lonCount + 1;
	for (int `v`lon = 0; `v`lon < `a`lonCount; `v`lon++) {
		`v`sphere.`w`index[`v`currentIndex++] = `v`lon;
		`v`sphere.`w`index[`v`currentIndex++] = `v`v;
		`v`sphere.`w`index[`v`currentIndex++] = `v`v + 1;

		`v`v += 1;
	}

	// Middle
	//
	// Each lateral layer has 2 triangles for every longitudinal count.
	//
	//          -------- lonCount -------->
	//          v          v + 1        v + 2
	//    |     *------------*------------*
	//    |     |          / |          / |
	// latCount |       /    |       /    |
	//    |     |    /       |    /       |
	//    |     | /          | /          |
	//   \ /    *------------*------------*
	//      v + lc + 1   v + lc + 2   (v + 1) + lc + 2

	`v`v = `a`lonCount + 1;
	for (int `v`lat = 1; `v`lat < `a`latCount - 1; `v`lat++) {
		for (int `v`lon = 0; `v`lon < `a`lonCount; `v`lon++) {
			`v`sphere.`w`index[`v`currentIndex++] = `v`v;
			`v`sphere.`w`index[`v`currentIndex++] = `v`v + `a`lonCount + 1;
			`v`sphere.`w`index[`v`currentIndex++] = `v`v + 1;
 
			`v`sphere.`w`index[`v`currentIndex++] = `v`v + 1;
			`v`sphere.`w`index[`v`currentIndex++] = `v`v + `a`lonCount + 1;
			`v`sphere.`w`index[`v`currentIndex++] = `v`v + `a`lonCount + 2;

			`v`v += 1;
		}

		`v`v += 1;
	}

	// Bottom cap

	// Same as top cap, but reversed.
	//
	//          -------- lonCount -------->
	//          v          v + 1        v + 2
	//    |     *------------*------------*
	//    |       \          |          /
	//    1          \       |       /
	//    |             \    |    /
	//    |                \ | /
	//   \ /                 *
	//                   v + lc + 1
 
	for (int `v`lon = 0; `v`lon < `a`lonCount; `v`lon++) {
		`v`sphere.`w`index[`v`currentIndex++] = `v`v;
		`v`sphere.`w`index[`v`currentIndex++] = `v`v + `a`lonCount + 1;
		`v`sphere.`w`index[`v`currentIndex++] = `v`v + 1;

		`v`v += 1;
	}
 
	return `v`sphere;
}
)