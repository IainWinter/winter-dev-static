[title](Designing a physics engine)

By coincidence, right when The Cherno announced his game engine series I was just starting to get going on my own engine. I couldn't wait to finally have a professional opinion on how to make one. With self-taught programming it's hard to not doubt yourself constantly, wondering if you are doing things right or just think you are.

Recently, he has been posting videos about huge aspects of his engine like physics and entity systems, which were what I really wanted to learn about by making myself, but he ended up using libraries instead of going through the internals! I am not against using libraries, but to use them for the fun stuff? I felt like it defeated the point of making a custom engine series.

There is an argument to be made about saving time, but this was the first C++ project that I was making and the goal from the start was to go through all the major pillars of an engine: input, graphics, physics, entities, and audio. I wanted to learn how those things worked along with C++ and code design in general.

I bet that some other people are interested in the details of how these systems work, and I want to learn how to explain code better, so I am going to try and make some videos going over the internals of these systems. They end up being much simpler than at first glance.

[sub-title](Let's start with the physics engine...)

Physics engines are responsible for figuring out where each object in a scene is over time. Objects can collide with one another, then choose to respond in several ways. It's a generic problem that the user can configure at several different levels. Do they want a collider? Do they want to respond to collisions? Do they want to simulate dynamics? They could want dynamics, but not gravity. It's a problem that calls for good planning and robust design.

I looked at how bullet and box2d went about sorting their engines and concluded that the way bullet went about it was solid. I boiled it down to just what was needed, and based my design around that. There are already some great articles going over the hard math involved, so I am going to focus on the design aspect instead because I haven't seen anyone do that, and it's also a real headache.

At the current moment, this physics engine is not fully featured, but in future articles I plan to build it out further. This article will not cover rotation, multiple contact point collisions, or constrained simulation. I think it will work out for the best as it's easy to get overwhelmed, and I want to ease into those topics. With that out of the way, let's dive into the different parts of a physics engine.

The problem can be split into 2 or 3 pieces, dynamics, collision detection, and collision response. I'll start with dynamics because it is by far the simplest.

[sub-title](Dynamics)

Dynamics is all about calculating where the new positions of objects are based on their velocity and acceleration. In high school you learn about the four kinematic equations along with Newton's three laws which describe the motion of objects. We'll only be using the first and third kinematic equations, the others are more useful for analysis of situations, not simulation. That leaves us with:

[equation](v=v_0+at)
[equation](\Delta x=v_0t+\frac{1}{2}at^2)

We can give ourselves more control by using Newtons 2nd law, subbing out acceleration giving us:

[equation](v=v_0+\frac{F}{m}t)
[equation](x=x_0+vt)

Each object needs to store these three properties: velocity, mass, and net force. Here we find the first decision we can make towards the design, net force could either be a list or a single vector. In school you make force diagrams and sum up the forces, implying that we should store a list. This would make it so you could set a force, but you would need to remove it later which could get annoying for the user. If we think about it further, net force is really the total force applied in a single frame, so we can use a vector and clear it at the end of each update. This allows the user to apply a force by adding it, but removing it is automatic. This shortens our code and gives a performance bump because there is no summation of forces, it's a running total.

We'll use this struct to store the object info for now.

[code](Object.h, cpp,
struct `t`Object {
	vec3 `w`Position; // struct with 3 floats for x, y, z or i + j + k
	vec3 `w`Velocity;
	vec3 `w`Force;
	float `w`Mass;
};
)

We need a way to keep track of the objects we want to update. A classic approach is to have a physics world that has list of objects and a step function that loops over each one. Let's see how that might look; I'll omit header/cpp files for brevity.

[code](PhysicsWorld.h, cpp,
class `t`PhysicsWorld {
private:
	std::vector<Object*> m_objects;
	vec3 m_gravity = vec3(0, -9.81f, 0);
 
public:
	void AddObject   (Object* object) { /* ... */ }
	void RemoveObject(Object* object) { /* ... */ }
 
	void Step(
		float dt)
	{
		for (Object* obj : m_objects) {
			obj->Force += obj->Mass * m_gravity; // apply a force
 
			obj->Velocity += obj->Force / obj->Mass * dt;
			obj->Position += obj->Velocity * dt;
 
			obj->Force = vec3(0, 0, 0); // reset net force at the end
		}
	}
};
)

Note the use of pointers, this forces other systems to take care of the actual storing of objects, leaving the physics engine to worry about physics, not memory allocation.

With this you can simulate all sorts of stuff from objects flying through the sky to solar systems.

[iframe-youtube-video](https://www.youtube.com/embed/crKrkn-RIOU?rel=0)
[iframe-youtube-video](https://www.youtube.com/embed/sHZEs-oQTI4?rel=0)

You can do a lot with this, but it's the easy part to be honest, and that's not what you came for...

[sub-title](Collision detection)

Collision detection is more involved, but we can lighten the load by using some clever tricks. Let's think about what needs to be found first. If we look at some examples of objects colliding, we notice that in most cases there is a point on each shape that is furthest inside the other.

[svg-half](./content/embed/physics-sphere-plane.svg)
[br]()
[svg-half](./content/embed/physics-sphere-sphere.svg)

For simple cases, it turns out to be all we need to respond to a collision. From those two points we can find the normal, and how deep the objects are inside one another. This is huge because it means that we can abstract the idea of different shapes away, and only worry about the points in the response.

Let's jump into the code, we'll need some helper structs that I'll note first.

[code](Transform.h, cpp,
struct `t`CollisionPoints {
	vec3 `w`A; // Furthest point of A into B
	vec3 `w`B; // Furthest point of B into A
	vec3 `w`Normal; // B – A normalized
	float `w`Depth;    // Length of B – A
	bool `w`HasCollision;
};
 
struct `t`Transform { // Describes an objects location
	vec3 `w`Position;
	vec3 `w`Scale;
	quat `w`Rotation;
};
)

When I originally wrote this article, I used a technique called double dispatch to call the collision algorithms, but as time when on I grew annoyed with this pattern. It led to a large number of duplicate functions which were just single lines calling other functions. It was very hard to follow and did a poor job solving the issue of locality, which is why I used it in the first place.

Instead, let’s steal some good ideas from Valve, specifically a table on page 33 of this [link](pdf, ~/articles/physics-engine/DirkGregorius_Contacts.pdf). We can use functions pointers and enums to centralize the dispatching to the collision algorithms, and at the same time get a well defined table of which interactions our engine supports. 

Each shape will have a different type of collider to hold its properties and a base to allow them to be stored. 

[code](Colliders.h, cpp,
enum `t`ColliderType {
	`d`SPHERE,
	`d`PLANE
};

struct `t`Collider {
	`t`ColliderType `w`Type;
};

struct `t`SphereCollider : `t`Collider {
	vec3 `w`Center;
	float `w`Radius;
};

struct `t`PlaneCollider : `t`Collider {
	vec3 `w`Normal;
	float `w`Distance;
};
)

Then we can stub out the different interactions we will support. I will include a Sphere vs Sphere and Sphere vs Plane test. I won’t go into the math behind these in this article, but you can find the code [link](here, https://github.com/IainWinter/IwEngine/blob/3e2052855fea85718b7a499a7b1a3befd49d812b/IwEngine/include/iw/physics/impl/TestCollision.h#L25). 

[code](TestCollision.h, cpp,
`t`CollisionPoints `f`Test_Sphere_Sphere(
	const `t`Collider* a, const `t`Transform* ta,
	const `t`Collider* b, const `t`Transform* tb);

`t`CollisionPoints `f`Test_Sphere_Plane(
	const `t`Collider* a, const `t`Transform* ta,
	const `t`Collider* b, const `t`Transform* tb);
)

Note that using this design we lose the benefit of type safety that double dispatch provided, but that is a small price to pay for now simple this design is to understand and extend.

Now that we have our test functions, we can put them into a table. Let's typedef the function signatures and make a table in a function called TestCollision.

[code](TestCollision.h, cpp,
using `t`FindContactFunc = `t`CollisionPoints(*)(
		const `t`Collider*, const `t`Transform*, 
		const `t`Collider*, const `t`Transform*);

`t`CollisionPoints `f`TestCollision(
	const `t`Collider* `a`a, const `t`Transform* `a`at, 
	const `t`Collider* `a`b, const `t`Transform* `a`bt)
{
	static const `t`FindContactFunc `v`tests[2][2] = 
	{
		// Sphere             Plane
		{ `f`Test_Sphere_Sphere, `f`Test_Sphere_Plane }, // Sphere
		{ nullptr,            nullptr           }  // Plane
	};
)

To call the correct function, we need to do a little dance because we could have passed the colliders in any order. To do this let's sort by the Collider Type enum.

[code](TestCollision.h_, cpp,
	// If we are passed a Plane vs Sphere, swap the 
	// colliders so it's a Sphere vs Plane
	bool `v`swap = `a`b->`w`Type > `a`a->`w`Type;

	if (`v`swap)
	{
		std::`f`swap(`a`a, `a`b);
		std::`f`swap(`a`at, `a`bt);
	}
)

Now we can dispatch to the function stored in our table, and return the points.

[code](TestCollision.h_, cpp,
	// now we can dispatch the correct function
	`t`CollisionPoints `v`points = `v`tests[`a`a->`w`Type][`a`b->`w`Type](`a`a, `a`at, `a`b, `a`bt);

	// if we swapped the order of the colliders, to keep the
	// results consistent, we need to swap the points
	if (`v`swap)
	{
		std::`f`swap(`v`points.`w`A, `v`points.`w`B);
		`v`points.`w`Normal = -`v`points.`w`Normal;
	}

	return `v`points;
)

You can use these colliders on their own, but most likely want to attach one to an object. We'll replace Position with a Transform in the Object. We are still only using position in the dynamics but can use scale and rotation in the collision detection. There is a tricky decision to make here. I'm going to use a Transform pointer for now, but we'll come back to this at the end and see why that might not be the best choice.

[code](Object.h, cpp,
struct `t`Object {
	float `w`Mass;
	vec3 `w`Velocity;
	vec3 `w`Force;
 
	`t`Collider* `w`Collider;
	`t`Transform* `w`Transform;
};
)

A good design practice is to separate all the different aspects of complex functions like Step into their own. This makes the code much more readable, so let's add another function named ResolveCollisions in the physics world.

First, another helper struct...

[code](Collision.h, cpp,
struct `t`Collision {
	`t`Object* `w`ObjA;
	`t`Object* `w`ObjB;
	`t`CollisionPoints `w`Points;
};
)

Again, we have the physics world, I'll compact the parts we have already looked at but it's nice to have context.

[code](PhysicsWorld.h, cpp,
class `t`PhysicsWorld {
private:
	std::vector<`t`Object*> m_objects;
	vec3 m_gravity = vec3(0, -9.81f, 0);
 
public:
	void `f`AddObject   (`t`Object* object);
	void `f`RemoveObject(`t`Object* object);
 
	void `f`Step(float `a`dt)
	{
		`f`ResolveCollisions(`a`dt);
 
		for (`t`Object* `v`obj : m_objects) { /* ... */ }
	}
 
	void `f`ResolveCollisions(float `a`dt)
	{
		std::vector<`t`Collision> `v`collisions;

		for (`t`Object* `v`a : m_objects)
		for (`t`Object* `v`b : m_objects) 
		{
			if (`v`a == `v`b)
				break;

			if (!`v`a->`w`Collider || !`v`b->`w`Collider)
				continue;

			`t`CollisionPoints `v`points = `f`TestCollision(
				`v`a->`w`Collider, `v`a->`w`Transform,
				`v`b->`w`Collider, `v`b->`w`Transform
			);

			if (`v`points.`w`HasCollision)
				`v`collisions.`f`emplace_back(`v`a, `v`b, `v`points);
		}
 
		// Solve collisions
	}
};
)

This is looking good. Because of the way we constructed TestCollision, we don't need to know anything about the colliders, and using a break in the for loop gives us the unique pairs, so we never check the same objects twice.

Now that we have detected a collision, we need some way to react to it.

[sub-title](Collision Response)

Now that we have abstracted away the idea of different shapes into points, the collision response is almost pure math. The design is relatively simple compared to what we just went through; we'll start with the idea of a solver. A solver is used to *solve* things about the physics world. That could be the impulse from a collision or raw position correction, really anything you choose to implement.

Let's start with an interface.

[code](Solver.h, cpp,
class `t`Solver {
public:
	virtual void `f`Solve(std::vector<`t`Collision>& `a`collisions, float `a`dt) = 0;
};
)

We'll need another list in the physics world to store these, and functions to add and remove them. After we generate our list of collisions, we can feed it to each solver.

[code](PhysicsWorld.h, cpp,
class `t`PhysicsWorld {
private:
	std::vector<`t`Object*> m_objects;
	std::vector<`t`Solver*> m_solvers;
	vec3 m_gravity = vec3(0, -9.81f, 0);
 
public:
	void `f`AddObject   (`t`Object* `a`object);
	void `f`RemoveObject(`t`Object* `a`object);
 
	void `f`AddSolver   (`t`Solver* `a`solver);
	void `f`RemoveSolver(`t`Solver* `a`solver);
 
	void `f`Step(float `a`dt);
 
	void `f`ResolveCollisions(float `a`dt)
	{
		std::vector<`t`Collision> `v`collisions;
		for (`t`Object* `v`a : m_objects) { /* ... */ }
 
		for (`t`Solver* `v`solver : m_solvers) {
			`v`solver->`f`Solve(`v`collisions, `a`dt);
		}
	}
};
)

In the last section the meat was in the design, this one leans much more towards what kinds of solvers you implement. I've made an impulse & position solver myself that seem to work for most situations. To keep this short, I won't cover the math here, but you can check out the source for the impulse solver [link](here, https://github.com/IainWinter/IwEngine/blob/3e2052855fea85718b7a499a7b1a3befd49d812b/IwEngine/src/physics/Dynamics/ImpulseSolver.cpp), and the position solver [link](here, https://github.com/IainWinter/IwEngine/blob/3e2052855fea85718b7a499a7b1a3befd49d812b/IwEngine/src/physics/Dynamics/SmoothPositionSolver.cpp) if you are interested.

Let's see a demo!

[iframe-youtube-video](https://www.youtube.com/embed/Q_KAqCmEgyA?rel=0)

[sub-title](More Options)

The real power of a physics engines comes from the options that you give to the user. In this example there aren't too many that can be changed, but we can start to think about the different options we want to add. In most games you want a mix of objects, some that simulate dynamics, and others that are static obstacles. There is also a need for triggers, objects that don't go through the collision response, but fire off events for exterior systems to react to, like an end of level flag. Let's go through some minor edits we can make to allow these settings to be easily configured.

The biggest change we can make is to distinguish between objects that simulate dynamics and ones that don't. Because of how many more settings a dynamic object needs, let's separate those out from what is necessary for collision detection. We can split Object into CollisionObject and Rigidbody structs. We'll make Rigidbody inherit from CollisionObject to reuse the collider properties and allow us to store both types easily.

We are left with these two structs. A dynamic_cast could be used to figure out if a CollisionObject is really a Rigidbody, but will make code slightly longer, so I like to add a boolean flag even through it's not considered best practice. We can also add a flag for the object to act as a trigger and a function for a callback. While we're at it, let's beef up the security by protecting the raw values.

[code](CollisionObject.h, cpp,
struct `t`CollisionObject {
protected:
	`t`Transform* m_transform;
	`t`Collider* m_collider;
	bool m_isTrigger;
	bool m_isDynamic;
 
	std::function<void(`t`Collision&, float)> m_onCollision;
 
public:
	// getters & setters, no setter for isDynamic
};
)

We can add many more settings to the Rigidbody. It's useful if each object has its own gravity, friction, and bounciness. This opens the door to all sorts of physics based effects. In a game you could have an ability that changes the gravity in an area for a time. You could have some objects be bouncy and other like weight balls. A floor could be made of ice and be slippy for a harder challenge.

[code](Rigidbody.h, cpp,
struct `t`Rigidbody : `t`CollisionObject
{
private:
	vec3 m_gravity;  // Gravitational acceleration
	vec3 m_force;    // Net force
	vec3 m_velocity;
 
	float m_mass;
	bool m_takesGravity; // If the rigidbody will take gravity from the world.
 
	float m_staticFriction;  // Static friction coefficient
	float m_dynamicFriction; // Dynamic friction coefficient
	float m_restitution;     // Elasticity of collisions (bounciness)
 
public:
	// getters & setters
};
)

Let's split the PhysicsWorld into a CollisionWorld and a DynamicsWorld as well. We can move the Step function into the DynamicsWorld, and ResolveCollisions into the CollisionWorld. This saves someone who doesn't want dynamics from sifting through functions that are useless to them.

We can make some edits to ResolveCollisions function to give triggers their correct functionality. Let's split the function into its parts to keep it readable. Adding a callback to the world can be useful too if you want program wide events.

[code](CollisionWorld.h, cpp,
class `t`CollisionWorld {
protected:
	std::vector<`t`CollisionObject*> m_objects;
	std::vector<`t`Solver*> m_solvers;
 
	std::function<void(`t`Collision&, float)> m_onCollision;
 
public:
	void `f`AddCollisionObject   (`t`CollisionObject* `a`object);
	void `f`RemoveCollisionObject(`t`CollisionObject* `a`object);
 
	void `f`AddSolver   (`t`Solver* `a`solver);
	void `f`RemoveSolver(`t`Solver* `a`solver);
 
	void `f`SetCollisionCallback(std::function<void(`t`Collision&, float)>& `a`callback);
 
	void `f`SolveCollisions(std::vector<`t`Collision>& `a`collisions, float `a`dt)
	{
		for (`t`Solver* `v`solver : m_solvers) {
			`v`solver->`f`Solve(`a`collisions, `a`dt);
		}
	}
 
	void `f`SendCollisionCallbacks(std::vector<`t`Collision>& `a`collisions, float `a`dt)
	{
		for (`t`Collision& `v`collision : `a`collisions) {
			m_onCollision(`v`collision, `a`dt);
 
			auto& `v`a = `v`collision.`w`ObjA->`f`OnCollision();
			auto& `v`b = `v`collision.`w`ObjB->`f`OnCollision();
 
			if (`v`a) `v`a(`v`collision, `a`dt);
			if (`v`b) `v`b(`v`collision, `a`dt);
		}
	}
 
	void `f`ResolveCollisions(float `a`dt)
	{
		std::vector<`t`Collision> `v`collisions;
		std::vector<`t`Collision> `v`triggers;
		
		for (`t`CollisionObject* `v`a : m_objects)
		for (`t`CollisionObject* `v`b : m_objects)
		{
			if (`v`a == `v`b)
				break;

			if (!`v`a->`f`Col() || !`v`b->`f`Col())
				continue;

			`t`CollisionPoints `v`points = `f`TestCollision(
				`v`a->`w`Collider, `v`a->`w`Transform,
				`v`b->`w`Collider, `v`b->`w`Transform
			);

			if (`v`points.`w`HasCollision)
			{
				if (`v`a->`f`IsTrigger() || `v`b->`f`IsTrigger())
					`v`triggers.`f`emplace_back(`v`a, `v`b, `v`points);
				else
					`v`collisions.`f`emplace_back(`v`a, `v`b, `v`points);
			}
		}
 
		`f`SolveCollisions(`v`collisions, `a`dt); // Don't solve triggers
 
		`f`SendCollisionCallbacks(`v`collisions, `a`dt);
		`f`SendCollisionCallbacks(`v`triggers, `a`dt);
	}
};
)

To keep the Step function readable, let's split it up into pieces as well.

[code](DynamicWorld.h, cpp,
class `t`DynamicsWorld : public `t`CollisionWorld
{
private:
	vec3 m_gravity = vec3(0, -9.81f, 0);
 
public:
	void `f`AddRigidbody(`t`Rigidbody* `v`rigidbody)
	{
		if (`v`rigidbody->`f`TakesGravity()) {
			`v`rigidbody->`f`SetGravity(m_gravity);
		}
 
		`f`AddCollisionObject(`v`rigidbody);
	}
 
	void `f`ApplyGravity() {
		for (`t`CollisionObject* `v`object : m_objects) {
			if (!`v`object->`f`IsDynamic())
				continue;
 
			`t`Rigidbody* `v`rigidbody = (`t`Rigidbody*)`v`object;
			`v`rigidbody->`f`ApplyForce(`v`rigidbody->`f`Gravity() * `v`rigidbody->`f`Mass());
		}
	}
 
	void `f`MoveObjects(float `a`dt)
	{
		for (`t`CollisionObject* `v`object : m_objects) {
			if (!`v`object->`f`IsDynamic())
				continue;
 
			`t`Rigidbody* `v`rigidbody = (`t`Rigidbody*)`v`object;
 
			vec3 `v`vel = `v`rigidbody->`f`Velocity()
				    + `v`rigidbody->`f`Force() / `v`rigidbody->`f`Mass()
				    * `a`dt;
 
			`v`rigidbody->SetVelocity(`v`vel);

			vec3 `v`pos = `v`rigidbody->`f`Position()
				    + `v`rigidbody->`f`Velocity()
				    * `a`dt;
 
			`v`rigidbody->`f`SetPosition(`a`pos);
 
			`v`rigidbody->`f`SetForce(vec3(0, 0, 0));
		}
	}
 
	void `f`Step(float `a`dt)
	{
		`f`ApplyGravity();
		`f`ResolveCollisions(`a`dt);
		`f`MoveObjects(`a`dt);
	}
};
)

Now we have a whole stack of options that the user can configure for many different scenarios with a simple yet powerful API.

There is one more option that I want to cover. The physics world has no need updating every frame. Say a game like CS:GO gets rendered at 300 fps. It's not checking the physics every frame; it might run at 50 Hz instead. If the game only used the positions from the physics engine, objects would have .02 seconds between each update, causing a jittery look. And that's an ideal rate, some games will only update at 20 Hz leaving .05 seconds between update!

[iframe-youtube-video](https://www.youtube.com/embed/_-cXkPp-aYw?rel=0)

To get around this, it is common to split the physics world from the rendered world. This is simply done by using a raw Transform instead of a pointer and having a system outside the physics interpolate the position every frame. Let's see how we might implement this.

First, we'll get rid of that pointer. We'll need to add a last transform as well which will gets set just before the update in MoveObjects.

[code](CollisionObject.h, cpp,
struct `t`CollisionObject {
protected:
	`t`Transform m_transform;
	`t`Transform m_lastTransform;
	`t`Collider* m_collider;
	bool m_isTrigger;
	bool m_isStatic;
	bool m_isDynamic;
 
	std::function<void(`t`Collision&, float)> m_onCollision;
public:
	// Getters & setters for everything, no setter for isDynamic
};
)

Because we used getters and setters, this won't break any code outside the CollisionObject. We can make an exterior system that keeps track of how far it is into the physics update and use a linear interpolation between the last and current position. I'm not going to go into where to put this system, but it should update every frame rather than every physics update.

[code](PhysicsSmoothStep.h, cpp,
class `t`PhysicsSmoothStepSystem {
private:
	float m_accumulator = 0.0f;
 
public:
	void `f`Update() {
		for (`t`Entity `v`entity : `f`GetAllPhysicsEntities()) {
			`t`Transform*       `v`transform = `v`entity.`f`Get<`t`Transform>();
			`t`CollisionObject* `v`object    = `v`entity.`f`Get<`t`CollisionObject>();
 
			`t`Transform& `v`last    = `v`object->`f`LastTransform();
			`t`Transform& `v`current = `v`object->`f`Transform();
 
			`v`transform->Position = `f`lerpf(
				`v`last.Position,
				`v`current.Position,
				m_accumulator / `f`PhysicsUpdateRate()
			);
		}
 
		m_accumulator += `f`FrameDeltaTime();
	}
 
	void `f`PhysicsUpdate() {
		m_accumulator = 0.0f;
	}
};
)

This system smoothy moves the objects between their positions in the physics engines every frame, removing all jittery artifacts from the movement.

[iframe-youtube-video](https://www.youtube.com/embed/0xJ-oRCPRk8?rel=0)

And that's the final result. I hope you can use the principles from this article to get a better idea of how to lay out complex systems in nimble ways, or even make your own engine. There is a lot more to cover, but I'll leave it to a part 2 because this is getting long. Let me know what you thought, should I keep focusing on design, or dive deeper into the math behind the implementations?

Thanks for reading, I hope to catch you next time!