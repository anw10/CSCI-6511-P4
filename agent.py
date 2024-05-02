import numpy as np
import json
import matplotlib.pyplot as plt
import re
import seaborn as sns


## Q-values I guess
def q_values():
    return True


def load_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    # print_grid("test.txt", data, "0")
    return data


def write_persist(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def print_grid(filename, data, world_id):

    grid = np.zeros((40, 40))

    for i in data[world_id]:

        avg_val = 0

        for direction in data[world_id][i]:
            avg_val += data[world_id][i][direction]

        pattern = re.compile(r"[\[\]]", re.IGNORECASE)
        new_i = re.sub(pattern, "", i).split(",")
        x, y = tuple(new_i)
        grid[int(x)][int(y)] = avg_val
        # np.savetxt(filename, grid)
        plt.imshow(grid)
        # plt.plot(grid)

    plt.show()


def alpha(visits):
    """
    Adaptive learning rate based on number of visits. Higher visits

    Args:
        visits (int): The count of visits of the direction taken from the previous state

    Returns:
        (float): Learning rate based on visits
    """

    return 1 / (1 + visits)
    # return 0.21


def epsilon_greedy(actions, _, epsilon=0.1):
    """
    Epsilon-greedy exploration strategy.

    Args:
        actions (dict): The actions available for the current state
        epsilon (int): Random exploration hyperparameter

    Returns:
        (str): Next action, whether it's exploring or exploiting
    """

    if np.random.rand() < epsilon:  # With probability epsilon, explore.
        return np.random.choice(list(actions.keys()))
    else:  # With probability 1-epsilon, exploit.
        return max(actions, key=actions.get)


def count_based(actions, visits, k=10, N_e=3, multiplier_at_zero_visits=0.5):
    """
    Count/Density-based exploration strategy to explore areas where badness is not yet established,

    R+ = u + k/visits
    f(u, n) = {R+ if n < N_e, else u}

    Args:
        actions (dict): The actions available for the current state
        visits (dict): The visits for the current state
        k (int): Exploration reward hyperparameter
        N_e (int): Cap for state-action tries hyperparameter, i.e., the agent should try the state-action pair at least N_e times.
        multiplier_at_zero_visits (float): Reward multiplier when a direction has not been visited from the current state

    Returns:
        next_action (str): Action with optimistic utility or exploited utility
    """

    def explore_optimisic_or_not(action):
        """R+ if n < N_e, else u"""

        visit_count = (
            visits[action] if visits[action] > 0 else multiplier_at_zero_visits
        )

        if visits[action] < N_e:
            return actions[action] + k / visit_count
        else:
            return actions[action]

    next_action = max(actions, key=explore_optimisic_or_not)

    return next_action


## Q-Learning-Agent
def q_learning_agent(
    prev_state, prev_action, curr_state, reward, Q, N, discount, world, f=count_based
):
    """
    Q-Learning Agent that uses an exploration function f.

    Psuedocode:
    if s is not null then
        increment N_sa[s, a]
        Q[s, a] = Q[s, a] + alpha(N_sa[s, a])(r + gamma*max_a'Q[s', a'] - Q[s, a])
    (s, a) = s', argmax_a' f(Q[s', a'], N_sa[s', a'])   // where f is exploration function
    return a

    Args:
        prev_state (str): The previous state.
        prev_action (str): The action taken at the previous state.
        curr_state (str): The current state.
        reward (float): The reward signal at current state.
        Q (dict): The Q-values table, where Q[state][action] is the Q-value for the state-action pair.
        N (dict): The N visits table, where N[state][action] counts the visits to the state-action pair.
        discount (float): The discount factor (gamma).
        world (str): Current world
        f: The exploration function

    Returns:
        next_action (str): The next action to take.
    """

    if prev_state is not None:
        # N[worldId][[x,y]]["DIRECTION"] += 1
        N[world][prev_state][prev_action] += 1
        Q[world][prev_state][prev_action] = Q[world][prev_state][prev_action] + alpha(
            N[world][prev_state][prev_action]
        ) * (
            reward
            + discount * max(Q[world][curr_state].values())
            - Q[world][prev_state][prev_action]
        )

    # Decide next action using exploration function f
    next_action = f(Q[world][curr_state], N[world][curr_state])
    return next_action, Q, N
