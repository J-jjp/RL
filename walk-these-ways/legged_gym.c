

Learning Multiple Gaits within Latent Space for Quadruped Robots

    Abstract— Learning multiple gaits is non-trivial for legged
    robots, especially when encountering different terrains and velocity commands. 
    In this work, we present an end-to-end training framework for learning multiple gaits for quadruped robots,
    tailored to the needs of robust locomotion, agile locomotion, and
    user’s commands. A latent space is constructed concurrently by
    a gait encoder and a gait generator, which helps the agent to
    reuse multiple gait skills to achieve adaptive gait behaviors.
    To learn natural behaviors for multiple gaits,
    we design gaitdependent rewards that are constructed explicitly from gait
    parameters and implicitly from conditional adversarial motion
    priors (CAMP). We demonstrate such multiple gaits control on
    a quadruped robot Go1 with only proprioceptive sensors.