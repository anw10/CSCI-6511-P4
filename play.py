import api
import agent
import time
import visualization
import os


def format_coord_enter_world(current_pos):

    if current_pos == None:
        coord_formated = False
    else:
        coord = tuple(current_pos.replace(":", ""))
        coord_formated = f"[{coord[0]},{coord[1]}]"

    return coord_formated


def format_coord_make_move(current_pos):

    if current_pos == None:
        coord_formated = False
    else:
        coord = current_pos
        x_coord = str(coord["x"])
        y_coord = str(coord["y"])
        coord_formated = "[" + x_coord + "," + y_coord + "]"

    return coord_formated


def full_algo(world=str(0), epoch=20, gamma=0.9999):

    world = str(world)

    Q = agent.load_json("Q.json")
    N = agent.load_json("N.json")

    # Hold coords for neg and pos terminal states, if next_action is ever in neg_t_coords don't take it
    pos_t_coords = agent.load_json("posT.json")
    neg_t_coords = agent.load_json("negT.json")

    for i in range(0, epoch):

        epoch_file = open("runs.txt", "a")
        epoch_file.write("world is " + str(world) + " epoch is " + str(i))
        epoch_file.write("\n")
        epoch_file.close()

        q_save = visualization.load_json("Q.json")

        if not os.path.exists(world):
            os.mkdir(world)

        visualization.print_grid("test", q_save, world)

        # Each epoch, enter the world
        response_dict = api.enter_world(world)
        if response_dict["code"] == "FAIL":
            current_pos = api.locate_me()["state"]
        else:
            current_pos = response_dict["state"]
        # current_pos = "0:0"  ##

        coord_formated = format_coord_enter_world(current_pos)

        prev_state = None
        prev_action = None
        reward = 0

        while coord_formated:

            next_action, Q, N = agent.q_learning_agent(
                prev_state, prev_action, coord_formated, reward, Q, N, gamma, world
            )
            prev_prev_state = prev_state
            prev_prev_action = prev_action
            prev_state = coord_formated
            prev_action = next_action

            print(next_action)
            reward, current_pos = api.make_move(
                next_action, world
            )  ## Returns reward and new_state

            coord_formated = format_coord_make_move(current_pos)

            if current_pos == None:
                # Save terminal reward to Q
                print(f"prev_prev_state: {prev_prev_state}")
                print(f"prev_prev_action: {prev_prev_action}")
                print(f"terminal state: {prev_state}")
                print(f"reward at terminal state: {reward}")
                next_action, Q, N = agent.q_learning_agent(
                    prev_prev_state,
                    prev_prev_action,
                    prev_state,
                    reward,
                    Q,
                    N,
                    gamma,
                    world,
                )

                if reward < 0:
                    neg_t_coords[world].append(prev_state)
                else:
                    pos_t_coords[world].append(prev_state)

            agent.write_persist("Q.json", Q)
            agent.write_persist("N.json", N)
            agent.write_persist("posT.json", pos_t_coords)
            agent.write_persist("negT.json", neg_t_coords)

            time.sleep(5)


if __name__ == "__main__":
    # Run game
    full_algo(world=4, epoch=20)
