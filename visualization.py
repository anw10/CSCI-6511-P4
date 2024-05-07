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

def print_gradient(filename, data, world_id):
    grid = np.zeros((40, 40))
    # Updated direction vectors
    direction_vectors = {'N': np.array([0, 1]), 'E': np.array([1, 0]), 'S': np.array([0, -1]), 'W': np.array([-1, 0])}
    
    plt.figure(figsize=(10, 10))
    
    for i in data[world_id]:
        vector_sum = np.zeros(2)
        
        for direction, value in data[world_id][i].items():
            vector_sum += direction_vectors[direction] * value
        
        # Normalize the vector sum to get the average direction
        if np.linalg.norm(vector_sum) > 0:
            vector_sum /= np.linalg.norm(vector_sum)
        
        pattern = re.compile(r"[\[\]]", re.IGNORECASE)
        new_i = re.sub(pattern, "", i).split(",")
        x, y = map(int, new_i)
        grid[x][y] = np.sum(np.abs(list(data[world_id][i].values())))
        
        dx, dy = vector_sum
        plt.arrow(y, x, dx, dy, head_width=0.3, head_length=0.4, fc='k', ec='k')
    
    plt.imshow(grid.T, cmap='PuRd', origin='lower', interpolation='nearest')
    
    directory = str(world_id)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    plt.savefig(f"{directory}/Gradient_{time.time_ns()}.png")
    plt.close()


if __name__ == "__main__":
    q_save = load_json("Q.json")
    print_gradient("test", q_save, world_id="3")
    # print_grid("test", q_save, world_id="3")