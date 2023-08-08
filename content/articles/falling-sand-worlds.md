---
title: Making an infinite world with Falling Sand part 2
date: March 27, 2021
thumbnail: vNcsPE_YdmA.jpg
published: true
---

# Making an infinite world with Falling Sand part 2

![iframe-youtube-video](https://www.youtube.com/embed/vNcsPE_YdmA?rel=0 "Making an infinite world with Falling Sand part 2")

Welcome back to the sand series, this post directly follows from what we did last time, so if you missed that, here's the [link](/articles/falling-sand-simulations). In this post we’ll first split the world into chunks, then look at some ways to speed it up.

## Splitting the world into chunks

The main feature that chunks allow for is expanding the world quickly. Let’s look at the two extreme solutions, and then why chunks are the obvious way to go.

If we store the world in a single list, whenever the player reaches the edge, the whole list needs to be reallocated. This would be fine for smaller worlds, but with bigger worlds becomes impractical. Another approach would be to store each cell in a map. This would allow for an expanding world but is crippled by very slow iteration caused by the memory being scattered all over the place.

The solution comes from mixing the two together. If we store small lists in a map, we can have fast iteration, while also being able to expand the world without copying anything. These lists will act as our chunks, and if each one is a fixed size, some simple math can find the corresponding one from a world coordinate. Whenever the player wants to expand the world, we just add more chunks into the map. This only takes minimal work to implement. Each chunk is just like a small world, all we need to account for is that a particle could move from one chunk to another.

We ended last time with a SandWorld class that contained some simple functions for getting, setting, and moving cells. Let’s copy those, along with the member variables to a new class called SandChunk.

There are only few changes we need to make. First, we’ll add member variables for the chunk’s world position, and edit GetIndex and InBounds to account for these. We’ll also need to change all the functions that take x and y from unsigned to signed ints, as world coordinates contain negative numbers. Originally, I had tried to convert from world coordinates to chunk coordinates in the world, but that was a headache, this way there is only one coordinate system all the way down.

~~~SandChunk.h cpp
class `t`SandChunk {
public:
	const int m_width, m_height;
	const int m_x, m_y;
private:
	`t`Cell* m_cells;
	std::vector<std::pair<size_t, size_t>> m_changes; // destination, source
 
public:
	`f`SandChunk(size_t `a`width, size_t `a`height, int `a`x, int `a`y)
		: m_width  (`a`width)
		, m_height (`a`height)
		, m_x      (`a`x)
		, m_y      (`a`y)
	{
		m_cells = new `t`Cell[`a`width * `a`height];
	}
 
	`f`~SandChunk() {
		delete[] m_cells;
	}
 
	size_t `f`GetIndex(int `a`x, int `a`y) {
		return (`a`x - m_x)
		     + (`a`y - m_y) * m_width;
	}
 
	bool `f`InBounds(int `a`x, int `a`y) {
		return `a`x >= m_x && `a`x < m_x + m_width
		    && `a`y >= m_y && `a`y < m_y + m_height;
	}
 
	bool `f`IsEmpty(int `a`x, int `a`y) { return `f`IsEmpty(`f`GetIndex(`a`x, `a`y); }
	bool `f`IsEmpty(size_t `v`index) { return `f`GetCell(`v`index).Type == `t`CellType::`d`EMPTY; }
 
 
	`t`Cell& `f`GetCell(int `a`x, int `a`y) { return `f`GetCell(`f`GetIndex(`a`x, `a`y)); }
	`t`Cell& `f`GetCell(size_t index) { return m_cells[index]; }
 
	void `f`SetCell(int `a`x, int `a`y, const `t`Cell& `a`cell) { `f`SetCell(`f`GetIndex(`a`x, `a`y), `a`cell); }
	void `f`SetCell(size_t `v`index, const `t`Cell& `a`cell) { m_cells[`v`index] = `a`cell; }
~~~

The second edit we’ll make allows for particles to move from one chunk to another. Let’s edit the m_changes list to store tuples and add a SandChunk* along with the indices from before.

~~~SandChunk.h cpp
	std::vector<std::tuple<`t`SandChunk*, size_t, size_t>> m_changes; // source chunk, source, destination
	
	void `f`MoveCell(`t`SandChunk* `a`source, int `a`x, int `a`y, int `a`xto, int `a`yto)
	{
		m_changes.`f`emplace_back(
			`a`source,
			`a`source->`f`GetIndex(`a`x, `a`y),
			`f`GetIndex(`a`xto, `a`yto)
		);
	}
~~~

In CommitCells, any .first or .second needs to be changed to std::get<>. Where we set the cell’s data, instead of writing directly to m_cells, we’ll use GetCell and SetCell with the source chunk.

~~~SandChunk.h cpp
	#define `p`_DEST(x) std::`f`get<2>(x)
 
	void `f`CommitCells() { 
		// remove moves that have their destinations filled
 
		for (size_t `v`i = 0; i < m_changes.`f`size(); `v`i++) {
			if (!`f`IsEmpty(`p`_DEST(m_changes[`v`i]))) {
				m_changes[`v`i] = m_changes.`f`back(); m_changes.`f`pop_back();
				`v`i--;
			}
		}
 
		// sort by destination
 
		std::`f`sort(m_changes.`f`begin(), m_changes.`f`end(),
			[](auto& `a`a, auto& `a`b) { return `p`_DEST(`a`a) < `p`_DEST(`a`b); }
		);
 
		// pick random source for each destination
 
		size_t `v`iprev = 0;
 
		m_changes.`f`emplace_back(nullptr, -1, -1); // to catch final move
 
		for (size_t `v`i = 0; `v`i < m_changes.`f`size() - 1; `v`i++) {
			if (`p`_DEST(m_changes[`v`i + 1]) != `p`_DEST(m_changes[`v`i])) {
				size_t `v`rand = `v`iprev + `f`rand_int(`v`i - `v`iprev);
 
				auto [`v`chunk, `v`src, `v`dst] = m_changes[`v`rand];
 
				       `f`SetCell(`v`dst, `v`chunk->`f`GetCell(`v`src));
				`v`chunk->`f`SetCell(`v`src, `t`Cell());
 
				`v`iprev = `f`i + 1;
			}
		}
 
		m_changes.`f`clear();
	}
};
~~~

Now that we have chunks that can work together, we need to coordinate them in the SandWorld. Let’s replace every function from before with one that gets a chunk, then calls its respected function.

~~~SandWorld.h cpp
class `t`SandWorld {
public:
	const size_t m_chunkWidth;
	const size_t m_chunkHeight;
	const double m_scale;
	
public:
	`f`SandWorld(size_t `a`chunkWidth, size_t `a`chunkHeight, double `a`scale)
		: m_chunkWidth  (`a`chunkWidth  / `a`scale)
		, m_chunkHeight (`a`chunkHeight / `a`scale)
		, m_scale       (`a`scale)
	{}
 
	bool `f`InBounds(int `a`x, int `a`y) {
		if (`t`SandChunk* `v`chunk = `f`GetChunk(`a`x, `a`y)) {
			return `v`chunk->`f`InBounds(`a`x, `a`y);
		}
 
		return false;
	}
 
	bool `f`IsEmpty(int `a`x, int `a`y) {
		return `f`InBounds(`a`x, `a`y)
		    && `f`GetChunk(`a`x, `a`y)->`f`IsEmpty(`a`x, `a`y);
	}
 
	`t`Cell& `f`GetCell(int `a`x, int `a`y) {
		return `f`GetChunk(`a`x, `a`y)->`f`GetCell(`a`x, `a`y);
	}
 
	void `f`SetCell(int `a`x, int `a`y, const Cell& `a`cell) {
		if (`t`SandChunk* `v`chunk = `f`GetChunk(`a`x, `a`y)) {
			`v`chunk->`f`SetCell(`a`x, `a`y, `a`cell);
		}
	}
 
	void `f`MoveCell(int `a`x, int `a`y, int `a`xto, int `a`yto) {
		if (`t`SandChunk* `a`src = `f`GetChunk(`a`x, `a`y))
		if (`t`SandChunk* `a`dst = `f`GetChunk(`a`xto, `a`yto)) {
			`a`dst->`f`MoveCell(`a`src, `a`x, `a`y, `a`xto, `a`yto);
		}
	}
~~~

The final piece we need to add is storage for the chunks. I opted for a vector of SandChunk* for iteration, and a map to look them up by coordinate.

~~~SandWorld.h cpp
	std::vector<`t`SandChunk*> m_chunks;
	std::unordered_map<std::pair<int, int>, `t`SandChunk*, `t`pair_hash> m_chunkLookup;
~~~

Pair hash is defined as the (first hash * #) ^ second hash

~~~pair_hash.h cpp
struct `t`pair_hash {
	template<typename `t`T1, typename `t`T2>
	size_t operator() (const std::pair<`t`T1, `t`T2>& `a`pair) const {
		return ( std::`f`hash<`t`T1>()(`a`pair.`w`first) * `d`0x1f1f1f1f)
			   ^ std::`f`hash<`t`T2>()(`a`pair.`w`second);
	}
};
~~~

Now that we have our containers, we can make GetChunk. First, we’ll convert the world coordinates into a chunk location, then we’ll get the chunk or create a new one. To create a new chunk, let’s make a function called CreateChunk and pass it the location. Here, we can define the world boundaries; if the location is inside, we’ll make a new chunk, add it to the containers and return.

~~~SandWorld.h cpp
	`t`SandChunk* `f`GetChunk(int `a`x, int `a`y) {
		auto `v`location = `f`GetChunkLocation(`a`x, `a`y);
		`t`SandChunk* `v`chunk = `f`GetChunkDirect(`v`location);
 
		return `v`chunk ? `v`chunk : CreateChunk(`v`location);
	}
 
	`t`SandChunk* `f`GetChunkDirect(std::pair<int, int> `a`location) {
		auto `v`itr = m_chunkLookup.`f`find(`a`location);
		auto `v`end = m_chunkLookup.`f`end();
 
		return `v`itr != `v`end ? `v`itr->`w`second : nullptr;
	}
 
	std::pair<int, int> `f`GetChunkLocation(int `a`x, int `a`y) {
		return { `f`floor(float(`a`x) / m_chunkWidth),
		         `f`floor(float(`a`y) / m_chunkHeight)};
	}
private:
	`t`SandChunk* `f`CreateChunk(std::pair<int, int> `a`location) {
		auto [`v`lx, `v`ly] = `a`location;
 
		if (   `v`lx < -10 || `v`ly < -10 
		    || `v`lx >  10 || `v`ly >  10) // could pass in a world limit to constructor
		{
			return nullptr;
		}
 
		`t`SandChunk* `v`chunk = new `t`SandChunk(m_chunkWidth, m_chunkHeight, `v`lx, `v`ly);
 
		m_chunkLookup.`f`insert({ `a`location, `v`chunk });
		m_chunks.`f`push_back(`v`chunk);
 
		return `v`chunk;
	}
~~~

Finally, the Update function needs to be edited to iterate over the chunks.

~~~SomeClass.h cpp
`t`SandWorld m_world = `t`SandWorld(200, 200, 2); // in a class somewhere

void `f`Update() {
	// Draw cells with mouse
	// Paste tiles

	// Update cells

	for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
		for (size_t `v`x = 0; `v`x < `v`chunk->m_width;  `v`x++)
		for (size_t `v`y = 0; `v`y < `v`chunk->m_height; `v`y++) {
			`t`Cell& `v`cell = `v`chunk->`f`GetCell(`v`x + `v`y * `v`chunk->m_width);

			int `v`px = `v`x + `v`chunk->m_x;
			int `v`py = `v`y + `v`chunk->m_y;

			     if (`v`cell.`w`Props & `t`CellProperties::`d`MOVE_DOWN      && `f`MoveDown    (`v`px, `v`py, `v`cell)) {}
			else if (`v`cell.`w`Props & `t`CellProperties::`d`MOVE_DOWN_SIDE && `f`MoveDownSide(`v`px, `v`py, `v`cell)) {}
			else if (`v`cell.`w`Props & `t`CellProperties::`d`MOVE_SIDE      && `f`MoveSide    (`v`px, `v`py, `v`cell)) {}
		}
	}

	for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
		`v`chunk->`f`CommitCells();
	}

	// Copy sand colors to a texture
	// Draw the texture on the screen
	// Remove tiles
}
~~~

And with that, we have chunked the world. I’ve made the texture draw a red pixel on the boundary of each chunk so we can see them. While I’m at it, I’ve made the camera center around the player so now we can fly around and see chunks all around us.

![iframe-youtube-video](https://www.youtube.com/embed/29iiIUi9_kE?rel=0 "Chunks Everywhere & Empty Chunks")

## Performance

Optimization is something that never ends, so I am going to only look at a few of the most bang for buck areas we can smooth out.

Let’s start with something small. Currently, every time a world function gets called, it needs to find a chunk from the map. These can’t be expected to be in the cache, so hitting this map for every cell will add up to a considerable loss of time. To get around this, let’s make a SandWorker class that stores a chunk from the map, then only calls back to the world if necessary. This also gives us a nice way to hook into the engine with other custom behaviors.

~~~SandWorker.h cpp
class `t`SandWorker {
protected:
	`t`SandWorld& m_world;
	`t`SandChunk* m_chunk;
 
public:
	`f`SandWorker(`t`SandWorld& world, `t`SandChunk* chunk)
		: m_world (world)
		, m_chunk (chunk)
	{}
 
	void `f`UpdateChunk() {
		for (int `v`x = 0; `v`x < m_chunk->m_width;  `v`x++)
		for (int `v`y = 0; `v`y < m_chunk->m_height; `v`y++) {
			`t`Cell& `v`cell = m_chunk->`f`GetCell(`v`x + `v`y * m_chunk->m_width);
 
			int px = `v`x + m_chunk->m_x;
			int py = `v`y + m_chunk->m_y;
 
			`f`UpdateCell(`v`px, `v`py, `v`cell);
		}
	}
 
	virtual void `f`UpdateCell(int `a`x, int `a`y, `t`Cell& `a`cell) = 0;
 
	`t`Cell& `f`GetCell(int x, int y) {
		if (m_chunk->`f`InBounds(x, y)) {
			return m_chunk->`f`GetCell(x, y);
		}
 
		return m_world.`f`GetCell(x, y);
	}
 
	void `f`SetCell(int `a`x, int `a`y, const `t`Cell& `a`cell) {
		if (m_chunk->`f`InBounds(`a`x, `a`y)) {
			return m_chunk->`f`SetCell(`a`x, `a`y, `a`cell);
		}
 
		return m_world.`f`SetCell(`a`x, `a`y, `a`cell);
	}
 
	void `f`MoveCell(int `a`x, int `a`y, int `a`xto, int `a`yto) {
		if (   m_chunk->`f`InBounds(`a`x, `a`y)
		    && m_chunk->`f`InBounds(`a`xto, `a`yto))
		{
			return m_chunk->`f`MoveCell(m_chunk, `a`x, `a`y, `a`xto, `a`yto);
		}
 
		return m_world.`f`MoveCell(`a`x, `a`y, `a`xto, `a`yto);
	}
 
	bool `f`InBounds(int `a`x, int `a`y) {
		return m_chunk->`f`InBounds(`a`x, `a`y)
		    || m_world .`f`InBounds(`a`x, `a`y);
	}
 
	bool `f`IsEmpty(int `a`x, int `a`y) {
		if (m_chunk->`f`InBounds(`a`x, `a`y)) {
			return m_chunk->`f`IsEmpty(`a`x, `a`y);
		}
 
		return m_world.`f`IsEmpty(`a`x, `a`y);
	}
};
~~~

Now we can override this class and put our custom cell behaviors in it.

~~~SimpleSandWorker.h cpp
class `t`SimpleSandWorker : public `t`SandWorker {
public:
	`f`SimpleSandWorker(`t`SandWorld& `a`world, `t`SandChunk* `a`chunk) 
		: `t`SandWorker (`a`world, `a`chunk) 
	{}
 
	void `f`UpdateCell(int `a`x, int `a`y, `t`Cell& `a`cell) override {
		     if (`a`cell.`w`Props & `t`CellProperties::`d`MOVE_DOWN      && `f`MoveDown    (`a`x, `a`y, `a`cell)) {}
		else if (`a`cell.`w`Props & `t`CellProperties::`d`MOVE_DOWN_SIDE && `f`MoveDownSide(`a`x, `a`y, `a`cell)) {}
		else if (`a`cell.`w`Props & `t`CellProperties::`d`MOVE_SIDE      && `f`MoveSide    (`a`x, `a`y, `a`cell)) {}
	}
private:
	bool `f`MoveDown    (int `a`x, int `a`y, const `t`Cell& `a`cell) { /* ... */ }
	bool `f`MoveDownSide(int `a`x, int `a`y, const `t`Cell& `a`cell) { /* ... */ }
	bool `f`MoveSide    (int `a`x, int `a`y, const `t`Cell& `a`cell) { /* ... */ }
};
~~~

To make use of this, let’s edit the Update function. You could add a list of these in the world, but for now I’ll just hard code this one.

~~~SomeClass.h cpp
void `f`Update() {
	// Draw cells with mouse
	// Paste tiles

	for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
		`t`SimpleSandWorker(m_world, `v`chunk).`f`UpdateChunk();
	}

	for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
		`v`chunk->`f`CommitCells();
	}

	// Copy sand colors to a texture
	// Draw the texture on the screen
	// Remove tiles
}
~~~

The biggest time sink is iterating over the cells, so anything we can do to cutdown on the number we need to check will improve the frame rate dramatically. The most obvious is that most chunks are completely empty, so we could delete those and remove them from iteration entirely.

To do this, let’s add a count of filled cells in the SandChunk. When setting a cell, if the source is filled but the destination isn’t, we’ll increment by one. Inversely, if the destination is filled and we are setting it to empty, we’ll decrement.

~~~SandChunk.h cpp
	size_t m_filledCellCount;
 
	void `f`SetCell(size_t `a`index, const `t`Cell& `a`cell)
	{
		`t`Cell& `v`dest = m_cells[`a`index];
 
		if (   `v`dest.Type == `t`CellType::`d`EMPTY
		    && `a`cell.Type != `t`CellType::`d`EMPTY) // Filling a cell
		{
			m_filledCellCount++;
		}
 
		else
		if (   `v`dest.Type != `t`CellType::`d`EMPTY
			&& `a`cell.Type == `t`CellType::`d`EMPTY) // Removing a filled cell
		{
			m_filledCellCount--;
		}
 
		`v`dest = `a`cell;
	}
~~~

In the SandWorld, let’s add a new function called RemoveEmptyChunks.

~~~SandWorld.h cpp
void `f`RemoveEmptyChunks() {
	for (size_t `v`i = 0; `v`i < m_chunks.`f`size(); `v`i++) {
		`t`SandChunk* `v`chunk = m_chunks.`f`at(`v`i);
 
		if (`v`chunk->m_filledCellCount == 0) {
			m_chunkLookup.`f`erase(`f`GetChunkLocation(`v`chunk->m_x, `v`chunk->m_y));
			m_chunks[`v`i] = m_chunks.`f`back(); m_chunks.`f`pop_back();
			`v`i--;
 
			delete `v`chunk;
		}
	}
}
~~~

Then call it before the world update.

~~~SomeClass.h cpp
void `f`Update() {
	// Draw cells with mouse
	// Paste tiles

	m_world.`f`RemoveEmptyChunks();

	// Update cells

	// Copy sand colors to a texture
	// Draw the texture on the screen
	// Remove tiles
}
~~~

If we look back at the chunk visualization, there are now only chunks where there are filled cells.

![iframe-youtube-video](https://www.youtube.com/embed/X5Uwk63wLP4?rel=0 "No empty chunks but rocks still iterated")

However, we still iterate over the static cells like rocks. This brings us to the second optimization. If a chunk only has a single filled cell, every cell is still iterated. We could though, select only a subsection to iterate. This technique is commonly referred to as a dirty rectangle and used in UI painting to save time by not redrawing static elements.

Whenever a cell gets set or moved, this rectangle needs to expand to contain it for the next update. We can’t expand this rectangle during an update, so we need to double buffer it like we did for the initial [Processing version](/articles/falling-sand-simulations#java-version) of the cells array. To implement this, let’s add a min/max x and y to the SandChunk along with two functions named UpdateRect and KeepAlive.

~~~SandChunk.h cpp
public:
	int m_minX, m_minY,
	    m_maxX, m_maxY;   // Dirty rect
private:
	int m_minXw, m_minYw,
	    m_maxXw, m_maxYw; // Working dirty rect
 
public:
	void `f`KeepAlive(int `a`x, int `a`y) {
		`f`KeepAlive(`f`GetIndex(`a`x, `a`y));
	}
 
	void `f`KeepAlive(size_t `a`index) {
		int `a`x = `a`index % m_width;
		int `a`y = `a`index / m_width;
 
		m_minXw = `f`clamp(`f`min(`v`x - 2, m_minXw), 0, m_width);
		m_minYw = `f`clamp(`f`min(`v`y - 2, m_minYw), 0, m_height);
		m_maxXw = `f`clamp(`f`max(`v`x + 2, m_maxXw), 0, m_width);
		m_maxYw = `f`clamp(`f`max(`v`y + 2, m_maxYw), 0, m_height);
	}
 
	void `f`UpdateRect() {
		// Update current; reset working
		m_minX = m_minXw;  m_minXw = m_width;
		m_minY = m_minYw;  m_minYw = m_height;
		m_maxX = m_maxXw;  m_maxXw = -1;
		m_maxY = m_maxYw;  m_maxYw = -1;	
	}
~~~

Then in SetCell, we’ll pass the index to KeepAlive.

~~~SandChunk.h cpp
	void `f`SetCell(size_t `a`index, const `t`Cell& `a`cell)
	{
		// Set cell & update count

		`f`KeepAlive(`a`index);
	}
~~~

Because the chunks can update each other’s rectangles, we need to wait for all the chunks to be committed before calling UpdateRect. To do this, let’s add another loop after committing the cells in the main update.

Now, in the SandWorker’s Update function, instead of iterating from 0 to the boundary, we can iterate from the min to the max of the rectangle.

~~~SandChunk.h cpp
	void `f`UpdateChunk() {
		for (int `v`x = m_chunk->m_minX; `v`x < m_chunk->m_maxX; `v`x++)
		for (int `v`y = m_chunk->m_minY; `v`y < m_chunk->m_maxY; `v`y++) {
			`t`Cell& `v`cell = m_chunk->`f`GetCell(`v`x + `v`y * m_chunk->m_width);
 
			int px = `v`x + m_chunk->m_x;
			int py = `v`y + m_chunk->m_y;
 
			`f`UpdateCell(`v`px, `v`py, `v`cell);
		}
	}
~~~

I was under the impression that this was all that was required, but if we look at the boundary of a sleeping chunk, the cells don’t wake up correctly. This happens because the rectangles are bounded by the chunks and they can’t talk to their neighbors.

![iframe-youtube-video](https://www.youtube.com/embed/8K1UN0H5X0w?rel=0 "Broken Dirty Rect")

We need a way to notify the chunks that an update has happened on their border. Let’s add a KeepAlive function to the world,

~~~SandWorld.h cpp
	void `f`KeepAlive(int `a`x, int `a`y) {
		if (`t`SandChunk* `v`chunk = `f`GetChunk(`a`x, `a`y)) {
			`v`chunk->`f`KeepAlive(`a`x, `a`y);
		}
	}
~~~

and for now just edit MoveCell in the SandWorker to use it.

~~~SandWorker.h cpp
	void `f`MoveCell(int `a`x, int `a`y, int `a`xto, int `a`yto)
	{
		int `v`pingX = 0, `v`pingY = 0;
 
		if (`a`x == m_chunk->m_x)                         `v`pingX = -1;
		if (`a`x == m_chunk->m_x + m_chunk->m_width  - 1) `v`pingX =  1;
		if (`a`y == m_chunk->m_y)                         `v`pingY = -1;
		if (`a`y == m_chunk->m_y + m_chunk->m_height - 1) `v`pingY =  1;
 
		if (`v`pingX != 0)               m_world.`f`KeepAlive(`a`x + `v`pingX, `a`y);
		if (`v`pingY != 0)               m_world.`f`KeepAlive(`a`x,         `a`y + `v`pingY);
		if (`v`pingX != 0 && `v`pingY != 0) m_world.`f`KeepAlive(`a`x + `v`pingX, `a`y + `v`pingY);
 
		if (   m_chunk->`f`InBounds(`a`x, `a`y)
		    && m_chunk->`f`InBounds(`a`xto, `a`yto))
		{
			return m_chunk->`f`MoveCell(m_chunk, `a`x, `a`y, `a`xto, `a`yto);
		}
 
		return m_world.`f`MoveCell(`a`x, `a`y, `a`xto, `a`yto);
	}
~~~

Now finally, let’s look at what we got.

![iframe-youtube-video](https://www.youtube.com/embed/MfZopu-o6b4?rel=0 "Fixed Dirty Rect But Full Screen Is Slow")

That’s a considerable speed up! These optimizations won’t have much effect if the whole screen if full of moving cells though, we’ll need to look to threading to alleviate that.

This made it sound easy, but in reality, it took me a while to stamp out all the bugs. If you’re following along, before we get into threading, make sure this works 100% because it’s going to be impossible to debug without disabling the threading part.

## Threading

Now we can get to the fun part, threading it all together. Multi-threading is tough because if you’re not careful, race conditions can sneak in unexpectedly. Instead of a normal logic error that will cause a consistent problem, you could get random crashes. This makes these types of bugs hard to find if you’re not sure where to look. Because of this, it’s best to keep the threading code as concise as possible. Luckily for us this code is quite small, and not very interconnected, so it shouldn’t be too bad.

Currently, we update each chunk one-by-one, but chunks are mostly independent from one another. This makes them perfect candidates for thread pooling!

The idea of a thread pool is to queue up a series of tasks and execute as many at a time as there are threads in the pool. In my code, I’ve got a thread pool variable named Task. You can checkout a simple implementation of one [here](https://github.com/progschj/ThreadPool/blob/9a42ec1329f259a5f4881a291db1dcb8f2ad9040/ThreadPool.h)

Let’s edit the Update function to use this thread pool.

~~~SomeClass.h cpp
for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
	`w`Task->`f`queue([&, `v`chunk]() {
		`t`SimpleSandWorker(m_world, `v`chunk).`f`UpdateChunk();
	});
}
~~~

And we’re done, let’s see a demo!

![iframe-youtube-video](https://www.youtube.com/embed/OXop-HK18So?rel=0 "Threading Crash")

Well if only it was that simple, right?

There are many issues with this code, if we look at the execution line by line, notice that the current thread only pushes tasks onto the queue, leaving the chunk updates to finish sometime in the future. Before that can happen, we start calling CommitCells. This causes race conditions all over the place, and an inevitable crash.

To fix this we need a way to wait for all the chunks to finish. C++ provides the std:: condition_variable class, which we can use to pause a thread until a condition is met, and the std::mutex class which allows us to mark critical sections for the OS to guard. Only one thread can run critical sections protected by a specific mutex at a time which allows us to safely edit shared variables in different threads.

To make these changes we’ll need three variables: one condition variable, one mutex, and a count of chunks to update. After updating the chunk, we’ll lock and decrement the count. We’ll use a std::unique_lock and pass it the mutex. This locks the mutex until it pops off the stack, so we can use a scope and make it a one-liner. After we get the correct count, let’s tie it all together with a condition variable. These act like messengers between threads; we can send notifications to a waiting thread by calling notify_one. Calling wait, blocks the thread until it receives a notification. Once it does, and the condition is met, it continues onwards with the mutex locked.

~~~SomeClass.h cpp
		std::mutex `v`mutex;
		std::condition_variable `v`cond;
		int `v`chunkCount = m_world.m_chunks.size();
 
		for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
			`w`Task->`f`queue([&, `v`chunk]() {
				`t`SimpleSandWorker(m_world, `v`chunk).`f`UpdateChunk();
 
				{ std::unique_lock `v`lock(`v`mutex); `v`chunkCount--; }
				`v`cond.`f`notify_one();
			});
		}
 
		{
			std::unique_lock `v`lock(`v`mutex);
			`v`cond.`f`wait(`v`lock, [&]() { return `v`chunkCount == 0; });
		}
~~~

We can also multithread the CommitCells function in much the same way. Before we do that, to keep the code clean, I am going to throw this loop into a lambda called doForAllChunks. Then we can make two calls to it, one for the updating and the other for the commitment.

~~~SomeClass.h cpp
	void `f`Update() {
		// Draw cells with mouse
		// Paste tiles
 
		// Update cells
 
		m_world.`f`RemoveEmptyChunks();
 
		std::mutex `v`mutex;
		std::condition_variable `v`cond;
 
		auto `v`doForAllChunks = [&](std::function<void(`t`SandChunk*)> `a`func) {
			int `v`chunkCount = m_world.m_chunks.`f`size();
		
			for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
				`w`Task->`f`queue([&, `v`chunk]() {
					`a`func(`v`chunk);
 
					{ std::unique_lock `v`lock(`v`mutex); `v`chunkCount--; }
					`v`cond.`f`notify_one();
				});
			}
 
			std::unique_lock `v`lock(`v`mutex);
			`v`cond.`f`wait(`v`lock, [&]() { return `v`chunkCount == 0; });
		};
 
		`v`doForAllChunks([&](`t`SandChunk* `a`chunk) {
			`t`SimpleSandWorker(m_world, `a`chunk).`f`UpdateChunk();
		});
 
		`v`doForAllChunks([&](`t`SandChunk* `a`chunk) {
			`a`chunk->`f`CommitCells();
		});
 
		for (`t`SandChunk* `v`chunk : m_world.m_chunks) {
			`v`chunk->`f`UpdateRect();
		}
 
		// Copy sand colors to a texture
		// Draw the texture on the screen
		// Remove tiles
	}
~~~

Let’s see what happens when we run it now.

![iframe-youtube-video](https://www.youtube.com/embed/gOAnfB8ylGg?rel=0 "Stable but then crash")

It seems stable, but eventually it crashes. Why could this be? Well we didn’t account for the different threads calling back to the world and into other chunks. Those other chunks could be getting updated at the same time, creating more race conditions.

We need to consider who could be calling what functions in the SandChunk and SandWorld, and make sure to guard the ones that multiple threads could call at the same time.

Let’s start with the functions in the SandChunk. Multiple threads could collide inside of SetCell, MoveCell, and KeepAlive, so we’ll need three mutexes.

~~~SandChunk.h cpp
private:
	std::mutex m_filledCellCountMutex;
	std::mutex m_changesMutex;
	std::mutex m_workingRectMutex;
~~~

In SetCell, we only need to guard the filled cell count because no two cells in the array will get written/read at the same time. This is guaranteed by the way that CommitCells works, and we won’t be drawing with the mouse during the update.

~~~SandChunk.h cpp
	void `f`SetCell(size_t `a`index, const `t`Cell& `a`cell)
	{
		`t`Cell& `v`dest = m_cells[`a`index];
 
		if (   `v`dest.Type == `t`CellType::`d`EMPTY
			&& `a`cell.Type != `t`CellType::`d`EMPTY)  // Filling a cell
		{
			std::unique_lock `v`lock(m_filledCellCountMutex);
			m_filledCellCount++;
		}
 
		else 
		if (   `v`dest.Type != `t`CellType::`d`EMPTY
			&& `a`cell.Type == `t`CellType::`d`EMPTY) // Removing a filled cell
		{
			std::unique_lock `v`lock(m_filledCellCountMutex);
			m_filledCellCount--;
		}
 
		`v`dest = cell;
 
		`f`KeepAlive(`a`index);
	}
~~~

In MoveCell, we need to lock the whole list unfortunately, but this should only be in conflict when a chunk tries to move a particle into a neighboring chunk, which is a low percentage of the moves.

~~~SandChunk.h cpp
	void `f`MoveCell(`t`SandChunk* `a`source, int `a`x, int `a`y, int `a`xto, int `a`yto)
	{
		size_t `v`src = source->`f`GetIndex(`a`x, `a`y);
		size_t `v`dst = `f`GetIndex(`a`xto, `a`yto);
 
		std::unique_lock `v`lock(m_changesMutex);
 
		m_changes.`f`emplace_back(`a`source, `v`src, `v`dst);
	}
~~~

Finally, we need to also lock the KeepAlive function.

~~~SandChunk.h cpp
	void KeepAlive(size_t `a`index) {
		int `v`x = `a`index % m_width;
		int `v`y = `a`index / m_width;
 
		std::unique_lock `v`lock(m_workingRectMutex);
 
		m_minXw = `f`clamp(`f`min(`v`x - 2, m_minXw), 0, m_width);
		m_minYw = `f`clamp(`f`min(`v`y - 2, m_minYw), 0, m_height);
		m_maxXw = `f`clamp(`f`max(`v`x + 2, m_maxXw), 0, m_width);
		m_maxYw = `f`clamp(`f`max(`v`y + 2, m_maxYw), 0, m_height);
	}
~~~

In the SandWorld we could use two mutexes to guard the list and map but guarding the whole map every time it needs to be accessed will cripple the multithreaded performance. To get around this we can use a concurrent map, I saw that Microsoft provides a concurrent_unordered_map, so I just replaced the current map with it. Basically, this locks the buckets instead of the whole container, so more threads can key into it at once. We need to lock the list though, but we never use it for access besides iteration, so we only need to lock when inserting into it as multiple threads could be creating chunks at the same time.

~~~SandWorld.h cpp
#include `l`<concurrent_unordered_map.h>
 
private:
	`w`Concurrency::`t`concurrent_unordered_map<std::pair<int, int>, `t`SandChunk*, `t`pair_hash> m_chunkLookup;
	std::mutex m_chunkMutex;
 
private:
	`t`SandChunk* `f`CreateChunk(std::pair<int, int> `a`location) {
		auto [`v`lx, `v`ly] = `a`location;
 
		if (   `v`lx < -50 || `v`ly < -50
			|| `v`lx >  50 || `v`ly >  50) // could pass in a world limit to constructor
		{
			return nullptr;
		}
 
		`t`SandChunk* `v`chunk = new `t`SandChunk(m_chunkWidth, m_chunkHeight, lx, ly);
 
		m_chunkLookup.`f`insert({ `a`location, `v`chunk });
 
		{
			std::unique_lock `v`lock(m_chunkMutex);
			m_chunks.`f`push_back(`v`chunk);
		}
 
		return `v`chunk;
	}
~~~

That should be all for multithreading! Let’s take a look at the performance.

![iframe-youtube-video](https://www.youtube.com/embed/0k4DKajj_ZM?rel=0 "Final Demo")

Look at that frame time! I think this is a good basis for a strong sand engine. Now I am going to try and build a game with it, so expect a few dev logs about that. I was hoping to make a game in a month but including engine dev time I’m already way past that, so we’ll pause the clocks and I’ll try and do some sort of weekly thing if I can, I think that’ll be interesting. I tried making that space game I was taking about, and it was actually pretty cool, but there wasn’t too much sand involved unfortunately, so I am going to try and repurpose the mechanics from it into something on the ground instead of in space.