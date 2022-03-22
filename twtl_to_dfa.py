from subprocess import check_output
import yaml
import networkx as nx

def old_nx_nodes(g):
    return list(iter(g.node.items()))

def old_nx_edges_iter(g):
    seen = {}     # helper dict to keep track of multiply stored edges
    nodes_nbrs = g.edge.items()
    for n, nbrs in nodes_nbrs:
        for nbr, ddict in nbrs.items():
            if nbr not in seen:
                yield (n, nbr, ddict)
        seen[n] = 1
    del seen

def old_nx_edges(g):
    return list(old_nx_edges_iter(g))

def twtl_to_dfa(formula, kind, norm=False, dont_optimize=False):

    # check args
    if kind not in ['normal', 'infinity', 'both']:
        raise ValueError(f'Valid options for argument "kind" are "normal", "infinity", or "both". Received "{kind}".')

    # get output serialized as yaml
    yaml_serialized_data = check_output(['./bin-linux/twtl_translate', formula, '--kind=' + kind], text=True)
    # with open('yaml_dump.yaml', "r") as f:
    #     data = f.read()

    # python 2 to 3 yaml convert
    yaml_serialized_data = yaml_serialized_data.replace('__builtin__', 'builtins')
    tup = yaml.unsafe_load(yaml_serialized_data)

    # Create a dictionary to hold the return values, rather than a tuple with possible ordering errors.
    return_dict = {'alphabet': tup[0]}

    # Rebuild nx 1 graphs for nx 2
    g1 = tup[1].g
    H1 = nx.DiGraph()
    H1.add_nodes_from(old_nx_nodes(g1))
    H1.add_edges_from(old_nx_edges(g1))

    if kind == 'both':
        g2 = tup[2].g
        H2 = nx.DiGraph()
        H2.add_nodes_from(old_nx_nodes(g2))
        H2.add_edges_from(old_nx_edges(g2))

        normal_dfa = tup[1]
        normal_dfa.g = H1
        return_dict['normal'] = normal_dfa
        inf_dfa = tup[2]
        inf_dfa.g = H2
        return_dict['infinity'] = inf_dfa

    else:
        # either normal or infinity
        kind_dfa = tup[1]
        kind_dfa.g = H1
        return_dict[kind] = kind_dfa

    if norm:
        return_dict['bounds'] = tup[-1]

    return return_dict

    # print(y)
# tup = yaml.safe_load(output)
# print(tup)

if __name__ == '__main__':
    d = twtl_to_dfa("[H^1 r2]^[0,10]", kind='both')
    print(d)