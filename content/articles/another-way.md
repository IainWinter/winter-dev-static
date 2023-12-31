[title](Another way of programming, taking it slow)

Whenever I sit down to write some code, I always get an itch to finish whatever problem is staring me in the face right at that moment. Over the last 2 years, I've realized that if you can afford to tackle a problem over a long period of time, you should absolutely go for that option.

There are major benefits that arise from this approach. The final code ends up more developed than what you would have been capable of writing at the beginning. You end up spending less time on the actual problem, because you only work on it when you have a good idea. And, after sitting with it for so long there's a good chance that even if not fully correct, it will still move you in the right direction. Taking it slow leads to an aha moment in the future along with the insight required to solve the problem.

I was inspired to write this article from an extreme example in my own code around making a prefab class for my entity system. When I first wrote the class, I had the intention to create it right then and there, but quickly realized I didn't have the knowledge to do so. It required doing type specific operations on generic pointers, with no types!

[sub-title](A quick overview of an entity system & the root of the problem)

Entities are made from sets of components. Components are made up of data. Ideally, they would be Plain Old Data classes, but more complex components that store data in dynamic memory are eventually required. This could be in the form of lists, maps, or things like shared pointers.

When copying a class in C++ we make use of the copy constructor, which takes care of these special cases by calling the copy constructors of the underlying containers, resulting in a deep copy.

Prefabs need to store a list of components and their respected data to spawn an entity in the future. The only way to store multiple types in a single list is to use generic void pointers. There is a fundamental problem that comes up frequently when using this practice; because of the use of voids, we dropped all knowledge of what type of data we are pointing to. When it comes time to spawn the entity, each component's data needs to be copied into the entity system, but without type information there is no way to know which copy constructor to call, so we can't make deep copies.

[sub-title](The process)

I took the first stab at my prefab class in February, but only completed it a couple days ago in June! This was a non-critical, time saver class, so I could afford not to worry about it for several months while working on other stuff. I'm glad I waited though because it opened my mind to this new way of thinking.

I made the first real attempt in early June but was stopped yet again by a lack of type information. The prefab needed to store void*s in a list and copy them into other void*s in the entity system. The simplest way to do this is with a memcpy which works great for POD classes, but when a component requires a deep copy, it will miss most of the real data. Components that make use of containers or inheritance don't get copied correctly because most of the data is behind pointers.

I got stuck at this point because it seemed impossible to get type information back from the void*s. I knew I was really close to having the solution, I just needed a way to deep copy void*s, but I couldn't think of any way of doing that, so I put it on pause again.

Cut to 3 weeks later; I was working on a bug in the physics engine where lambdas were not getting copied correctly and finally had that aha moment. Forget about copying lambdas, what if I could use lambdas to do the copying? In the entity system there is a Component class that stores metadata like the name and size. I could just add a lambda to it that would call the correct copy constructor. A lambda with a completely generic signature could get created in a template function and called whenever a component needs to get copied.

This solution requires that at some point you use a template function in the entity system. That's a fair price when the alternatives would require the user to create at least one more function for each component, or add to some list, etc. I love solutions that are completely behind the scenes. Why should the user need to worry about things this low level if all they are trying to do is spawn entities?

Here is the code that creates the lambda. When you register a component, it calls GetCopyFunc and gets the lambda that copies for that component type. This seems like a powerful concept that I want to explore further, the idea that you can call a template function once and store information from it in generic types, making it so there is no need to template further. You can see my attempt at this in the entity system in my engine.

[code](TypeErasureCopy.h, cpp,
using `t`func_DeepCopy = std::function<void(void*, void*)>;

struct `t`Component {
	...
	`t`func_DeepCopy `w`DeepCopyFunc;
	...
};

template<typename `t`_t>
`t`func_DeepCopy `f`GetCopyFunc() {
	return [](void* `a`ptr, void* `a`data) 
	{
		`t`_t* `v`p = (`t`_t*)`a`ptr;
		`t`_t* `v`d = (`t`_t*)`a`data;

		*`v`p = *`v`d; // call copy constructor
	};
}
)

Even though this prefab system took 5 months, I only spent around an hour or so on it. I think that the result is much better than anything that I could have written months ago. Because I had to live without a prefab system for so long, I got a good idea for what it really needed to do, instead of wanting a prefab system because it's cool and guessing at the use cases. I also avoided doing any research apart from a single google search for how to make that lambda above that landed me at [link](stackoverflow, https://stackoverflow.com/a/40293164/6772365), which shows some other constructors.

I think that this style of coding is very powerful, and I want to try and use it in other places in my code more frequently. It seems hard to do though because you need something to work at some point, so I guess I'll leave it to future aha'ed me to see if it works...