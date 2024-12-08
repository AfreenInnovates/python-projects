import networkx as nx
import matplotlib.pyplot as plt

def visualize_notes(notes):
    graph = nx.Graph()
    for note in notes:
        graph.add_node(note["title"], category=note["category"])

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue')
    plt.show()
