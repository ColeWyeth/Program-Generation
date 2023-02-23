# Program-Generation

This project is designed to randomly generate (or sample)
algorithms to solve problems. The framework is general enough
to work in diverse simulated worlds, controlling agents
with a set of observations.
Interestingly, I wrote this code before I was familiar with Kolmogorov
complexity, and avoided the problem of nonhalting TMs by simply not
adding a looping construct to the generated language. Of course this
limits the expressiveness of generated algorithms.

The obvious challenge is the exploding number of possible
algorithms needed to solve complex problems.
My solution is to first generate a "seed" program which is sometimes
randomly successful, then attempt to fill in the random commands/tests.
The most successful approach is to run many iterations of this seed
and fill strategy.

Currently, code generation can be run against two games.

In the "grid" game, the agent rolls a ball to a goal square.
Run grid.py in the v2 directory to see the training process run
and the code generated.

In the "kill ogre" game, an avatar (Tanith Low) must be moved close to an enemy
and swing its sword (inspired by Derek Landy's Skulduggery Pleasant series).
Run killOgre.py in the v2 directory to see the training process run
and the code generated.
You may also watch an animation of a successful run or even play yourself.
This has pygame as a dependency.
