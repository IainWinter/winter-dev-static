---
title: Making games with Falling Sand part 1
date: December 30, 2020
thumbnail: wZJCQQPaGZI.jpg
published: true
---

# Making games with Falling Sand part 1

![iframe-youtube-video](https://www.youtube.com/embed/wZJCQQPaGZI?start=6&rel=0 "Making games with Falling Sand part 1")

Simulating falling sand is no different from any other cellular automata. We have a big gird of cells and a set of rules that get applied to each cell every frame. You’ve probably heard of the [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). In that cellular automata, the rules are based on the number of neighbors surrounding a cell. For falling sand, we mostly look at if there is empty space below a cell for it to move into. This creates the look of particles cascading down.

One of the more interesting aspects of cellular automata is how complex behavior can emerge from such simple rules. That sounds like an interesting project could be created from only a few lines of code! Let’s look at how you could go about making one of these in the Java version of Processing. You can download Processing [here](https://processing.org/) if you want to follow along.

## Java version

We’ll start with the standard setup and draw functions. Before we fill these in, we should establish what our particles will be. For simplicity, color will determine the particle types, so let’s define some colors at the top.

~~~sketch.pde processing
`t`color `w`_EMPTY = `f`color(0);
`t`color `w`_SAND  = `f`color(255, 150, 50);

void `m`setup() { 
}

void `m`draw() {
}
~~~

In setup we need to set the size and background. I like to use a size of 800x800 pixels, and we need to set the background to the empty particle color. We should also uncap the framerate from 60 to allow this to run faster if it can.

~~~sketch.pde processing no_title
void `m`setup() {
  `f`size(800, 800);
  `f`background(`w`_EMPTY);
  `f`frameRate(1000);
}
~~~

Each time the draw function is called we will step our simulation. Because we are only using color, let’s use the pixels array as the storage for our cells. Each frame we need to call loadPixels to copy the displayed frame into the pixels array. This first frame will be all  _EMPTY because we called background.

~~~sketch.pde processing no_title
void `m`draw() {
  `f`loadPixels();
~~~

After we load the pixels, we can iterate over them and check if they match a particle type that we know about.

~~~sketch.pde processing no_title
  for (int `v`x = 0; `v`x < width;  `v`x++)
  for (int `v`y = 0; `v`y < height; `v`y++) {
    `t`color `v`cell = `f`get(`v`x, `v`y);
    
    if (`v`cell == `w`_SAND) {
~~~

We want sand to form dune like shapes, so let’s encode a pyramid into its rules. We need to check directly below, down to the left, and down to the right.

![article-embed-half](/articles/falling-sand-simulations/sand.png "Sand.png")

By default, it should move down if possible, but if that cell is occupied, we’ll check the other two directions.

~~~sketch.pde processing no_title
		boolean `v`down  = `w`isEmpty(`v`x,     `v`y + 1);
		boolean `v`left  = `w`isEmpty(`v`x - 1, `v`y + 1);
		boolean `v`right = `w`isEmpty(`v`x + 1, `v`y + 1);

		     if(`v`down)  `w`setCell(`v`x,     `v`y + 1, `w`_SAND);
		else if(`v`left)  `w`setCell(`v`x - 1, `v`y + 1, `w`_SAND);
		else if(`v`right) `w`setCell(`v`x + 1, `v`y + 1, `w`_SAND);

		if (`v`down || `v`left || `v`right) {
			`w`setCell(`v`x, `v`y, `w`_EMPTY); 
		}
	}
~~~

This looks ok, but the order of if statements matters. Because we put the left check before right, if both spaces are open, the particle will always move left. This creates an artificial look, but we can easily fix it by adding a little randomness to shuffle the direction if both cells are empty.

~~~sketch.pde processing no_title
	if (`v`left && `v`right) {
		boolean `v`rand = `f`random(1) > .5;
		`v`left  = `v`rand;
		`v`right = !`v`rand;
	}
~~~

Finally, we can close the for loops and call updatePixels to copy our frame to the display.

~~~sketch.pde processing no_title
	}

	`f`updatePixels();
}
~~~

To draw particles on the screen with the mouse, we can add these lines after loadPixels.

~~~sketch.pde processing no_title
	if (`p`mousePressed) {
		for (int `v`x = 0; `v`x < 1; `v`x++)
		for (int `v`y = 0; `v`y < 1; `v`y++) {
			`w`setCell(`p`mouseX + `v`x, `p`mouseY + `v`y, `w`_SAND);
		}
	}
~~~

You can create other particle types by adding more rules in a similar way. For example, water and a stationary barrier type are the most straight forward and where I would start. Water is like sand, but we check directly to the left and right instead of diagonal, which gives the effect of liquid flow. Barriers have no movement properties but fill space so the other types can’t move through them.

### Common issues

I saved the helper functions for last to highlight two common issues. The biggest gotcha with these types of simulations is that the order of iteration effects the behavior dramatically, and if we aren’t careful, we could end up updating particles multiple times or even lose them entirely.

~~~sketch.pde processing
boolean `w`inBounds(int `a`x, int `a`y) {
  return `a`x >= 0    && `a`y >= 0
      && `a`x < `p`width && `a`y < `p`height;
}

boolean `w`isEmpty(int `a`x, int `a`y) {
  return `w`inBounds(`a`x, `a`y) && `p`pixels[`a`x + `a`y * `p`width] == `w`_EMPTY;
}

void `w`setCell(int `a`x, int `a`y, color `a`cell) {
  `p`pixels[`a`x + `a`y * `p`width] = `a`cell;
}
~~~

We have four options for how we order the iteration. No matter which we pick, there will always be slight issues. Let’s see why.

If we iterate top to bottom, we end up updating the same particle multiple times. This results in a teleportation effect where a particle will only take a single frame to reach the floor. We could change the iteration to bottom to top, but then if we want particles that moves up, we run into the same issue. This highlights the fact that no matter which direction we pick, there will always be issues. Clearly, the solution must have more to it than just finding a magic ordering...

![iframe-youtube-video](https://www.youtube.com/embed/rh_AZGzRTcQ?rel=0 "teleport")

The band aid solution in this Processing version comes from the subtle details of how the pixel array works. In the helper functions we read and write to the pixels array, but in draw we use the get function. Even though the docs don’t say this, get must read from the displayed pixels array, which we don’t update until we call updatePixels. This allows us to dodge the issue of updating particles multiple times because nothing updates until the end of the frame from get’s perspective.

The second problem we can only mitigate. In isEmpty we don’t use get because we want information about the current frame as it updates. If we used get, two particles could both think a cell is empty, move in, and one would be lost. Even though we’ve somewhat fixed that issue, the order of iteration still matters. Now the order on the X axis determines who moves in first, so we still have inconsistent behavior.

Now that we have an idea of how the basics work, and common pitfalls, let’s jump over to C++ and see how these can be solved.

## C++ Version

I plan on expanding this over the next few videos, so I am going to try and make it more of a general sand framework. To start, we don’t want to edit the pixels directly because we want more properties than just color. Let’s make a CellType enum and store it in a Cell struct along with a Color. In the first version, sand and water both needed to check if the space directly below was free. This hints that the ways that the particles move doesn’t have to reflect their type. So, let’s keep two enums in each Cell, one for the movement properties and another the type. If we use a bit string for the properties, they can be combined to create more complex patterns.

~~~Cell.h cpp
enum `t`CellProperties {
	`d`NONE                = 0b00000000,
	`d`MOVE_DOWN           = 0b00000001,
	`d`MOVE_DOWN_SIDE      = 0b00000010,
	`d`MOVE_SIDE           = 0b00000100
};

enum `t`CellType {
	`d`EMPTY,
	`d`SAND,
	`d`WATER,
	`d`ROCK
};
 
struct `t`Cell {
	`t`CellType       `w`Type  = `t`CellType::`d`EMPTY;
	`t`CellProperties `w`Props = `t`CellProperties::`d`NONE;

	`t`Color `w`Color; // rgba
};
~~~

Now that we have defined our Cell, we need a way to store them. Let’s make a new class called SandWorld and store an array of Cells in it. In the constructor we can specify a width, height, and scale in pixels. This will allow us to easily change the size of the cells.

~~~SandWorld.h cpp
class `t`SandWorld {
public:
	const size_t m_width  = 0;
	const size_t m_height = 0;
	const double m_scale = 1;
private:
	`t`Cell* m_cells = nullptr;

public:
	`f`SandWorld(size_t `a`width, size_t `a`height, double `a`scale)
		: m_width  (`a`width  / `a`scale)
		, m_height (`a`height / `a`scale)
		, m_scale  (`a`scale)
	{
		m_cells = new `t`Cell[m_width * m_height];
	}

	`f`~SandWorld() {
		delete[] m_cells;
	}
~~~

We’ll need some functions for getting the cells out of the world, let’s add two: one that takes x and y coordinates, and another that takes a flat index.

~~~SandWorld.h cpp no_title
	const `t`Cell& `f`GetCell(size_t `a`index) {
		return m_cells[`a`index]; 
	}

	const `t`Cell& `f`GetCell(size_t `a`x, size_t `a`y) {
		return `f`GetCell(`f`GetIndex(`a`x, `a`y));
	}

	size_t `f`GetIndex(size_t `a`x, size_t `a`y) {
		return `a`x + `a`y * m_width;
	}
~~~

And to get us back to where we were, let’s add the same helper functions from before.

~~~SandWorld.h cpp no_title
	bool `f`InBounds(size_t `a`x, size_t `a`y) {
		return `a`x < m_width 
			&& `a`y < m_height;
	}

	bool `f`IsEmpty(size_t `a`x, size_t `a`y) {
		return `f`InBounds(`a`x, `a`y) 
			&& `f`GetCell(`a`x, `a`y).`w`Type == `t`CellType::`d`EMPTY;
	}

	void `f`SetCell(size_t `a`x, size_t `a`y, const `t`Cell& `a`cell) {
		m_cells[GetIndex(`a`x, `a`y)] = `a`cell;
	}
~~~

Processing gave us two arrays to work with, but before we just add another one and call it a day, let’s think about a way to actually solve the issues that arise from the iteration ordering. The main problem is that moves are executed as they come, but really, we should gather all the possible moves, then execute them at the end to give each one a fair chance.

Let’s add a vector to the SandWorld, and make a new function called MoveCell that adds a move to the list.

~~~SandWorld.h cpp no_title
	std::vector<std::pair<size_t, size_t>> m_changes; // destination, source

	void `f`MoveCell(size_t `a`x, size_t `a`y, size_t `a`xto, size_t `a`yto)
	{
		m_changes.`f`emplace_back(
			`f`GetIndex(`a`xto, `a`yto),
			`f`GetIndex(`a`x,   `a`y)
		);
	}
~~~

After we finish iterating over our cells, we can apply the changes. First, we need to remove any changes that were filled between frames by the SetCell function.

~~~SandWorld.h cpp no_title
	void `f`CommitCells() {
		// remove moves that have their destinations filled

		for (size_t `v`i = 0; `v`i < m_changes.`f`size(); `v`i++) {
			if (m_cells[m_changes[`v`i].`w`first].`w`Type != `t`CellType::`d`EMPTY) {
				m_changes[`v`i] = m_changes.`f`back(); m_changes.`f`pop_back();
				`v`i--;
			}
		}
~~~

Then we need to sort the list of moves by their destination. This is an unfortunate slowdown but allows us to add and choose moves quicker. We could use a multimap, but the slowdown from accessing the linked lists outweighs the sort.

~~~SandWorld.h cpp no_title
		// sort by destination

		std::`f`sort(m_changes.begin(), m_changes.`f`end(),
			[](auto& `a`a, auto& `a`b) { return `a`a.`w`first < `a`b.`w`first; }
		);
~~~

Then we can iterate over the sorted moves. Each time the destination changes, we’ll pick a random source to move from. This allows each particle to get a fair chance at moving into to a cell. Finally, we’ll clear the list.

~~~SandWorld.h cpp no_title
		// pick random source for each destination

		size_t `v`iprev = 0;

		m_changes.`f`emplace_back(-1, -1); // to catch final move

		for (size_t `v`i = 0; `v`i < m_changes.`f`size() - 1; `v`i++) {
			if (m_changes[`v`i + 1].first != m_changes[`v`i].`w`first) {
				size_t `v`rand = `v`iprev + `f`rand_int(`v`i - `v`iprev);

				size_t `v`dst = m_changes[`v`rand].`w`first;
				size_t `v`src = m_changes[`v`rand].`w`second;

				m_cells[`v`dst] = m_cells[`v`src];
				m_cells[`v`src] = `t`Cell();

				`v`iprev = `v`i + 1;
			}
		}

		m_changes.`f`clear();
	}
};
~~~

That’s it for the core of our little framework, let’s see how we can use it to make what we had in the Processing version. I am going to skip over the rendering details because C++ makes that really annoying. I suggest checking out [SDL](https://www.libsdl.org/) if you don't already have your own solution.

In an Update function, we’ll iterate over the cells in a similar way as before, but now that we have a bit string of movement properties, we can check each one until its respective MoveX function returns true.

~~~Main.cpp cpp
`t`SandWorld m_world = `t`SandWorld(1920, 1080, 2);

void `f`Update() {
	// Update cells

	for (size_t `v`x = 0; `v`x < m_world.m_width;  `v`x++)
	for (size_t `v`y = 0; `v`y < m_world.m_height; `v`y++) {
		const `t`Cell& `v`cell = m_world.`f`GetCell(`v`x, `v`y);

			 if (`v`cell.`w`Props & `t`CellProperties::`d`MOVE_DOWN      && `f`MoveDown    (`v`x, `v`y, `v`cell)) {}
		else if (`v`cell.`w`Props & `t`CellProperties::`d`MOVE_DOWN_SIDE && `f`MoveDownSide(`v`x, `v`y, `v`cell)) {}
		else if (`v`cell.`w`Props & `t`CellProperties::`d`MOVE_SIDE      && `f`MoveSide    (`v`x, `v`y, `v`cell)) {}
	}

	m_world.`f`CommitCells();

	// Update the sand texture
	// Draw the sand to the screen
}
~~~

We can make a function for each movement property that will return true if it finds a valid move.

~~~Main.cpp cpp no_title
bool `f`MoveDown(size_t `a`x, size_t `a`y, const Cell& `a`cell)
{
	bool `v`down = m_world.`f`IsEmpty(`a`x, `a`y - 1);
	if (`v`down) {
		m_world.`f`MoveCell(`a`x, `a`y, `a`x, `a`y - 1);
	}

	return `v`down;
}

bool `f`MoveDownSide(size_t `a`x, size_t `a`y, const Cell& `a`cell)
{
	bool `v`downLeft  = m_world.`f`IsEmpty(`a`x - 1, `a`y - 1);
	bool `v`downRight = m_world.`f`IsEmpty(`a`x + 1, `a`y - 1);

	if (`v`downLeft && `v`downRight) {
		`v`downLeft  = rand_float() > 0;
		`v`downRight = !`v`downLeft;
	}

		 if (`v`downLeft)  m_world.`f`MoveCell(`a`x, `a`y, `a`x - 1, `a`y - 1);
	else if (`v`downRight) m_world.`f`MoveCell(`a`x, `a`y, `a`x + 1, `a`y - 1);

	return `v`downLeft || `v`downRight;
}
~~~

To draw particles with the mouse, we can create some defaults in an Init function...

~~~Main.cpp cpp no_title
`t`Cell `w`_EMPTY, `w`_SAND, `w`_WATER, `w`_ROCK;
	
void `f`Initialize() { 
	`w`_EMPTY = {
		`t`CellType::`d`EMPTY,
		`t`CellProperties::`d`NONE,
		`t`Color::`f`From255(0, 0, 0, 0) // 0 alpha allows for a background
	};
	
	`w`_SAND = {
		`t`CellType::`d`SAND,
		`t`CellProperties::`d`MOVE_DOWN | `t`CellProperties::`d`MOVE_DOWN_SIDE,
		`t`Color::`f`From255(235, 200, 175)
	};
	
	`w`_WATER = {
		`t`CellType::`d`WATER,
		`t`CellProperties::`d`MOVE_DOWN | `t`CellProperties::`d`MOVE_SIDE,
		`t`Color::`f`From255(175, 200, 235)
	};
	
	`w`_ROCK = {
		`t`CellType::`d`ROCK,
		`t`CellProperties::`d`NONE,
		`t`Color::`f`From255(200, 200, 200)
	};
	
	// Init a texture for sand...
}
~~~

Then at the top of our update function, we’ll add these lines.

~~~Main.cpp cpp no_title
void `f`Update() {
	if (`t`Mouse::`f`ButtonDown(`d`LMOUSE)) {
		`t`vector2 `v`pos = `t`Mouse::`f`ScreenPos() / m_world.m_scale;
		`v`pos.`w`y = m_world.m_height - `v`pos.`w`y;

		`t`Cell `v`placeMe = _EMPTY;

			 if (`t`Keyboard::`f`KeyDown(`d`S)) `v`placeMe = `w`_SAND;
		else if (`t`Keyboard::`f`KeyDown(`d`W)) `v`placeMe = `w`_WATER;
		else if (`t`Keyboard::`f`KeyDown(`d`R)) `v`placeMe = `w`_ROCK;

		for (size_t `v`x = `v`pos.`w`x; `v`x < `v`pos.`w`x + 20; `v`x++)
		for (size_t `v`y = `v`pos.`w`y; `v`y < `v`pos.`w`y + 20; `v`y++) 
		{
			if (!m_world.`f`InBounds(`v`x, `v`y)) 
				continue;
			
			m_world.`f`SetCell(`v`x, `v`y, `v`placeMe);
		}
	}

	// Update cells
	// Copy sand colors to a texture
	// Draw the texture on the screen
}
~~~

The last thing I want to cover is about making games inside of these simulations. Let’s think about the most basic feature we need, then in future posts I’ll expand on this.

Having a player that moves around seems like a good place to start, so let’s think about how that might work. We’ll need some notion of a group of particles that can move together. Let’s make a Tile struct that holds a list of positions for its particles, and a position for the group itself. For now, we’ll just use the _ROCK particle for everything in the tile.

~~~Tile.h cpp
struct `t`Tile {
	std::vector<std::pair<int, int>> `w`Positions;
	int `w`X = 0;
	int `w`Y = 0;
};
~~~

Before we update the world, we need to paste the tile particles in, so let’s put these lines in the Update function before the main loops. After we’ve called CommitCells and updated the texture, we can remove the tiles by setting their cells to _EMPTY.

~~~main.cpp cpp
std::vector<`t`Tile> m_tiles;

void `f`Update() {
	// Draw cells with mouse

	for (`t`Tile& `v`tile : m_tiles) {
		for (auto [`v`x, `v`y] : `v`tile.`w`Positions) {
			`v`x += `v`tile.`w`X;
			`v`y += `v`tile.`w`Y;

			if (m_world.`f`InBounds(`v`x, `v`y)) {
				// what happens if the cell is already full?
				m_world.`f`SetCell(`v`x, `v`y, `w`_ROCK);
			}
		}
	}

	// Update cells
	// Copy sand colors to a texture
	// Draw the texture on the screen

	for (`t`Tile& `v`tile : m_tiles) {
		for (auto [`v`x, `v`y] : `v`tile.`w`Positions) {
			`v`x += `v`tile.`w`X;
			`v`y += `v`tile.`w`Y;

			if (m_world.`f`InBounds(`v`x, `v`y)) {
				// what happens if the cell is no longer part of the tile?
				m_world.`f`SetCell(`v`x, `v`y, `w`_EMPTY);
			}
		}
	}
}
~~~

Finally, we can make a little ship and add some basic movement. In the Init function, we’ll make a Tile and add it to the list.

~~~main.cpp cpp no_title
void `f`Initialize() { 
	`t`Tile `v`ship = {
		{
						  {2,6},
				   {1,5}, {2,5}, 
			{0,4}, {1,4}, {2,4}, {3,4},
			{0,3}, {1,3}, {2,3}, {3,3},
			{0,2},               {3,2},
			{0,1},               {3,1},
			{0,0},               {3,0},
		},
		200, 200
	};

	m_tiles.`f`push_back(`v`ship);

	// Create default cells
	// Init a texture for sand...
}
~~~

In the Update function, before the world updates, we can add these lines to move our ship. It’s important to move the tiles before pasting them in so they can be removed correctly at the end.

~~~main.cpp cpp no_title
void `f`Update() {
	// Draw cells with mouse

	if (`t`Keyboard::`f`KeyDown(`d`LEFT))  m_tiles[0].`w`X -= 1;
	if (`t`Keyboard::`f`KeyDown(`d`RIGHT)) m_tiles[0].`w`X += 1;
	if (`t`Keyboard::`f`KeyDown(`d`UP))    m_tiles[0].`w`Y += 1;
	if (`t`Keyboard::`f`KeyDown(`d`DOWN))  m_tiles[0].`w`Y -= 1;

	// Paste tiles
	// Update cells
	// Copy sand colors to a texture
	// Draw the texture on the screen
	// Remove tiles
}
~~~

And that about covers it, we’re left with a decently quick simulation. On my computer this runs between 0.005 - .015 seconds per frame. Which is around 200 – 60 fps. Currently we can only use 1 thread, so if your computer has 4 cores we are only using 1/4th or more likely only 1/8th of its power :(

![iframe-youtube-video](https://www.youtube.com/embed/_r8p1FOH9j0?rel=0 "Sand Demo")

In the next post, I am going to cover how we could make the world bigger, and how multi-threading the simulation works. Then we’ll make a game with it, so stay tuned if this seems interesting!
