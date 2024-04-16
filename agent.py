import numpy as np
import json
# from dataclasses import dataclass, field

# @dataclass
# class Percept:
#     current_state: tuple[int, int]
#     reward: int


## Q-values I guess
def q_values():
    return True

## Utils

def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def alpha(visits):
    """ Adaptive learning rate based on number of visits """

    return 1 / (1 + visits)


def epsilon_greedy(actions, _, epsilon=0.1):
    """ Epsilon-greedy exploration strategy. """
    if np.random.rand() < epsilon:  # With probability epsilon, explore.
        return np.random.choice(list(actions.keys()))
    else:  # With probability 1-epsilon, exploit.
        return max(actions, key=actions.get)

def count_based(actions, visits):
    """ Count/Density-based exploration strategy. """

    raise NotImplementedError

## Q-Learning-Agent
def q_learning_agent(prev_state, prev_action, curr_state, reward, Q, N, discount, f=epsilon_greedy):
    """
    Q-Learning Agent that uses an exploration function f.

    Psuedocode:
    if s is not null then
        increment N_sa[s, a]
        Q[s, a] = Q[s, a] + alpha(N_sa[s, a])(r + gamma*max_a'Q[s', a'] - Q[s, a])
    (s, a) = s', argmax_a' f(Q[s', a'], N_sa[s', a'])   // where f is exploration function
    return a

    Args:
        prev_state: The previous state.
        prev_action: The action taken at the previous state.
        curr_state: The current state.
        reward: The reward signal at current state.
        Q: The Q-values table, where Q[state][action] is the Q-value for the state-action pair.
        N: The N visits table, where N[state][action] counts the visits to the state-action pair.
        discount: The discount factor (gamma).
        f: The exploration function
        
    Returns:
        next_action: The next action to take.
    """

    if prev_state is not None:
        N[prev_state][prev_action] += 1
        Q[prev_state][prev_action] = Q[prev_state][prev_action] + alpha(N[prev_state][prev_action]) * (reward + discount * max(Q[curr_state].values()) - Q[prev_state][prev_action])

    # Decide next action using exploration function f
    next_action = f(Q[curr_state], N[curr_state])
    return next_action
