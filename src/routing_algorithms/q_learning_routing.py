import random

from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
import math
import numpy as np
import src.routing_algorithms.tables as tables
from src.utilities import config as config


class QLearningRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone=drone, simulator=simulator)
        self.taken_actions = dict()  # id event : (action, hop_number)
        self.link_parameters = {}  # drone : (TR, ES, FS)
        self.qtable_hc = simulator.qtable_hc
        self.qtable_spdt = simulator.qtable_spdt

        self.alpha_h = 1
        self.alpha_t = 1
        self.gamma = 1

    def feedback(self, drone, id_event, hops, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @param drone: The drone that holds the packet
        @hops: all hops of the drone
        @param id_event: The Event id
        @param delay: packet delay
        @param outcome: -1 or 1 (read below)
        @return:
        """

        # outcome can be:
        #   -1 if the packet/event expired;
        #   1 if the packets has been delivered to the depot

        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple
        # feedback for the same packet!!

        hope = list(self.taken_actions.keys())

        if id_event in hope:

            if outcome == 1:
                print(self.drone.identifier, " : ", self.taken_actions[id_event])


            return
            # # BE AWARE, IMPLEMENT YOUR CODE WITHIN THIS IF CONDITION OTHERWISE IT WON'T WORK!
            # # TIPS: implement here the q-table updating process
            #
            # # Drone id and Taken actions
            # # print(f"\nIdentifier: {self.drone.identifier}, Taken Actions: {self.taken_actions}, Time Step: {self.simulator.cur_step}")
            # #
            # # # feedback from the environment
            # # print(drone, id_event, delay, outcome)
            #
            # state, action = self.taken_actions[id_event]
            # # print(drone, state, action, " : " + str(outcome))
            #
            # # remove the entry, the action has received the feedback
            # del self.taken_actions[id_event]
            #
            # # TODO: Davide, compute here the TR
            # self.drone.number_packets += 1
            # if outcome == 1:
            #     self.drone.successful_deliveries += 1
            # self.drone.tr = self.drone.successful_deliveries / self.drone.number_packets
            #
            # # TODO: Nic e Giacomo, Q-Learning
            # # UPDATE Q-TABLE
            # # if state in self.qtable:
            # #     if action in self.qtable[state]:
            # #         self.qtable[state][action][0] += 0  # HC
            # #         self.qtable[state][action][1] += 0  # SPDT
            # #     else:
            # #         self.qtable[state][action] = [0, 0]
            # #         self.qtable[state][action][0] = 0  # HC
            # #         self.qtable[state][action][1] = 0  # SPDT
            # # else:
            # #     self.qtable[state] = {}
            # #     self.qtable[state][action] = [0, 0]
            # #     self.qtable[state][action][0] = 0  # HC
            # #     self.qtable[state][action][1] = 0  # SPDT
            #
            # # if self.drone.identifier == 1:
            # # print(self.qtable)

    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.

        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """

        packet_id = packet.event_ref.identifier

        hc = None
        spdt = None
        state = None

        # update residual energyh
        self.drone.residual_energy -= 100

        # UPDATE ALL LINK PARAMETERS
        for hello_pck, neigh in opt_neighbors:
            self.link_parameters[neigh] = self.update_link_param(neigh, hello_pck)

        # FUZZY LOGIC
        candidates = []
        for hello, neigh in opt_neighbors:
            tr, es, fs = self.link_parameters[neigh][0], self.link_parameters[neigh][1], self.link_parameters[neigh][2]
            candidates.append((neigh, self.fuzzy_logic(tr, es, fs, hc, spdt)))

        relay = None
        cur_priority = -1
        for drone, priority in candidates:
            if priority > cur_priority:
                cur_priority = priority
                relay = drone
                self.simulator.exploration += 1

        # the drone hasn't any neigh ?
        if relay is None:
            relay = self.select_best_neigh(opt_neighbors)
            self.simulator.exploitation[0] += 1

        # print(relay, "|", self.drone)
        # if relay == self.drone.identifier:
        #     print("ciao")
        #     return None
        # print(relay.coords)

        # last_hop = packet.hops[-1]
        # if last_hop == relay.identifier:
        #     print("diocane")

        # packet.add_hop((self.drone.identifier, relay.identifier))

        # if packet_id not in set(self.taken_actions.keys()):
        #     self.taken_actions[packet_id] = [(relay.identifier, packet.n_hops)]
        # else:
        #     self.taken_actions[packet_id].append((relay.identifier, packet.n_hops))

        return relay

    def update_link_param(self, neigh, hello_pck):
        tr = hello_pck.optional_data[1]

        b1, b2 = 0.5, 0.5
        rej = hello_pck.optional_data[0]  # residual energy of neigh
        edr_j = hello_pck.speed / config.DRONE_MAX_ENERGY  # energy drain rate of neigh computed based on the velocity (and maybe on the transmission?)
        ie = config.DRONE_MAX_ENERGY  # initial energy for all nodes
        es = b1 * (rej / ie) - b2 * edr_j

        vj = hello_pck.speed  # velocity of neigh
        pos_neigh = hello_pck.cur_pos
        next_pos_neigh = hello_pck.next_target
        J = next_pos_neigh  # destination node, maybe next_pos_neigh?
        teta_i = util.angle_between_points(self.drone.coords, J, pos_neigh)
        teta_j = util.angle_between_points(pos_neigh, J, self.drone.coords)
        cos_jd = np.dot(J, pos_neigh) / (
                np.linalg.norm(J) * np.linalg.norm(pos_neigh))  # projection vector of node-neigh on the destination
        pdj = vj * cos_jd
        fs = math.cos(teta_i - teta_j) * pdj

        return tr, fs, es

    def fuzzy_logic(self, tr, es, fs, hc, spdt):
        tr, es, fs, hc, spdt = self.fuzzification(tr, es, fs, hc, spdt)
        route = tables.table_link_param(tr, es, fs)
        if hc is not None and spdt is not None:  # i.e, there aren't path-parameters
            route = tables.table_link_routh_param(tr, es, fs, hc, spdt)
        output = self.defuzzification(route)
        return output

    def fuzzification(self, tr, es, fs, hc, spdt):
        hc_fuzz, spdt_fuzz = None, None
        tr_fuzz = "m" if tr < 0.8 else "h"
        es_fuzz = "l" if es < 6 else "h"
        fs_fuzz = "b" if fs < 5 else "g"
        if hc is not None:
            hc_fuzz = "sm" if hc < 5 else "lg"
        if spdt is not None:
            spdt_fuzz = "sh" if spdt < 0.1 else "ln"
        return tr_fuzz, es_fuzz, fs_fuzz, hc_fuzz, spdt_fuzz

    def defuzzification(self, route):
        crisp_output = 0
        if route == "o_vb":
            crisp_output = 0
        if route == "o_b":
            crisp_output = 1
        if route == "o_act":
            crisp_output = 2
        if crisp_output == "o_g":
            crisp_output = 3
        if crisp_output == "o_p":
            crisp_output = 4
        return crisp_output

    def select_best_neigh(self, opt_neighbours):  # select the fastest drone that could reach the depeot
        relay = None
        depeot_pos = self.simulator.depot_coordinates
        time = 15000
        speed_drone = self.drone.speed
        for hello_packet, neigh in opt_neighbours:
            next_pos_neigh = hello_packet.next_target
            speed_neigh = hello_packet.speed
            new_distance = util.euclidean_distance(depeot_pos, next_pos_neigh)
            time_needed = new_distance / speed_neigh
            if time_needed < time:
                relay = neigh
                time = time_needed
        # maybe the drone itself can do the relay
        if util.euclidean_distance(depeot_pos, self.drone.coords) / speed_drone < time:
            relay = self.drone
        return relay

    def get_cell(self, position):
        xpos = position[0]
        ypos = position[1]
        return util.TraversedCells.coord_to_cell(size_cell=self.simulator.prob_size_cell,
                                                 width_area=self.simulator.env_width,
                                                 x_pos=xpos,
                                                 y_pos=ypos)[0]
