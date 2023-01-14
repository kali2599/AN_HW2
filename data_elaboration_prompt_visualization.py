"""
You can write here the data elaboration function/s

You should read all the JSON files containing simulations results and compute
average and std of all the metrics of interest.

You can find the JSON file from the simulations into the data.evaluation_tests folder.
Each JSON file follows the naming convention: simulation-current date-simulation id__seed_drones number_routing algorithm

In this way you can parse the name and properly aggregate the data.

To aggregate data you can use also external libraries such as Pandas!

IMPORTANT: Both averages and stds must be computed over different seeds for the same metric!
"""

import numpy as np
import os
import json
from glob import glob
import pandas as pd
from pandas import DataFrame


def compute_data_avg_std(path: str):
    """
    Computes averages and stds from JSON files
    @param path: results folder path
    @return: one or more data structure containing data
    """

    # TODO: Implement your code HERE
    cg = np.zeros((31, 6))
    cq = np.zeros((31, 6))
    mrg = np.zeros((31, 6))
    mrq = np.zeros((31, 6))
    mtg = np.zeros((31, 6))
    mtq = np.zeros((31, 6))

    for filename in path:

        with open(filename) as json_data:
            data = json.load(json_data)

        df = pd.DataFrame(data["mission_setup"])
        ra = df["routing_algorithm"]
        n_seed = df["seed"][0]
        n_drones = df["n_drones"][0]
        ratio = pd.DataFrame({data.get("packet_delivery_ratio")})[0]
        dt = pd.DataFrame({data.get("packet_mean_delivery_time")})[0]

        i = int(n_seed)
        j = int((n_drones / 5) - 1)

        if ra[0] == "RoutingAlgorithm.GEO":
            mrg[i][j] += ratio
            mtg[i][j] += dt
            cg[i][j] += 1

        elif ra[0] == "RoutingAlgorithm.QL":
            mrq[i][j] += ratio
            mtq[i][j] += dt
            cq[i][j] += 1

    for i in range(31):
        for j in range(6):
            if mrg[i][j] > 0:
                mrg[i][j] = round(mrg[i][j] / cg[i][j], 6)
                mtg[i][j] = round(mtg[i][j] / cg[i][j], 6)
            else:
                mrg[i][j] = -1
                mtg[i][j] = -1

            if mrq[i][j] > 0:
                mrq[i][j] = round(mrq[i][j] / cq[i][j], 6)
                mtq[i][j] = round(mtq[i][j] / cq[i][j], 6)
            else:
                mrq[i][j] = -1
                mtq[i][j] = -1

    print("Tabella packet_delivery_ratio con GEO Routing:")
    print(mrg)
    print("Tabella packet_mean_delivery_time con GEO Routing:")
    print(mtg)
    print("Tabella packet_delivery_ratio con QL Routing:")
    print(mrq)
    print("Tabella packet_mean_delivery_time con GEO Routing:")
    print(mtq)


if __name__ == "__main__":
    """
    You can run this file to test your script
    """

    path = "data/evaluation_tests/*.json"
    path = glob(path)

    compute_data_avg_std(path=path)
