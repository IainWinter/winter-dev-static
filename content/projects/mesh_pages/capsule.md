[code](Capsule.h, cpp,
#pragma once

#include "glm/vec3.hpp"
#include "glm/vec2.hpp"
#include "glm/geometric.hpp"
#include `l`<`l`vector`l`>

using namespace `n`glm;

struct `t`Capsule {
	std::vector<int> `w`index;
	std::vector<vec3> `w`pos;
	std::vector<vec2> `w`uvs;
};

`t`Capsule `f`MakeCapsule(int `a`resolution, float `a`height, float `a`radius);
)

[code](Capsule.cpp, cpp,
#include "capsule.h"

static const float `n`pi = 3.1415927f;

`t`Capsule `f`MakeCapsule(int `a`resolution, float `a`height, float `a`radius) {
	if (`a`resolution < 2) {
		return {};
	}

	// Almost same generation as UV sphere but we force the
	// lat count to be odd so it can be split evenly

	int `v`latCount = `a`resolution;
	int `v`lonCount = `a`resolution;

	if (`v`latCount % 2 == 0) {
		`v`latCount++;
	}

	// Each longitudinal count makes two triangles (6 indices) for every
	// lateral count except for the top and bottom poles, which only make
	// one triangle per longitudinal count.

	// UV maps require two vertices with the same position, but different UVs
	// so we need counts + 1.

	const int `v`totalIndexCount = 6 * (`v`latCount - 1) * `v`lonCount;
	const int `v`totalVertexCount = (`v`latCount + 1) * (`v`lonCount + 1);
	const float `v`latStep = `n`pi / `v`latCount;
	const float `v`lonStep = 2 * `n`pi / `v`lonCount;
	const float `v`zOffset = clamp(`a`height / 2.0f - `a`radius, 0.0f, FLT_MAX);

	`t`Capsule `v`capsule;

	`v`capsule.`w`index.`f`resize(`v`totalIndexCount);
	`v`capsule.`w`pos.`f`resize(`v`totalVertexCount);
	`v`capsule.`w`uvs.`f`resize(`v`totalVertexCount);

	int `v`currentVertex = 0;
	int `v`currentIndex = 0;

	for (int `v`lat = 0; `v`lat <= `v`latCount; `v`lat++) {
		float `v`offset = `v`lat > `v`latCount / 2 ? `v`zOffset : -`v`zOffset;

		for (int `v`lon = 0; `v`lon <= `v`lonCount; `v`lon++) {
			`v`capsule.`w`pos[`v`currentVertex] = vec3(
				cos(`v`lon * `v`lonStep) * sin(`v`lat * `v`latStep) * `a`radius,
				sin(`v`lon * `v`lonStep) * sin(`v`lat * `v`latStep) * `a`radius,
				cos(`v`lat * `v`latStep - `n`pi) * `a`radius + `v`offset
			);

			// UVs are almost the same as the UV sphere, but V needs 
			// to be scaled to fit the height

			`v`capsule.`w`uvs[`v`currentVertex] = vec2(
				(float)`v`lon / `v`lonCount,
				`v`capsule.`w`pos[`v`currentVertex].`w`z / (`a`radius * 2 + `a`height) + 0.5f
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
	//          v          v + 1      (v + 1) + 1

	int `v`v = `v`lonCount + 1;
	for (int `v`lon = 0; `v`lon < `v`lonCount; `v`lon++) {
		`v`capsule.`w`index[`v`currentIndex++] = `v`lon;
		`v`capsule.`w`index[`v`currentIndex++] = `v`v;
		`v`capsule.`w`index[`v`currentIndex++] = `v`v + 1;

		`v`v += 1;
	}

	// Middle
	//
	// Each lateral layer has 2 triangles for every longitudinal count.
	//
	//          -------- lonCount -------->
	//          v          v + 1      (v + 1) + 1
	//    |     *------------*------------*
	//    |     |          / |          / |
	// latCount |       /    |       /    |
	//    |     |    /       |    /       |
	//    |     | /          | /          |
	//   \ /    *------------*------------*
	//      v + lc + 1   v + lc + 2   (v + 1) + lc + 2

	`v`v = `v`lonCount + 1;
	for (int `v`lat = 1; `v`lat < `v`latCount - 1; `v`lat++) {
		for (int `v`lon = 0; `v`lon < `v`lonCount; `v`lon++) {
			`v`capsule.`w`index[`v`currentIndex++] = `v`v;
			`v`capsule.`w`index[`v`currentIndex++] = `v`v + `v`lonCount + 1;
			`v`capsule.`w`index[`v`currentIndex++] = `v`v + 1;

			`v`capsule.`w`index[`v`currentIndex++] = `v`v + 1;
			`v`capsule.`w`index[`v`currentIndex++] = `v`v + `v`lonCount + 1;
			`v`capsule.`w`index[`v`currentIndex++] = `v`v + `v`lonCount + 2;

			`v`v += 1;
		}

		`v`v += 1;
	}

	// Bottom cap

	// Same as top cap, but reversed.
	//
	//          -------- lonCount -------->
	//          v          v + 1      (v + 1) + 1
	//    |     *------------*------------*
	//    |       \          |          /
	//    1          \       |       /
	//    |             \    |    /
	//    |                \ | /
	//   \ /                 *
	//                   v + lc + 1

	for (int `v`lon = 0; `v`lon < `v`lonCount; `v`lon++) {
		`v`capsule.`w`index[`v`currentIndex++] = `v`v;
		`v`capsule.`w`index[`v`currentIndex++] = `v`v + `v`lonCount + 1;
		`v`capsule.`w`index[`v`currentIndex++] = `v`v + 1;

		`v`v += 1;
	}

	return `v`capsule;
}
)