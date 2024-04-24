import api
import agent
import time


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


def full_algo(world=str(0), epoch=1):

    world = str(world)

    Q = agent.load_json("Q.json")
    N = agent.load_json("N.json")

    for i in range(0, epoch):

        # Each epoch, enter the world
        if api.enter_world(world)["code"] == "FAIL":
            current_pos = api.locate_me()["state"]
        else:
            current_pos = api.enter_world(world)["state"]
        # current_pos = "0:0"  ##

        coord_formated = format_coord_enter_world(current_pos)

        prev_state = None
        prev_action = None
        reward = 0

        while coord_formated:
            next_action, Q, N = agent.q_learning_agent(
                prev_state, prev_action, coord_formated, reward, Q, N, 0.9, world
            )
            prev_state = coord_formated
            prev_action = next_action

            reward, current_pos = api.make_move(
                next_action, world
            )  ## Returns reward and new_state

            coord_formated = format_coord_make_move(current_pos)

            agent.write_persist("Q.json", Q)
            agent.write_persist("N.json", N)

            time.sleep(15)


if __name__ == "__main__":
    # Run game
    full_algo(world=0, epoch=1)
