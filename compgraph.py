import networkx as nx
import itertools

import utils


class Variable:
    node_counter = itertools.count()

    def __init__(self, value, G=None):
        self.value = str(value)
        self._id = next(Variable.node_counter)
        self._G = G or nx.MultiDiGraph()
        self._G.add_node(self._id)
        self._labels = {self._id: self.value}

    def graph(self):
        for layer, nodes in enumerate(nx.topological_generations(self._G)):
            for node in nodes:
                self._G.nodes[node]["layer"] = layer

        pos = nx.multipartite_layout(self._G, subset_key="layer")
        nx.draw_networkx_labels(self._G, pos, self._labels)
        for edge in self._G.edges(data=True):
            nx.draw_networkx_edges(self._G, pos, edgelist=[(edge[0], edge[1])],
                                   connectionstyle=f'arc3, rad = {edge[2]["rad"]}')


    def compose(self, value, other):
        var = Variable(value, G=nx.compose(self._G, other.G))
        utils.new_add_edge(var._G, self._id, var._id)
        utils.new_add_edge(var._G, other._id, var._id)
        var._labels.update(self._labels)
        var._labels.update(other._labels)
        return var

    def compute(self, value):
        var = Variable(value, G=self._G)
        utils.new_add_edge(self._G, self._id, var._id)
        var._labels.update(self._labels)
        return var

    def __add__(self, other):
        return self.compose("+", other)

    def __sub__(self, other):
        return self.compose("-", other)

    def __mul__(self, other):
        return self.compose("*", other)

    def __truediv__(self, other):
        return self.compose("/", other)

    def __pow__(self, power, modulo=None):
        return self.compose("**", power)

def sqrt(x: Variable):
    return x.compute("√")


def ln(x: Variable):
    return x.compute("ln")


def exp(x: Variable):
    return x.compute("exp")


def cos(x: Variable):
    return x.compute("cos")


def sin(x: Variable):
    return x.compute("sin")
