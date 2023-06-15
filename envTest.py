from snakeEnvironment import SnakeEnvironment

env = SnakeEnvironment()

for episode in range(50):

    state = env.reset()
    for timestep in range(100):
        env.render()
        action = env.get_sample_action()  # take a random action
        state, reward, done = env.step(action)

        if done:
            break    
