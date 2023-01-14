import random
from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util


class NEW_QLearningRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone=drone, simulator=simulator)
        self.taken_actions = {}  # id event : (old_state, old_action)
        self.qtable = {}  # set_of_neighbours : (relay : value)

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

        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple
        # feedback for the same packet!!

        if id_event in self.taken_actions:
            # BE AWARE, IMPLEMENT YOUR CODE WITHIN THIS IF CONDITION OTHERWISE IT WON'T WORK!
            # TIPS: implement here the q-table updating process

            # Drone id and Taken actions
            # print(f"\nIdentifier: {self.drone.identifier}, Taken Actions: {self.taken_actions}, Time Step: {self.simulator.cur_step}")

            # feedback from the environment
            # print(drone, id_event, delay, outcome)

            state, action = self.taken_actions[id_event]
            del self.taken_actions[id_event]

            """COMPUTE NEXT-STATE"""
            max_next = 0
            if self.qtable != {}:
                # we cannot calculate the next state, so we estimate it randomly, if it's not possibile we consider 0
                pseduo_next_state = random.choice(list(self.qtable.keys()))
                if self.qtable[pseduo_next_state] != {}:
                    pseudo_best_drone = max(self.qtable[pseduo_next_state], key=self.qtable[pseduo_next_state].get)
                    max_next = self.qtable[pseduo_next_state][pseudo_best_drone]

            """UPADTE Q_TABLE"""
            reward = outcome * (2000 / delay)
            a, y = 0.8, 0.2
            if state in self.qtable:
                if action in self.qtable[state]:
                    self.qtable[state][action] += a * (reward + y * max_next - self.qtable[state][action])
                else:
                    self.qtable[state][action] = a * (reward + y * max_next)
            else:
                self.qtable[state] = {}
                self.qtable[state][action] = a * (reward + y * max_next)

    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.
        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """

        neighs = [d for hello, d in opt_neighbors]
        state = frozenset(neighs)  # frozenset because we need some set operations
        e = random.random()
        if e < 0.95:  # greedy case
            if state in self.qtable:
                relay = max(self.qtable[state], key=self.qtable[state].get)
                self.simulator.exploitation[0] += 1

            # search if we already have some information about the neighbours
            elif state not in self.qtable and self.qtable != {}:
                # candidate: the  state (as set) intersected with cover_candidate
                # cover_candidate: the greater key in self.qtable that covers candidate
                candidate, cover_candidate = self.get_cover_candidate_and_candidate(state)

                if len(candidate) == 0:  # any info known about current neighbours
                    relay = self.select_best_neigh(opt_neighbors)
                    self.simulator.exploitation[1] += 1

                else:  # some neighbours are already known in the Q-Table
                    relay = None
                    relay_sorted = sorted(self.qtable[cover_candidate].items(), key=lambda x: x[1])
                    for i in range(len(relay_sorted)):
                        if relay_sorted[i][0] in candidate:
                            relay = relay_sorted[i][0]
                            self.simulator.exploitation[0] += 1
                            break  # being relay_sorted sorted we break immediately, because first we find it, higher is its value

                    if relay is None:  # means that the relay belongs to cover_key\candidate , thus it is not in the current neighbours
                        self.simulator.exploitation[1] += 1
                        relay = self.select_best_neigh(opt_neighbors)

            else:  # self.qtable = {}
                relay = self.select_best_neigh(opt_neighbors)
                self.simulator.exploitation[1] += 1

        else:  # exploration case
            self.simulator.exploration += 1
            relay = random.choice(neighs)

        action = relay
        self.taken_actions[packet.event_ref.identifier] = (state, action)
        return relay

    def select_best_neigh(self, opt_neighbours): # select the fastest drone that could reach the depeot
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

    def get_cover_candidate_and_candidate(self, state):
        candidate = frozenset()
        cover_candidate = frozenset()
        for key in self.qtable:
            tmp = state.intersection(key)
            if len(tmp) > len(candidate):
                candidate = state.intersection(key)
                cover_candidate = key
        return candidate, cover_candidate
