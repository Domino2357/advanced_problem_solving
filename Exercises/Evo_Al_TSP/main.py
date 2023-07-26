import random


def evol_algorithm(g):
    (vert, edg) = g
    # needed for upper bound on the cost of the TSP path
    max_cost = max(list(edg.values())) * len(list(edg.values()))
    generation = initial_population(g, 5, max_cost)
    best_sol = []
    for i in range(100):
        generation = create_new_gen(generation, edg, max_cost)
        if i == 0:
            best_sol = generation[-1]
        else:
            if best_sol[1] > generation[0][1]:
                best_sol = generation[0]
    return best_sol


def eval_path(path, e, max_cost):
    cost = 0
    no_edges_count = 0
    complete_path = list(path)
    for i in range(len(complete_path)):
        edge_in_g = False
        if i == len(complete_path) - 1:
            # start at the beginning
            step = (complete_path[-1], complete_path[0])
        else:
            step = (complete_path[i], complete_path[i + 1])
        for key in e:
            if step == key:
                edge_in_g = True
                cost += e[key]
        if not edge_in_g:
            no_edges_count += 1
            cost += max_cost / no_edges_count
    return cost


def initial_population(g, length, max_cost):
    (v, e) = g
    init_pop = []
    path = [x for x in range(1, len(v) + 1)]
    init_pop.append((path, eval_path(path, e, max_cost)))
    for i in range(length - 1):
        new = list(path)
        random.shuffle(new)
        init_pop.append((new, eval_path(new, e, max_cost)))
    init_pop.sort(key=second_element)
    return init_pop


def create_new_gen(generation, e, max_cost):
    parents = choose_parents(generation)
    new_gen = list(generation)
    for pair in parents:
        (mother1, mother2) = pair
        daughter = mutate_swap(recombine_ordinal(mother1[0], mother2[0]))
        fitness = eval_path(daughter, e, max_cost)
        new_gen.append((daughter, fitness))
    new_gen.sort(key=second_element)
    # survival of the fittest should be probabilistic, but I 'm to lazy atm
    return new_gen[:len(generation)]


def second_element(t):
    return t[1]


def choose_parents(generation):
    parents = []
    # arbitrary choice: at most 50 percent of population mates
    length = int(len(generation) * 0.5)
    for i in range(length):
        parents.append((generation[i], generation[i + 1]))
    return parents


def recombine_ordinal(permutation_1, permutation_2):
    # take the first half from one and the second half from the other
    ordinal1 = enc_ordinal_permutation(permutation_1)
    ordinal2 = enc_ordinal_permutation(permutation_2)
    length1 = int(len(ordinal1) / 2)
    length2 = len(ordinal1)
    child1 = []
    for i in range(length1):
        child1.append(ordinal1[i])
    for j in range(length1, length2):
        child1.append(ordinal2[j])
    return dec_ordinal_permutation(child1)


def mutate_swap(permutation):
    mutated_per = list(permutation)
    rand_index1 = random.randint(0, len(permutation) - 1)
    rand_index2 = random.randint(0, len(permutation) - 1)
    mutated_per[rand_index1] = permutation[rand_index2]
    mutated_per[rand_index2] = permutation[rand_index1]
    return mutated_per


def enc_ordinal_permutation(permutation):
    order = [i for i in range(len(permutation) + 1)]
    ordinal = []
    for number in permutation:
        iter_length = len(order)
        for i in range(iter_length):
            if number == order[i]:
                ordinal.append(i)
                del order[i]
                break
    return ordinal


def dec_ordinal_permutation(ordinal):
    order = [i for i in range(len(ordinal) + 1)]
    permutation = []
    for i in ordinal:
        permutation.append(order[i])
        del order[i]
    return permutation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    vertices = [1, 2, 3, 4, 5]
    edges = {(1, 2): 2, (2, 1): 2, (1, 4): 3, (4, 1): 3, (1, 5): 6, (5, 1): 6, (2, 3): 4, (3, 2): 4, (2, 4): 3,
             (4, 2): 3, (3, 4): 7, (4, 3): 7, (3, 5): 3, (5, 3): 3, (4, 5): 3, (5, 4): 3}
    graph = (vertices, edges)
    hamiltonian = evol_algorithm(graph)
    print(hamiltonian)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
