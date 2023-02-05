"""
Implement here your plotting functions
Below you can see a print function example.
You should use it as a reference to implements your own plotting function

IMPORTANT: if you need you can and should use other matplotlib functionalities! Use
            the following example only as a reference

The plot workflow is can be summarized as follows:

    1) Extensive simulations
    2) Json file containing results
    3) Compute averages and stds for each metric for each algorithm
    4) Plot the results

In order to maintain the code tidy you can use:

    - src.plots.config.py file to store all the parameters you need to
        get wonderful plots (see the file for an example)

    - src.plots.data.data_elaboration.py file to write the functions that compute averages and stds from json
        result files

    - src.plots.plot_data.py file to make the plots.

The script plot_data.py can be run using python -m src.plots.plot_data

"""

# ***EXAMPLE*** #
import matplotlib.pyplot as plt
import numpy as np
import json
import config

# from src.experiments.json_and_plot import ALL_SIZE
# from src.plots.config import PLOT_DICT, LABEL_SIZE, LEGEND_SIZE, properties
from src.utilities.config import N_DRONES

DATA = json.load(open("data/output.json", "r"))


def plot(algorithms: list):
    metrics = config.METRICS_OF_INTEREST
    # n_plots = len(metrics)
    n_columns = 1
    height = config.HEIGHT
    width = height * n_columns
    name = -1
    fig, graph_hc = plt.subplots(nrows=1, ncols=n_columns, figsize=(width, height))
    fig, graph_spdt = plt.subplots(nrows=1, ncols=n_columns, figsize=(width, height))
    fig, graph_ratio = plt.subplots(nrows=1, ncols=n_columns, figsize=(width, height))
    fig, graph_delivery_time = plt.subplots(nrows=1, ncols=n_columns, figsize=(width, height))
    for metric in metrics:
        name += 1
        # fig.suptitle(config.PLOT_INFO[metric]["title"], fontsize=config.SUP_TITLE_SIZE)
        # fig.suptitle(fontsize=config.SUP_TITLE_SIZE)
        if metric == "mean_hc":
            ax = graph_hc
            ax.tick_params(axis='both', which='major', labelsize=config.TICKS_SIZE)
            ax.set_title(label=config.PLOT_INFO[metric]["title"], fontsize=config.TITLE_SIZE)
            ax.set_xlabel(xlabel=config.PLOT_INFO[metric]["x_label"], fontsize=config.LABEL_SIZE)
            ax.set_ylabel(ylabel=config.PLOT_INFO[metric]["y_label"], fontsize=config.LABEL_SIZE)
            ax.grid(linewidth=0.3, color="grey")
            x_values = np.arange(config.STEPS)
            for key in DATA[metric]:
                y_values = []
                for step in DATA[metric][key]:
                    y_values.append(DATA[metric][key][step])
                ax.plot(x_values, y_values, label=str(key) + " drones", marker='.', ms=20)
                ax.legend(fontsize=20)

        elif metric == "mean_spdt":
            ax = graph_spdt
            ax.tick_params(axis='both', which='major', labelsize=config.TICKS_SIZE)
            ax.set_title(label=config.PLOT_INFO[metric]["title"], fontsize=config.TITLE_SIZE)
            ax.set_xlabel(xlabel=config.PLOT_INFO[metric]["x_label"], fontsize=config.LABEL_SIZE)
            ax.set_ylabel(ylabel=config.PLOT_INFO[metric]["y_label"], fontsize=config.LABEL_SIZE)
            ax.grid(linewidth=0.3, color="grey")
            x_values = np.arange(config.STEPS)
            for key in DATA[metric]:
                y_values = []
                for step in DATA[metric][key]:
                    y_values.append(DATA[metric][key][step])
                ax.plot(x_values, y_values, marker='.', ms=20, label=str(key) + " drones")
                ax.legend(fontsize=20)
        elif metric == "mean_packet_delivery_ratio":
            ax = graph_ratio
            ax.tick_params(axis='both', which='major', labelsize=config.TICKS_SIZE)
            ax.set_title(label="Delivery ratio packets", fontsize=config.TITLE_SIZE)
            # ax.set_title(label=config.ALGORITHMS[algorithm]["title"], fontsize=config.TITLE_SIZE)
            ax.set_xlabel(xlabel=config.PLOT_INFO[metric]["x_label"], fontsize=config.LABEL_SIZE)
            ax.set_ylabel(ylabel=config.PLOT_INFO[metric]["y_label"], fontsize=config.LABEL_SIZE)
            ax.grid(linewidth=0.3, color="grey")
            ax.plot(config.X_VALUES, DATA[metric], marker='.', ms=20, label="Mean")
            ax.legend(fontsize=20)

        elif metric == "mean_standard_deviation_ratio":
            ax = graph_ratio
            ax.plot(config.X_VALUES, DATA[metric], marker='.', ms=20, label="Deviation")
            ax.legend(fontsize=20)

        elif metric == "mean_packet_delivery_time":
            ax = graph_delivery_time
            ax.tick_params(axis='both', which='major', labelsize=config.TICKS_SIZE)
            ax.set_title(label="Mean delivery time of packets", fontsize=config.TITLE_SIZE)
            # ax.set_title(label=config.ALGORITHMS[algorithm]["title"], fontsize=config.TITLE_SIZE)
            ax.set_xlabel(xlabel=config.PLOT_INFO[metric]["x_label"], fontsize=config.LABEL_SIZE)
            ax.set_ylabel(ylabel=config.PLOT_INFO[metric]["y_label"], fontsize=config.LABEL_SIZE)
            ax.grid(linewidth=0.3, color="grey")
            ax.plot(config.X_VALUES, DATA[metric], marker='.', ms=20, label="Mean")
            ax.legend(fontsize=20)
        else:
            ax = graph_delivery_time
            ax.plot(config.X_VALUES, DATA[metric], marker='.', ms=20, label="Deviation")
            ax.legend(fontsize=20)


        #plt.savefig("figures/" + str(name), dpi=400, format="png")
    plt.tight_layout()
    plt.show()

    # plt.clf()

    # """
    # This method has the ONLY responsibility to plot data
    # @param y_data_std:
    # @param y_data:
    # @param algorithm:
    # @param type:
    # @return:
    # """
    # values = json.load(open("data/output.json", "r"))
    # x_values = np.array([5, 10, 15, 20, 25, 30])
    #
    # # QL Mean_ratio_plot
    # fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    # y_values = values["media_ratio"]["QL"]
    # # x_values = [5, 10, 15, 20, 25, 30]
    # # ax1.plot(x_values, y_values)
    # plt.plot(x_values, y_values, plottype="bar")
    # props = properties["mean_ratio_plot"]
    # ax1.tick_params(axis='both', which='major', labelsize=18)
    # ax1.set_title(label=props["title"], fontsize=30)
    # ax1.set_xlabel(xlabel=props["xlabel"], fontsize=20)
    # ax1.set_ylabel(ylabel=props["ylabel"], fontsize=20)
    # plt.show()
    #
    # # # QL Mean Explr and Explt
    # # fig, hope = plt.subplots(figsize=(14, 14))
    # # exploration_values = values["exploration"]["QL"]
    # # exploitation_total_values = values["exploitation_total"]["QL"]
    # # q_exploitation_values = values["exploitation_q_values"]["QL"]
    # # exploitation_heuristic_values = values["exploitation_heuristic"]["QL"]
    # # n = 0.75
    # # n_mezzi = n/2
    # # hope.bar(x_values - (n + n_mezzi), exploration_values, n, label="exploration")
    # # # hope.plot(x_values, exploration_values)
    # # hope.bar(x_values - n_mezzi, exploitation_total_values, n, label="total exploitation")
    # # # hope.plot(x_values, exploitation_total_values)
    # # hope.bar(x_values + n_mezzi, q_exploitation_values, n, label="exploitation with q values")
    # # # hope.plot(x_values, q_exploitation_values)
    # # hope.bar(x_values + (n + n_mezzi), exploitation_heuristic_values, n, label="exploitation with heuristic")
    # # # hope.plot(x_values, exploitation_heuristic_values)
    # # hope.legend(prop={'size': 17})
    # # plt.show()
    #
    # # print(f"Algorithm: {algorithm}")
    # #
    # # print(f"y_data: {y_data}\ny_data_std: {y_data_std}")
    # #
    # # ax1.errorbar(x=np.array(PLOT_DICT[algorithm]["x_ticks_positions"]),
    # #              y=y_data,
    # #              yerr=y_data_std,
    # #              label=PLOT_DICT[algorithm]["label"],
    # #              marker=PLOT_DICT[algorithm]["markers"],
    # #              linestyle=PLOT_DICT[algorithm]["linestyle"],
    # #              color=PLOT_DICT[algorithm]["color"],
    # #              markersize=8)
    # #
    # # ax1.set_ylabel(ylabel="Metric 1", fontsize=LABEL_SIZE)
    # # ax1.set_xlabel(xlabel="UAVs", fontsize=LABEL_SIZE)
    # # ax1.tick_params(axis='both', which='major', labelsize=ALL_SIZE)
    # #
    # # plt.legend(ncol=1,
    # #            handletextpad=0.1,
    # #            columnspacing=0.7,
    # #            prop={'size': LEGEND_SIZE})
    # #
    # # plt.grid(linewidth=0.3)
    # # plt.tight_layout()
    # # plt.savefig("figures/" + type + ".svg")
    # # plt.savefig("figures/" + type + ".png", dpi=400)
    # # plt.show()
    # # plt.clf()


# TODO: Implement your code HERE


if __name__ == "__main__":
    """
    Run this file to get the plots.
    Of course, since you need to plot more than a single data series (one for each algorithm) you need to modify
    plot() in a way that it can handle a multi-dimensional data (one data series for each algorithm). 
    y_data and y_data_std could be for example a list of lists o a dictionary containing lists. It up to you to decide
    how to deal with data
    """

    # ***EXAMPLE***

    # you can call the compute_data_avg_std in data_elaboration function here to get all the data you need
    # in this example that function is "approximated" using np.linspace()

    # algorithm = "algo_1"
    # y_data = np.linspace(0, 10, 5)
    # y_data_std = np.linspace(0, 1, 5)
    # type = "metric_1"
    plot(list(config.ALGORITHMS.keys()))

    # ***EXAMPLE***

    # TODO: Implement your code HERE
