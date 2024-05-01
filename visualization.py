import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import re
import time
import os

def load_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    # print_grid("test.txt", data, "1")
    return data


def print_grid(filename, data, world_id):

    grid = np.zeros((40, 40))

    for i in data[world_id]:

        avg_val = 0

        for direction in data[world_id][i]:
            avg_val += data[world_id][i][direction]

        pattern = re.compile(r"[\[\]]", re.IGNORECASE)
        new_i = re.sub(pattern, "", i).split(",")
        x, y = tuple(new_i)
        grid[int(x)][int(y)] = abs(avg_val)
        # np.savetxt(filename, grid)
        plt.imshow(
            grid.T,
            norm="log",
            interpolation="nearest",
            origin="lower",
            cmap="PuRd",
        )
        # plt.plot(grid)

    # Check if directory exists, create if it doesn't
    directory = str(world_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # plt.show()
    plt.savefig(str(world_id) + "/" + str(time.time_ns()) + ".png")


# load_json("Q.json")

if __name__ == "__main__":
    q_save = load_json("Q.json")
    print_grid("test", q_save, world_id="5")