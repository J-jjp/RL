


Figure 1: Multiplicity of Behavior (MoB) enables a human to tune a single quadruped policy trained
on flat ground to diverse unseen environments. Top row: A low-frequency gait fails to sprint on
slippery terrain (Gait 2; inset) but tuning it to high frequency results in success (Gait 1). However,
a low frequency and high footswing height are necessary for stair traversal (Gait 2; middle image).
A low footswing and wide stance (Gait 3) makes the robot robust to leg shoves, but Gait 1, which
succeeded at sprinting, fails. Tuning gait thus aids in generalizing to different tasks. Bottom row:
Examples of other behaviors enabled by our controller.
Abstract: Learned locomotion policies can rapidly adapt to diverse environments
similar to those experienced during training but lack a mechanism for fast tuning when they fail in an out-of-distribution test environment. This necessitates
a slow and iterative cycle of reward and environment redesign to achieve good
performance on a new task. As an alternative, we propose learning a single policy that encodes a structured family of locomotion strategies that solve training
tasks in different ways, resulting in Multiplicity of Behavior (MoB). Different
strategies generalize differently and can be chosen in real-time for new tasks or
environments, bypassing the need for time-consuming retraining. We release a
fast, robust open-source MoB locomotion controller, Walk These Ways, that can
execute diverse gaits with variable footswing, posture, and speed, unlocking diverse downstream tasks: crouching, hopping, high-speed running, stair traversal, bracing against shoves, rhythmic dance, and more. Video and code release:
https://gmargo11.github.io/walk-these-ways/
Keywords: Locomotion, Reinforcement Learning, Task Specification