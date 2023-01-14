from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
import random


class QLearningRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone=drone, simulator=simulator)
        self.taken_actions = {}  # id event : (old_state, old_action)
        self.qtable = {}  # position : (relay : value)  , discretize the space in cells--> each position is a cell
        path = self.drone.path
        self.path_discretized = []
        for i in range(len(path)):
            cell = util.TraversedCells.coord_to_cell(size_cell=self.simulator.prob_size_cell,
                                                     width_area=self.simulator.env_width,
                                                     x_pos=path[i][0],
                                                     y_pos=path[i][1])[0]
            self.path_discretized.append(cell)

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

            state, action, next_target = self.taken_actions[id_event]

            # remove the entry, the action has received the feedback
            del self.taken_actions[id_event]

            """ CALCULATE THE MAX NEXT VALUE OF Q-TABLE"""
            if next_target in self.qtable:
                best_next_drone = max(self.qtable[next_target], key=self.qtable[next_target].get)
                max_next = self.qtable[next_target][best_next_drone]
            else:
                max_next = 0

            """ UPDATE THE Q-TABLE"""
            reward = outcome * (2000 / delay)
            a, y = 0.2, 0.8
            if state in self.qtable:
                if action in self.qtable[state]:  # we already know something about the action taken
                    self.qtable[state][action] = self.qtable[state][action] + a * (
                            reward + y * max_next - self.qtable[state][action])
                else:  # we don't know anything about the action taken
                    self.qtable[state][action] = a * (reward + y * max_next)
            else:  #
                self.qtable[state] = {}
                self.qtable[state][action] = a * (reward + y * max_next)

    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.

        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """

        cell_index = self.get_cell(self.drone.coords)
        relay = None
        cur_pos = cell_index
        neighs = [d for hello, d in opt_neighbors]

        e = random.random()
        if e < 0.95:  # greedy case
            if cur_pos in self.qtable:
                relay = max(self.qtable[cur_pos], key=self.qtable[cur_pos].get)
                if relay not in neighs:  # the relay could not be in the neighbours
                    relay = self.select_best_neigh(opt_neighbors)
                    self.simulator.exploitation[1] += 1
                else:
                    self.simulator.exploitation[0] += 1
            else:
                self.simulator.exploitation[1] += 1
                relay = self.select_best_neigh(
                    opt_neighbors)  # choose the best relay based on the neighbours properties
        else:  # exploration case
            self.simulator.exploration += 1
            relay = random.choice(neighs)

        state, action = cur_pos, relay
        next_target = self.get_cell(self.drone.next_target())
        self.taken_actions[packet.event_ref.identifier] = (state, action, next_target)
        return relay

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
