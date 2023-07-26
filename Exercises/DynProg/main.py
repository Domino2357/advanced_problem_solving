"""
Solution to the bridge crossing problem
Basic assumptions:
1. always two people cross on the first move and one returns
2. the fastest one on the right side is always the one returning

Please note, the solution returns one time step too much, i.e., the fastest person in the last step does one last move
"""

speeds = {'a': 1, 'b': 2, 'c': 5, 'd': 10}


def crossing_step(current_states):
    new_states = []
    for state in current_states:
        (l, r, time, crossing_order) = state
        # first two walk
        second_it = len(l)
        for h in range(len(l)):
            for j in range(second_it):
                if h != j:
                    first = l[h]
                    second = l[j]
                    new_left = list(l)
                    new_left.remove(first)
                    new_left.remove(second)
                    new_right = list(r) + [first, second]
                    time += max(speeds[first], speeds[second])
                    new_right.sort(key=return_speed)
                    fastest_person = new_right[0]
                    time += speeds[fastest_person]
                    new_right.remove(fastest_person)
                    new_left.append(fastest_person)
                    iter_length = len(new_states)
                    if not new_states:
                        new_states.append((new_left, new_right, time, list(crossing_order) + [first, second, fastest_person]))
                    else:
                        appended = False
                        for k in range(iter_length):
                            (inter_left, inter_right, inter_time, inter_order) = new_states[k]
                            if inter_right == new_right:
                                appended = True
                                if time < inter_time:
                                    new_states[k] = (new_left, new_right, time, list(crossing_order) +
                                                     [first, second, fastest_person])
                        if not appended:
                            new_states.append(
                                    (new_left, new_right, time, list(crossing_order) + [first, second, fastest_person]))
            second_it -= 1
    return new_states


def return_speed(person):
    return speeds[person]


def return_time(state):
    return state[3]


if __name__ == '__main__':

    left = list(speeds.keys())
    right = []
    states = [(left, right, 0, [])]
    # cross as long as there are people on the left side
    while len(states[0][0]) > 1:
        states = crossing_step(states)
    # print fastest configuration
    states.sort(key=return_time)
    # solution is strictly speaking wrong as the last person does one last step
    print((states[0][2], states[0][3]))
