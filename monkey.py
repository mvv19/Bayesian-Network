# Maria Vega Vazquez
# AI Project 3: Monkey Business
# I have neither given nor received unauthorized help on this program

from decimal import Decimal, ROUND_HALF_UP


# class for Location just to treat it as an object (makes referencing easier)
class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loc = (x, y)

    def to_string(self):
        return print(self.loc)


class LastLocation(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dist(self, m, n, debug):
        if debug:
            print("Last location distribution:")
        last_loc = {}
        rows = int(m)
        cols = int(n)

        for i in range(int(m)):
            for j in range(int(n)):
                loc = Location(i, j)  # (r,c)
                p = 1 / (rows * cols)  # P(L=(r,c))=1/m⋅n
                last_loc[loc.loc] = Decimal(p).quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)

                if debug:
                    print("Last location: ", loc.loc, "prob:", p)

                    print()
        return last_loc


class CurrentLocation(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.c_prob = {}

    def get_dist(self, loc, m, n, debug):
        if debug:
            print("Current Location Distribution")

        # retrieves the whole distribution, given a specific setting for the parent variable(s)
        adj_locs = locationsOneManhattan(loc, m, n)  # gets the possible neighbors from the man dist

        #   print(adj_locs)
        for loc in adj_locs:
            probability = Decimal(1 / len(adj_locs))
            #   print(f"The curr loc is {loc} and the probability is {probability}")
            self.c_prob[loc] = probability.quantize(Decimal('1e-8'),
                                                      rounding=ROUND_HALF_UP)  # put down the curr location too

            if debug:
                print("Current location: ", loc, "prob: ", probability)

        all_locs = allLocations(m, n)

        for loc in all_locs:
            if loc not in self.c_prob:
                self.c_prob[loc] = Decimal(0)  # 0 probability for places on the board it cannot touch

        #   print(f"THE CURR VALS ARE {self.c_prob}")
        return self.c_prob

    def get_prob(self, currLoc, lastLoc, m, n, debug):
        #  retrieves just a single probability from the distribution, given a specific setting for the
        #  parent variable and the setting of the variable in question.

        probabilities = self.get_dist(lastLoc, m, n, debug)
        # print("debug for currLoc", probabilities[currLoc])
        prob = probabilities.get(currLoc.loc)

        return prob


class MotionSensors(object):
    # binary T or F
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    # all distributions
    # each sensor detects the monkey with a probability equal to
    # 0.9 minus 0.1 ⋅ (the number of steps away from the sensor the monkey is).
    def get_dist(self, sensorB, ms: Location, m, n, debug):
        all_locs = allLocations(m, n)
        motionsensors = {}
        ms1 = {}
        ms2 = {}

        m = int(m)
        n = int(n)

        for currloc in all_locs:
            # print(currloc)
            x = currloc[0]
            y = currloc[1]
            curr_loc = Location(x, y)

            # if the monkey is within the radius of m1 (0,0)
            if ms.x == 0 and ms.y == 0:
                prob = self.get_dist_m1(curr_loc, sensorB)
                ms1[curr_loc] = prob.quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)

            elif ms.x == m - 1 and ms.y == n - 1:
                prob = self.get_dist_m2(curr_loc, sensorB, m, n)
                ms2[curr_loc] = prob.quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)

            motionsensors[curr_loc.loc] = prob.quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)

        if debug:
            print("Motion sensor #1 (top left) distribution")
            self.print_probability(ms1)
            print("Motion sensor #2 (bottom right) distribution")
            self.print_probability(ms2)

            print()
        return motionsensors

    def get_dist_m1(self, curr_loc, b):
        if curr_loc.x == 0 or curr_loc.y == 0:
            prob = Decimal(0.9 - (0.1 * max(curr_loc.x, curr_loc.y))).quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)

        else:
            prob = Decimal(0.95) if not b else Decimal(0.05)
        return prob

    def get_dist_m2(self, curr_loc, b, m, n):
        if curr_loc.x == m - 1 or curr_loc.y == n - 1:
            prob = Decimal(0.9 - (0.1 * max(m - 1 - curr_loc.x, n - 1 - curr_loc.y))).quantize(Decimal('1e-8'),
                                                                                               rounding=ROUND_HALF_UP)

        else:
            prob = Decimal(0.05)

        if not b:
            prob = 1 - prob
        return prob

    def print_probability(self, ms_dict):
        for loc in ms_dict:
            prob = ms_dict[loc]
            print(f"Current location:  {loc.loc}, true probability: {prob:.8f}, false probability: {1 - prob:.8f}")

    # singular one for C
    def get_prob_m1(self, currLoc, b, m, n, debug):
        ms = Location(0, 0)
        probM1 = self.get_dist(b, ms, m, n, debug).get(currLoc)
        return probM1

    def get_prob_m2(self, currLoc, b, m, n, debug):
        m = int(m)
        n = int(n)
        ms = Location(m - 1, n - 1)
        probM2 = self.get_dist(b, ms, m, n, debug).get(currLoc)
        return probM2


class SoundSensor(object):
    def get_dist(self, currLoc, m, n, debug):
        sound_locs = {}
        all_locs = allLocations(m, n)
        neighbors = locationsOneManhattan(currLoc, m, n)
        neighbors2 = locationsTwoManhattan(currLoc, m, n)

        prob0 = 0.6
        sound_locs[currLoc] = Decimal(prob0).quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)  # 60% correct

        if debug:
            print(f"Sound reported at: , {currLoc}, prob: , {prob0:.8f}")

        for neighbor in neighbors:
            prob = 0.3 / len(neighbors)
            prob = Decimal(prob).quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)

            sound_locs[neighbor] = prob  # 30% correct for 1 Manhattan distance
            if debug:
                print(f"Sound reported at: , {neighbor}, prob: , {prob:.8f}")

        for neighbor in neighbors2:
            prob2 = .1 / len(neighbors2)
            prob2 = Decimal(prob2).quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)
            sound_locs[neighbor] = prob2  # 10% correct for 2 Manhattan distances

            if debug:
                print(f"Sound reported at: , {neighbor}, prob: , {prob:.8f}")

        for loc in all_locs:
            if loc not in sound_locs:
                sound_locs[loc] = Decimal(0)  # 0 probability for places on the board it cannot touch

                if debug:
                    print(f"Sound reported at: , {loc}, prob: , {prob:.8f}")

        return sound_locs

    def get_prob(self, currLoc, soundLoc, m, n, debug):
        prob = self.get_dist(currLoc, m, n, debug).get(soundLoc.loc)
        return prob


def allLocations(rows, cols):
    allLoc = []
    for r in range(int(rows)):
        for c in range(int(cols)):
            loc = Location(int(r), int(c))
            allLoc.append(loc.loc)
            #   print("r", r, "c", c, "loc", loc.loc, "all locs", allLoc)
    return allLoc


def locationsOneManhattan(currLoc, rows, cols):
    x = currLoc[0]
    y = currLoc[1]
    oneMLoc = []

    if x + 1 < int(cols):
        loc = Location(x + 1, y)
        oneMLoc.append(loc.loc)
    if y + 1 < int(rows):
        loc = Location(x, y + 1)
        oneMLoc.append(loc.loc)
    if x - 1 >= 0:
        loc = Location(x - 1, y)
        oneMLoc.append(loc.loc)
    if y - 1 >= 0:
        loc = Location(x, y - 1)
        oneMLoc.append(loc.loc)

    #   print(oneMLoc)
    return oneMLoc


def locationsTwoManhattan(currLoc, rows, cols):
    twoMLoc = []
    x = currLoc[0]
    y = currLoc[1]
    row = int(rows)
    col = int(cols)

    if x + 1 < col and y + 1 < row:
        loc = Location(x + 1, y + 1)
        twoMLoc.append(loc.loc)
    if x - 1 >= 0 and y - 1 >= 0:
        loc = Location(x - 1, y - 1)
        twoMLoc.append(loc.loc)
    if x + 1 < col and y - 1 >= 0:
        loc = Location(x + 1, y - 1)
        twoMLoc.append(loc.loc)
    if x - 1 >= 0 and y + 1 < row:
        loc = Location(x - 1, y + 1)
        twoMLoc.append(loc.loc)
    if x + 2 < col:
        loc = Location(x + 2, y)
        twoMLoc.append(loc.loc)
    if x - 2 >= 0:
        loc = Location(x - 2, y)
        twoMLoc.append(loc.loc)
    if y + 2 < row:
        loc = Location(x, y + 2)
        twoMLoc.append(loc.loc)
    if y - 2 >= 0:
        loc = Location(x, y - 2)
        twoMLoc.append(loc.loc)

    # print(twoMLoc)
    return twoMLoc


def main():
    file_input = input("Please enter the file you'd like to read: ")
    debug_opt = input("Debugger? (Y/N)").upper()
    #   debug_opt = 'Y'

    if debug_opt == 'Y':
        debug = True
    elif debug_opt == 'N':
        debug = False

    # open the file for reading
    with open(file_input, 'r') as file:
        # Read the first line to get the dimensions
        m, n = file.readline().split()

        #   print("Possible last locations: ", last_locations)

        print("Initial distribution of monkey's last location:")
        for i in range(int(m)):
            for j in range(int(n)):
                # creates an obj to get the dictionary of L (Last Location)
                lastloc = LastLocation(m, n)
                last_locations = lastloc.get_dist(m, n, debug)
                print(f"{last_locations}")
        print()

        alpha = Decimal(0)
        timestep = 0

        for line in file:
            line = line.strip().split()
            m1_val = line[0]
            m2_val = line[1]

            # creates the boolean variables for the motion sensors
            if m1_val == '1':
                m1 = True
            else:
                m1 = False
            if m2_val == '1':
                m2 = True
            else:
                m2 = False

            # creates a location object for where the sound sensor is
            sound_x = int(line[2])
            sound_y = int(line[3])
            sound_loc = Location(sound_x, sound_y)

            # confirm it matches with the txt
            print(f"\nObservation: , Motion1: , {m1}, Motion2: , {m2}, Sound location: , {sound_loc.loc}")
            print(f"Monkey's predicted current location at time step: {timestep}")

            # # list of all possible locations on the board
            all_locations = allLocations(m, n)
            #   print("All possible locations: ", all_locations)

            # creates an M1 and M2 object to get their respective probabilities
            ms = MotionSensors(m1, m2)
            #   print("Motion sensors are: ", ms.m1, ms.m2)

            # dictionary for the probabilities of the current value
            probabilities = {}

            #  iterates over all possible locations in the board
            for curr_loc in all_locations:
                total_prob = Decimal(0)

                if debug:
                    print(f"\nCalculating total prob for current location {curr_loc}: ")

                for last_loc in last_locations.keys():
                    last_prob = last_locations[last_loc]

                    curr = Location(curr_loc[0], curr_loc[1])
                    currentLocation = CurrentLocation(curr.x, curr.y)
                    C_prob = currentLocation.get_prob(curr, last_loc, m, n, debug)

                    ms1_prob = ms.get_prob_m1(curr_loc, m1, m, n, debug)
                    ms2_prob = ms.get_prob_m2(curr_loc, m2, m, n, debug)

                    sound = SoundSensor()
                    sound_prob = sound.get_prob(curr_loc, sound_loc, m, n, debug)

                    prob_product = last_prob * C_prob * ms1_prob * ms2_prob * sound_prob

                    if debug:
                        print(f"Probabilities being multiplied for last location {last_loc}: "
                              f"{last_prob} {C_prob} {ms1_prob} {ms2_prob} {sound_prob}")
                    total_prob += prob_product

                alpha += total_prob
                probabilities[curr_loc] = total_prob

            if debug:
                print("\nBefore normalization:")
                print(probabilities.values())

            normalized_probabilities = {}
            for i in range(int(m)):
                for j in range(int(n)):
                    loc = Location(i, j)
                    temp = loc.loc
                    temp_prob = Decimal(str(probabilities[temp]))

                    normalized_probability = temp_prob / alpha
                    normalized_probability = normalized_probability.quantize(Decimal('1e-8'), rounding=ROUND_HALF_UP)
                    normalized_probabilities[temp] = normalized_probability

                    #   print("The normalized probability for", temp, "is", normalized_probability)

            if debug:
                print("\nAfter normalization:")
            print(normalized_probabilities.values())

            timestep += 1


main()
