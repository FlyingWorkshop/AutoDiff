import networkx as nx
import matplotlib.pyplot as plt
import itertools

import utils


class Variable:
    node_counter = itertools.count()
    edge_counter = itertools.count()

    def __init__(self, value, id=None, G=None):
        self.value = str(value)
        self._id = id or next(Variable.node_counter)
        self._G = G or nx.MultiDiGraph()
        self._G.add_node(self._id)
        self._labels = {self._id: self.value}

        # self.id = next(Variable.node_counter)
        # self.labels = {self.id: value}
        # self.G = nx.MultiDiGraph()
        # for inp in inputs or []:
        #     assert isinstance(inp, Variable)
        #     self.G = nx.compose(self.G, inp.G)
        #     utils.new_add_edge(self.G, inp.id, self.id)
        #     self.labels.update(inp.labels)
    def graph(self):
        pos = nx.spring_layout(self._G)
        nx.draw_networkx_labels(self._G, pos, self._labels)
        for edge in self._G.edges(data=True):
            nx.draw_networkx_edges(self._G, pos, edgelist=[(edge[0], edge[1])],
                                   connectionstyle=f'arc3, rad = {edge[2]["rad"]}')

    def compose(self, value, other):
        id = next(Variable.node_counter)
        G = nx.compose(self._G, other._G)
        utils.new_add_edge(G, self._id, id)
        utils.new_add_edge(G, other._id, id)
        var = Variable(value, id, G)
        var._labels.update(self._labels)
        var._labels.update(other._labels)
        return var

    def __add__(self, other):
        return self.compose("+", other)
