import api
import agent
import time


def full_algo():

    api.enter_world("0")

    Q = agent.load_json("Q.json")

    N = agent.load_json("N.json")

    prev_state = None
    prev_action = None

    current_pos = api.locate_me()
    reward = 0

    terminal_state = True

    for i in range(0, 100):
        while terminal_state:
            next_action, Q, N = agent.q_learning_agent(
                prev_state, prev_action, current_pos, reward, Q, N, 0.9
            )
            prev_state = current_pos
            prev_action = next_action

            reward = json.loadsapi.make_move()

            current_pos = api.locate_me()

            agent.write_persist("Q.json", Q)
            agent.write_persist("N.json", N)

            time.sleep(15)
