import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import re


def load_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    print_grid("test.txt", data, "0")
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
        grid[int(x)][int(y)] = avg_val
        # np.savetxt(filename, grid)
        plt.imshow(grid)
        # plt.plot(grid)

    plt.show()


load_json("Q.json")
