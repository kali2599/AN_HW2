from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
import math
import numpy as np
import src.routing_algorithms.tables as tables
from src.utilities import config as config


class QLearningRoutingChain(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone=drone, simulator=simulator)
        self.chain_of_actions = dict()  # id event : [(action, hop_number)]
        self.link_parameters = {}  # drone : (TR, ES, FS)

        self.qtable_hc = {drone.identifier: dict()}
        self.qtable_spdt = {drone.identifier: dict()}

        self.alpha_h = 0.5
        self.alpha_t = 0.5
        self.gamma = 0.7
        self.hop_delay = 0.01

    def feedback(self, id_event, hops, n_hops, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @hops: all hops of the drone
        @hops: len(hops)
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

        if id_event in self.chain_of_actions:
            # # BE AWARE, IMPLEMENT YOUR CODE WITHIN THIS IF CONDITION OTHERWISE IT WON'T WORK!

            # UPDATE TR
            self.drone.number_packets += 1

            if outcome > 0:

                self.drone.successful_deliveries += 1

                # TMP STUFF
                # if n_hops > self.simulator.max_jumps:
                #     self.simulator.max_jumps = n_hops

                my_id = self.drone.identifier

                # print("drone ", my_id, "'s actions: ", self.taken_actions[id_event])

                my_actions = reversed(self.chain_of_actions[id_event])

                for action in my_actions:
                    relay_id = action[0]
                    hop = action[1]
                    hc_reward = self.compute_reward_hc(n_hops, hop)

                    if hop == n_hops:
                        self.simulator.number_of_packets += 1
                        hop_delay = action[2]
                        spdt_reward = self.compute_reward_spdt(delay, hop_delay)
                        self.update_qtables_last_hop(my_id, relay_id, hc_reward, spdt_reward)
                        # print("\n")
                        continue

                    next_action_id = hops[hop + 1][1]
                    hop_delay = hops[hop + 1][2]
                    spdt_reward = self.compute_reward_spdt(delay, hop_delay)
                    self.update_qtables(my_id, relay_id, next_action_id, hc_reward, spdt_reward)
                    # print("\n")

            self.drone.tr = self.drone.successful_deliveries / self.drone.number_packets

        return

    def update_qtables(self, my_id, action_id, next_action_id, hc_reward, spdt_reward):
        qhc = self.qtable_hc
        qspdt = self.qtable_spdt

        if action_id not in qhc:
            qhc[action_id] = {next_action_id: self.alpha_h * hc_reward}
            qspdt[action_id] = {next_action_id: self.alpha_t * spdt_reward}
            if action_id not in qhc[my_id]:
                qhc[my_id][action_id] = self.alpha_h * hc_reward
                qspdt[my_id][action_id] = self.alpha_t * spdt_reward
            else:
                qhc[my_id][action_id] = (1 - self.alpha_h) * qhc[my_id][action_id] + self.alpha_h * hc_reward
                qspdt[my_id][action_id] = (1 - self.alpha_h) * qspdt[my_id][action_id] + self.alpha_t * spdt_reward


        elif next_action_id not in qhc[action_id]:
            # QHC
            qhc[action_id][next_action_id] = self.alpha_h * hc_reward
            qhc[my_id][action_id] = (1 - self.alpha_h) * qhc[my_id][action_id] + \
                                    self.alpha_h * (self.gamma * min(qhc[action_id].values()))
            # Q-SPDT
            qspdt[action_id][next_action_id] = self.alpha_t * (spdt_reward + self.hop_delay)
            qspdt[my_id][action_id] = (1 - self.alpha_t) * qspdt[my_id][action_id] + \
                                      self.alpha_t * (self.gamma * min(qspdt[action_id].values()) + self.hop_delay)

        else:
            # QHC
            qhc[action_id][next_action_id] = (1 - self.alpha_h) * qhc[action_id][next_action_id] + \
                                             self.alpha_h * hc_reward
            qhc[my_id][action_id] = (1 - self.alpha_h) * qhc[my_id][action_id] + \
                                    self.alpha_h * (self.gamma * min(qhc[action_id].values()))
            # QSPDT
            qspdt[action_id][next_action_id] = (1 - self.alpha_t) * qspdt[action_id][next_action_id] + \
                                               self.alpha_t * (spdt_reward + self.hop_delay)
            qspdt[my_id][action_id] = (1 - self.alpha_t) * qspdt[my_id][action_id] + \
                                      self.alpha_t * (self.gamma * min(qspdt[action_id].values()) + self.hop_delay)
        # print("pre-update-> ", qspdt)
        # hc_action_next = qhc[action_id][next_action_id]
        # hc_state_action = qhc[my_id][action_id]
        # spdt_state_action = qspdt[my_id][action_id]
        # spdt_action_next = qspdt[action_id][next_action_id]
        #
        # # QHC-UPDATE
        # if hc_action_next is None:
        #     qhc[action_id][next_action_id] = hc_action_next = self.alpha_h * hc_reward
        # else:
        #     qhc[action_id][next_action_id] = (1 - self.alpha_h) * hc_action_next + self.alpha_h * hc_reward
        # if hc_state_action is None:
        #     qhc[my_id][action_id] = hc_action_next
        # else:
        #     qhc[my_id][action_id] = (1 - self.alpha_h) * hc_state_action + \
        #                             self.alpha_h * (self.gamma * min(
        #         filter(lambda x: x is not None, qhc[action_id].values())))
        #
        # # SPDT-UPDATE
        # if spdt_action_next is None:
        #     qspdt[action_id][next_action_id] = spdt_action_next = self.alpha_t * (spdt_reward + self.hop_delay)
        # else:
        #     qspdt[action_id][next_action_id] = (1 - self.alpha_t) * spdt_action_next + \
        #                                        self.alpha_t * (spdt_reward + self.hop_delay)
        # if spdt_state_action is not None:
        #     qspdt[my_id][action_id] = (1 - self.alpha_t) * spdt_state_action + \
        #                             self.alpha_t * (self.gamma * min(
        #         filter(lambda x: x is not None, qspdt[action_id].values())) + self.hop_delay)
        # else:
        #     qspdt[my_id][action_id] = self.alpha_t * spdt_reward
        #
        # # print("post-update-> ", qspdt)
        return

    def update_qtables_last_hop(self, my_id, action_id, hc_reward, spdt_reward):
        qhc = self.qtable_hc
        qspdt = self.qtable_spdt
        # print("pre-update-> ", qspdt)
        if action_id not in qhc[my_id]:
            qhc[my_id][action_id] = self.alpha_h * hc_reward
            qspdt[my_id][action_id] = self.alpha_t * spdt_reward
        else:
            qhc[my_id][action_id] = (1 - self.alpha_h) * qhc[my_id][action_id] + self.alpha_h * hc_reward
            qspdt[my_id][action_id] = (1 - self.alpha_h) * qspdt[my_id][action_id] + self.alpha_t * spdt_reward

        # print("post-update-> ", qspdt)
        return

    @staticmethod
    def compute_reward_hc(n_hops, hop):
        return n_hops - hop - 5

    @staticmethod
    def compute_reward_spdt(total_delay, hop_delay):
        return ((total_delay - hop_delay) * config.TS_DURATION) - (20 * config.TS_DURATION)

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
            self.link_parameters[neigh] = self.update_link_param(hello_pck)

        # FUZZY LOGIC
        candidates = []
        for hello, neigh in opt_neighbors:
            action = neigh.identifier
            tr, es, fs = self.link_parameters[neigh][0], self.link_parameters[neigh][1], self.link_parameters[neigh][2]
            hc = None
            spdt = None
            if action in self.qtable_hc[state]:
                hc = self.qtable_hc[state][action]
                spdt = self.qtable_spdt[state][action]
            candidates.append((neigh, self.fuzzy_logic(tr, es, fs, hc, spdt)))

        # RELAY SELECTION
        relay = None
        cur_priority = -1
        for drone, priority in candidates:
            if priority > cur_priority:
                cur_priority = priority
                relay = drone

        return relay

    def update_link_param(self, hello_pck):

        tr = hello_pck.optional_data[1]

        b1, b2 = 0.5, 0.5
        rej = hello_pck.optional_data[0]  # residual energy of neigh
        if rej == 0:
            edr_j = 0
        else:
            edr_j = hello_pck.speed / rej  # config.DRONE_MAX_ENERGY  # energy drain rate of neigh computed based on the velocity
        ie = config.DRONE_MAX_ENERGY  # initial energy for all nodes
        es = b1 * (rej / ie) - b2 * edr_j

        vj = hello_pck.speed  # velocity of neigh
        pos_neigh = hello_pck.cur_pos
        next_pos_neigh = hello_pck.next_target
        J = self.simulator.depot_coordinates  # destination node, maybe next_pos_neigh?
        teta_i = util.angle_between_points(self.drone.coords, J, pos_neigh)
        teta_j = util.angle_between_points(pos_neigh, J, next_pos_neigh)
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
        tr_fuzz = "m" if tr < 0.1 else "h"
        es_fuzz = "l" if es < 6 else "h"
        fs_fuzz = "b" if fs < 5 else "g"
        if hc is not None:
            hc_fuzz = "sm" if hc < 10 else "lg"
            # print(hc_fuzz)
        if spdt is not None:
            spdt_fuzz = "sh" if spdt < 0.2 else "ln"
            #print(spdt_fuzz)
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