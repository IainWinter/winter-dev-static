---
title: Mesh generation
data: October 6, 2020
published: false
---

# Mesh generation

![](/prims.png "Chunks Everywhere & Empty Chunks")

This post is less about some specific information and more about something I've been cooking up over at winter.dev/prims.

When working in 3D everything is made out of meshes. In their simplest form these are big lists of positions that get fed into the GPU for rendering. These lists can be generated or loaded from disk. Most games save a large amount of data in models that make up generic objects like rocks and trees. These typically are generated but then get baked into a game's download and can never change.

Instead, imagine if in an engine you only had to define the bounds of objects and their types, then the engine generated them when needed. I think this would make rouge likes and single player games look more interesting many playthroughs in because the repeating rooms could use differently generated base assets.

That is an end goal for what it's worth...

Right now, to start with something I've compiled an incomplete list of the generation algorithms that I've needed. This only consists of primitive shapes for now, but I think it will still prove useful because every time I need another shape I spend a long time searching on forms but only end up with bits and pieces. To try and help alleviate the pain of making these in the future, I've cleaned up some popular algorithms and added comments that clear up the oddities within them.

Let me know if you have any suggestions, there are more shapes that I want to add but I also want to open it up for people to add their own algorithms. Then expand into more complex meshes, like a rock generator or foliage generation.