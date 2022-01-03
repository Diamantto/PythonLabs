import numpy as np
import pandas as pd
import random

rewards = np.array([
    [-100, -1, -100, -100, -100, -100, -100, -100, -100, 100],
    [-1, -100, -1, -100, -100, -100, -100, -100, -100, -100],
    [-100, -1, -100, -100, -100, -1, -100, -100, -100, -100],
    [-100, -100, -100, -100, -1, -100, -1, -100, -100, -100],
    [-100, -100, -100, -1, -100, -1, -100, -100, -100, -100],
    [-100, -100, -1, -100, -1, -100, -100, -100, -1, -100],
    [-100, -100, -100, -1, -100, -100, -100, -1, -100, -100],
    [-100, -100, -100, -100, -100, -100, -1, -100, -1, 100],
    [-100, -100, -100, -100, -100, -1, -100, -1, -100, -100],
    [-1, -100, -100, -100, -100, -100, -100, -1, -100, 100]])


# pd.DataFrame(rewards)


def intialize_q(m, n):
    return np.zeros((m, n))


q_matrix = intialize_q(10, 10)


# pd.DataFrame(q_matrix)


def set_initial_state(state=10):
    return np.random.randint(0, state)


def get_action(current_state, reward_matrix):
    valid_actions = []
    for action in enumerate(reward_matrix[current_state]):
        if action[1] != -100:
            valid_actions += [action[0]]
    return random.choice(valid_actions)


def take_action(current_state, reward_matrix, gamma, verbose=False):
    action = get_action(current_state, reward_matrix)
    sa_reward = reward_matrix[current_state, action]  # current_state-action reward
    ns_reward = max(q_matrix[action,])  # next state-action reward
    q_current_state = sa_reward + (gamma * ns_reward)
    q_matrix[current_state, action] = q_current_state  # matutes q_matrix
    new_state = action
    if verbose:
        print(q_matrix)
        print(f"Old State: {current_state} | New State: {new_state}\n\n")
        if new_state == 9:
            print(f"Agent has reached it's goal!")
    return new_state


def initialize_episode(reward_matrix, initial_state, gamma, verbose=False):
    # Runs 1 episode unitl the agent reaches its goal-state
    current_state = initial_state
    while True:
        current_state = take_action(current_state, reward_matrix, gamma, verbose)
        if current_state == 9:
            break


def train_agent(iteration, reward_matrix, gamma, verbose=False):
    # Runs a given number of episodes then normalizs the matrix
    print("Training in progress...")
    for episode in range(iteration):
        initial_state = 4
        initialize_episode(reward_matrix, initial_state, gamma, verbose)
    print("Training complete!")
    return q_matrix


def normalize_matrix(q_matrix):
    normalize_q = q_matrix / max(q_matrix[q_matrix.nonzero()]) * 100
    return normalize_q.astype(int)


# Test run of full training
gamma = 0.8
initial_state = 4
# initial_action = get_action(initial_state, rewards)
q_table = train_agent(2000, rewards, gamma, False)
print(pd.DataFrame(q_table))
# pd.DataFrame(q_table)
