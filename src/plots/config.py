"""
Write your plot configuration script here
Below you can see just an example about how to write a config file.
You can import constants, lists and dictionaries in plot_data.py
"""

# *** EXAMPLE ***
import numpy as np
import matplotlib.pyplot as plt
import json
from src.utilities.config import SIM_DURATION

LABEL_SIZE = 22
LEGEND_SIZE = 20
SUP_TITLE_SIZE = 26
TITLE_SIZE = 20
TICKS_SIZE = 18
OTHER_SIZES = 20

METRICS_OF_INTEREST = ['mean_packet_delivery_ratio',
                       'mean_standard_deviation_ratio',
                       'mean_packet_delivery_time',
                       'mean_standard_deviation_packet_delivery_time',
                       # 'mean_number_of_relays',
                       # 'mean_standard_deviation_relays',
                       # ('mean_exploration',
                       # 'mean_exploitation_total',
                       # 'mean_exploitation_q_values',
                       # 'mean_exploitation_heuristic')
                       'mean_hc',
                       'mean_spdt']

ALGORITHMS = {"QL": {"title": "Multi-objective Routing"},
              # "NQL": {"title": "Neighbors-Based Routing Algorithm"},
              # "GEO": {"title": "GEO Routing Algorithm"},
              # "RND": {"title": "Random Routing Algorithm"}
              }

X_LABEL = "Number of drones"
STEPS = int(SIM_DURATION / 1000) + 1
Y_LABEL_MEAN = "Mean values"
Y_LABEL_DEV = "deviation"
X_VALUES = np.array([5, 10, 15, 20, 25, 30])
HEIGHT = 16

PLOT_INFO = {
    'mean_packet_delivery_ratio': {
        "title": "Mean Packet delivery ratio",
        "y_label": Y_LABEL_MEAN + " (ratio)",
        "x_label": X_LABEL
    },
    'mean_standard_deviation_ratio': {
        "title": "Standard Deviation of packet delivery ratio",
        "y_label": Y_LABEL_DEV + " (ratio)",
        "x_label": X_LABEL
    },
    'mean_packet_delivery_time': {
        "title": "Mean Packet delivery time",
        "y_label": Y_LABEL_MEAN + " (ms)",
        "x_label": X_LABEL
    },
    'mean_standard_deviation_packet_delivery_time': {
        "title": "Standard Deviation of packet delivery time",
        "y_label": Y_LABEL_DEV + " (ms)",
        "x_label": X_LABEL
    },
    'mean_hc': {
        "title": "Mean number of hops during the simulation",
        "y_label": Y_LABEL_MEAN + " (number of hops)",
        "x_label": "Simulation Lifetime (s)"

    },
    "mean_spdt": {
        "title": "Mean Successfully Delivered Packets during the simulation",
        "y_label": Y_LABEL_MEAN + " (ms)",
        "x_label": "Simulation Lifetime (s)"

    }

}

# PLOT_COLORS = {
#     "BLACK": {
#         "face_color": "black",
#         "spines_color": "white",
#         "grid_color": "grey",
#         "plot_color": "tab:green",
#         "tick_color": "white",
#         "label_color": "white",
#         "title_color": "white"
#     }
# }

# SCALE_LIM_DICT = {
#     "number_of_packets_to_depot": {
#         "scale": "linear",
#         "ylim": (0, 1000)
#     },
#     "packet_mean_delivery_time": {
#         "scale": "linear",
#         "ylim": (0, 5)
#     },
#     "mean_number_of_relays": {
#         "scale": "linear",
#         "ylim": (0, 10)
#     }
# }

# PLOT_DICT = {
#     "algo_1": {
#         "hatch": "",
#         "markers": "X",
#         "linestyle": "-",
#         "color": plt.cm.tab10(0),
#         "label": "Algo 1",
#         "x_ticks_positions": np.array(np.linspace(0, 8, 5))
#     },
#     "algo_2": {
#         "hatch": "",
#         "markers": "p",
#         "linestyle": "-",
#         "color": plt.cm.tab10(1),
#         "label": "Algo 2",
#         "x_ticks_positions": np.array(np.linspace(0, 8, 5))
#
#     },
#     "algo_n": {
#         "hatch": "",
#         "markers": "s",
#         "linestyle": "-",
#         "color": plt.cm.tab10(8),
#         "label": "Algo n",
#         "x_ticks_positions": np.array(np.linspace(0, 8, 5))
#
#     }
# }

# *** EXAMPLE ***
