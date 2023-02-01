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
        self.taken_actions = {}  # id event : (old_state, old_action)
        self.qtable = {}  # drone : drone ???
        self.link_parameters = {}  # drone : (TR, ES, FS)

    def feedback(self, drone, id_event, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @param drone: The drone that holds the packet
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

        if id_event in self.taken_actions:
            # BE AWARE, IMPLEMENT YOUR CODE WITHIN THIS IF CONDITION OTHERWISE IT WON'T WORK!
            # TIPS: implement here the q-table updating process

            # Drone id and Taken actions
            # print(f"\nIdentifier: {self.drone.identifier}, Taken Actions: {self.taken_actions}, Time Step: {self.simulator.cur_step}")

            # feedback from the environment
            # print(drone, id_event, delay, outcome)

            state, action, hops_count, pck_creation_time = self.taken_actions[id_event]

            # remove the entry, the action has received the feedback
            del self.taken_actions[id_event]

            # UPDATE TR
            self.drone.number_packets += 1
            if outcome == 1:
                self.drone.successful_deliveries += 1
            self.drone.tr = self.drone.successful_deliveries / self.drone.number_packets

            # UPDATE Q-TABLE
            a, y = 0.5, 0.7

            # UPDATE Q-TABLE-HC, Q-TABLE-SPDT
            action = action.identifier
            next_state = action
            min_hc = min(self.simulator.qtable_hc[next_state], key=self.simulator.qtable_hc[state].get)
            r_hc = hops_count  # REWARD FOR HC (more higher -> more "negative")
            self.simulator.qtable_hc[state][action] = (1 - a) * self.simulator.qtable_hc[state][action] + a * (
                        r_hc + y * min_hc)

            # r_spdt = delay
            total_delay = self.simulator.cur_step - pck_creation_time
            if total_delay > 2000:
                total_delay = 2000
            min_spdt = min(self.simulator.qtable_spdt[next_state], key=self.simulator.qtable_spdt[state].get)
            self.simulator.qtable_spdt[state][action] = ((1 - a) * self.simulator.qtable_spdt[state][action] + a * (
                        y * min_spdt + delay)) / 2000

    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.

        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """

        # UPDATE RESIDUAL ENERGY
        self.drone.residual_energy -= 100

        state = self.drone.identifier

        # UPDATE ALL LINK PARAMETERS
        for hello_pck, neigh in opt_neighbors:
            self.link_parameters[neigh] = self.update_link_param(neigh, hello_pck)
            # if self.drone.identifier == 1:
            # print(str(neigh.identifier) + " : " + str(hello_pck.optional_data))

        # FUZZY LOGIC
        candidates = []
        for hello, neigh in opt_neighbors:
            hc, spdt = None, None
            tr, es, fs = self.link_parameters[neigh][0], self.link_parameters[neigh][1], self.link_parameters[neigh][2]
            if neigh.identifier in self.simulator.qtable_hc[state]:
                hc = self.simulator.qtable_hc[state][neigh.identifier]
            if neigh.identifier in self.simulator.qtable_spdt[state]:
                spdt = self.simulator.qtable_spdt[state][neigh.identifier]
            candidates.append((neigh, self.fuzzy_logic(tr, es, fs, hc, spdt)))

        # RELAY SELECTION
        relay = None
        cur_priority = -1
        for drone, priority in candidates:
            if priority > cur_priority:
                cur_priority = priority
                relay = drone

        action = relay  # the state is defined above
        packet.hops += 1
        self.taken_actions[packet.event_ref.identifier] = (state, action, packet.hops, packet.time_step_creation)
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

    def extract_max(self, qtable, flag):
        if flag:
            max_ = 0
            for key in qtable:
                if qtable[key][0] >= max_:
                    max_ = qtable[key][0]
            return max_
        else:
            max_ = 0
            for key in qtable:
                if qtable[key][1] >= max_:
                    max_ = qtable[key][1]
            return max_
