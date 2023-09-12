An Icosphere is created by iterativly splitting the faces of an [link](Icosahedron, https://en.wikipedia.org/wiki/Icosahedron). The main selling point of icospheres is that their distributions of points are more uniform than a UV sphere. 

[code](Ico`v`sphere.h, cpp,
#pragma once

#include "glm/vec2.hpp"
#include "glm/vec3.hpp"
#include "glm/geometric.hpp"
#include `l`<`l`vector`l`>

using namespace `w`glm;

struct `t`Ico`v`sphere {
	std::vector<int> `w`index;
	std::vector<`t`vec3> `w`pos;
	std::vector<`t`vec2> `w`uvs;
};

`t`Ico`v`sphere `f`MakeIco`v`sphere(int `a`resolution);
)

[code](Ico`v`sphere.cpp, cpp,
#include "icosphere.h"
#include `l`<`l`unordered_map`l`>

static const float `n``n`Z = (1.0f + `f`sqrt(5.0f)) / 2.0f; // Golden ratio
static const vec2 `n`UV = vec2(1 / 11.0f, 1 / 3.0f); // The UV coordinates are laid out in a 11x3 grid

static const int `n`IcoVertexCount = 22;
static const int `n``n`IcoIndexCount = 60;
 
static const vec3 `n`IcoVerts[] = {
	vec3( 0, -1, -`n`Z), vec3(-1, -`n`Z,  0), vec3( `n`Z,  0, -1), vec3( 1, -`n`Z,  0),
	vec3( 1,  `n`Z,  0), vec3(-1, -`n`Z,  0), vec3( `n`Z,  0,  1), vec3( 0, -1,  `n`Z),
	vec3( 1,  `n`Z,  0), vec3(-1, -`n`Z,  0), vec3( 0,  1,  `n`Z), vec3(-`n`Z,  0,  1),
	vec3( 1,  `n`Z,  0), vec3(-1, -`n`Z,  0), vec3(-1,  `n`Z,  0), vec3(-`n`Z,  0, -1),
	vec3( 1,  `n`Z,  0), vec3(-1, -`n`Z,  0), vec3( 0,  1, -`n`Z), vec3( 0, -1, -`n`Z), 
	vec3( 1,  `n`Z,  0), vec3( `n`Z,  0, -1) 
};

static const vec2 `n`IcoUvs[] = {
	`n`UV * vec2( 0, 1), //  0
	`n`UV * vec2( 1, 0), //  1
	`n`UV * vec2( 1, 2), //  2  //
	`n`UV * vec2( 2, 1), //  3  // Vertices & UVs are ordered by U then V coordinates,
	`n`UV * vec2( 2, 3), //  4  //
	`n`UV * vec2( 3, 0), //  5  //        4     8    12    16    20
	`n`UV * vec2( 3, 2), //  6  //      /  \  /  \  /  \  /  \  /  \ 
	`n`UV * vec2( 4, 1), //  7  //     2---- 6----10----14----18----21
	`n`UV * vec2( 4, 3), //  8  //   /  \  /  \  /  \  /  \  /  \  /
	`n`UV * vec2( 5, 0), //  9  //  0---- 3---- 7----11----15----19
	`n`UV * vec2( 5, 2), // 10  //   \  /  \  /  \  /  \  /  \  /
	`n`UV * vec2( 6, 1), // 11  //     1     5     9    13    17
	`n`UV * vec2( 6, 3), // 12  //
	`n`UV * vec2( 7, 0), // 13  // [4, 8, 12, 16, 20] have the same position
	`n`UV * vec2( 7, 2), // 14  // [1, 5, 9, 13, 17]  have the same position
	`n`UV * vec2( 8, 1), // 15  // [0, 19]            have the same position
	`n`UV * vec2( 8, 3), // 16  // [2, 21]            have the same position
	`n`UV * vec2( 9, 0), // 17  // 
	`n`UV * vec2( 9, 2), // 18
	`n`UV * vec2(10, 1), // 19
	`n`UV * vec2(10, 3), // 20
	`n`UV * vec2(11, 2)  // 21
};
 
static const int `n`IcoIndex[] = {
	 2,  6,  4, // Top
	 6, 10,  8,
	10, 14, 12,
	14, 18, 16,
	18, 21, 20,

	 0,  3,  2, // Middle
	 2,  3,  6,
	 3,  7,  6,
	 6,  7, 10,
	 7, 11, 10,
	10, 11, 14,
	11, 15, 14,
	14, 15, 18,
	15, 19, 18,
	18, 19, 21,

	 0,  1,  3, // Bottom
	 3,  5,  7,
	 7,  9, 11,
	11, 13, 15,
	15, 17, 19
};

`t`Icosphere MakeIcosphere(int `a`resolution) {
	// For each resolution, every triangle is subdivided and replaced with 4 new triangles.
	// Most of the vertices are shared between triangles, so an index is also generated.
	// The number of vertices and indices for a given resolution can be calculated by using a geometric series.
	//
	// Example:
	// 
	//     *-------*               *---*---*
	//    / \     /               / \ / \ /
	//   /   \   /    ------->   *---*---*
	//  /     \ /               / \ / \ /
	// *-------*               *---*---*
 
	const int `v`rn = (int)pow(4, `a`resolution);
	const int `v`totalIndexCount = `n`IcoIndexCount * rn;
	const int `v`totalVertexCount = `n`IcoVertexCount + `n`IcoIndexCount * (1 - `v`rn) / (1 - 4);

	`t`Icosphere `v`sphere;

	`v`sphere.`w`index.`f`resize(`v`totalIndexCount);
	`v`sphere.`w`pos.`f`resize(`v`totalVertexCount);
	`v`sphere.`w`uvs.`f`resize(`v`totalVertexCount);
	
	for (int i = 0; i < `n`IcoVertexCount; i++) {  // Copy in initial mesh
		`v`sphere.`w`pos[i] = `n`IcoVerts[i];
		`v`sphere.`w`uvs[i] = `n`IcoUvs[i];
	}

	for (int `v`i = 0; `v`i < `n`IcoIndexCount; `v`i++) {
		`v`sphere.`w`index[`v`i] = `n`IcoIndex[`v`i];
	}
 
	int `v`currentIndexCount = `n`IcoIndexCount;
	int `v`currentVertCount = `n`IcoVertexCount;

	for (int `v`r = 0; `v`r < `a`resolution; `v`r++) {
		// Now split the triangles.
		// This can be done in place, but needs to keep track of the unique triangles
		// 
		//     i+2                 i+2
		//    /   \               /  \
		//   /     \    ---->   m2----m1
		//  /       \          /  \  /  \
		// i---------i+1      i----m0----i+1
 
		std::unordered_map<uint64_t, int> `v`triangleFromEdge;
		int `v`indexCount = `v`currentIndexCount;

		for (int `v`t = 0; `v`t < `v`indexCount; `v`t += 3) {
			int `v`midpoints[3] = {};

			for (int `v`e = 0; `v`e < 3; `v`e++) {
				int `v`first = `v`sphere.`w`index[`v`t + `v`e];
				int `v`second = `v`sphere.`w`index[`v`t + (`v`t + `v`e + 1) % 3];

				if (`v`first > `v`second) {
					std::`f`swap(`v`first, `v`second);
				}

				uint64_t `v`hash = (uint64_t)`v`first | (uint64_t)`v`second << (sizeof(uint32_t) * 8);

				auto [`v`triangle, `v`wasNewEdge] = `v`triangleFromEdge.`f`insert({ `v`hash, `v`currentVertCount });

				if (`v`wasNewEdge) {
					`v`sphere.`w`pos[`v`currentVertCount] = (`v`sphere.`w`pos[`v`first] + `v`sphere.`w`pos[`v`second]) / 2.0f;
					`v`sphere.`w`uvs[`v`currentVertCount] = (`v`sphere.`w`uvs[`v`first] + `v`sphere.`w`uvs[`v`second]) / 2.0f;

					`v`currentVertCount += 1;
				}

				`v`midpoints[e] = `v`triangle->`w`second;
			}

			int `v`mid0 = `v`midpoints[0];
			int `v`mid1 = `v`midpoints[1];
			int `v`mid2 = `v`midpoints[2];

			`v`sphere.`w`index[`v`currentIndexCount++] = `v`sphere.`w`index[`v`t];
			`v`sphere.`w`index[`v`currentIndexCount++] = `v`mid0;
			`v`sphere.`w`index[`v`currentIndexCount++] = `v`mid2;

			`v`sphere.`w`index[`v`currentIndexCount++] = `v`sphere.`w`index[`v`t + 1];
			`v`sphere.`w`index[`v`currentIndexCount++] = `v`mid1;
			`v`sphere.`w`index[`v`currentIndexCount++] = `v`mid0;

			`v`sphere.`w`index[`v`currentIndexCount++] = `v`sphere.`w`index[`v`t + 2];
			`v`sphere.`w`index[`v`currentIndexCount++] = `v`mid2;
			`v`sphere.`w`index[`v`currentIndexCount++] = `v`mid1;

			`v`sphere.`w`index[`v`t]     = `v`mid0; // Overwrite the original triangle with the 4th new triangle
			`v`sphere.`w`index[`v`t + 1] = `v`mid1;
			`v`sphere.`w`index[`v`t + 2] = `v`mid2;
		}
	}

	// Normalize all the positions to create the sphere

	for (vec3& `v`pos : `v`sphere.`w`pos) {
		`v`pos = `f`normalize(`v`pos);
	}

	return sphere;
}
)