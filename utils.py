def new_add_edge(G, a, b):
    """
    Source: https://stackoverflow.com/questions/60067022/multidigraph-edges-from-networkx-draw-with-connectionstyle
    """
    if (a, b) in G.edges:
        max_rad = max(x[2]['rad'] for x in G.edges(data=True) if sorted(x[:2]) == sorted([a,b]))
    else:
        max_rad = 0
    G.add_edge(a, b, rad=max_rad+0.1)