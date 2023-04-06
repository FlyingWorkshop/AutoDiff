import itertools
import networkx as nx

import utils


class Variable:
    # TODO: maintain a list of input variables to help take the Jacobian
    input_id = itertools.count(0, -1)  # v_0, v_{-1}, v_{-2}, ...
    intermediate_id = itertools.count(1)  # v_1, v_2, ...

    def __init__(self, value, is_input=True, G=None):
        self.value = value
        self.primal = 0
        self.tangent = 0
        self._id = next(Variable.input_id) if is_input else next(Variable.intermediate_id)
        self.inputs = {self} if is_input else set()
        self.G = G or nx.MultiDiGraph()
        self.G.add_node(self._id)
        self._labels = {self._id: self.value}

    def draw_computational_graph(self):
        for layer, nodes in enumerate(nx.topological_generations(self.G)):
            for node in nodes:
                self.G.nodes[node]["layer"] = layer

        pos = nx.multipartite_layout(self.G, subset_key="layer")
        nx.draw_networkx_labels(self.G, pos, self._labels)
        for edge in self.G.edges(data=True):
            nx.draw_networkx_edges(self.G, pos, edgelist=[(edge[0], edge[1])],
                                   connectionstyle=f'arc3, rad = {edge[2]["rad"]}')


    def compose(self, value, other):
        var = Variable(value, G=nx.compose(self.G, other.G), is_input=False)
        utils.new_add_edge(var.G, self._id, var._id)
        utils.new_add_edge(var.G, other._id, var._id)
        var.inputs.update(other.inputs)
        var.inputs.update(self.inputs)
        var._labels.update(self._labels)
        var._labels.update(other._labels)
        return var

    def compute(self, value):
        var = Variable(value, G=self.G, is_input=False)
        utils.new_add_edge(self.G, self._id, var._id)
        var.inputs.update(self.inputs)
        var._labels.update(self._labels)
        return var

    def __hash__(self):
        return hash(self._id)

    def __repr__(self):
        return f"<autodiff.Variable value={self.value}>"

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

