import random

'''
Vertices are the words in the graph. Every vertex has an edge 
(like a bridge that leads to the following word). These edges have weights 
which are determined by how much those vertices follow each other.

'''
class Vertex:
    def __init__(self, value):
        self.value = value
        self.adjacent = {}
        self.neighbors = []
        self.neighbor_weights = []

    def add_edge_to(self, vertex, weight=0):
        self.adjacent[vertex] = weight
    
    def increment_edge(self, vertex):
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():
            self.neighbors.append(vertex)
            self.neighbor_weights.append(weight)

    def next_word(self):
        return random.choices(self.neighbors, weights = self.neighbor_weights)[0]


class Graph:
    def __init__(self):
        self.vertices = {}

    def get_vertex_values(self):
        return set(self.vertices.keys())

    def add_vertex(self, value):
        self.vertices[value] = Vertex(value)

    def get_vertex(self, value):
        if value not in self.vertices:
            self.add_vertex(value)
        return self.vertices[value]

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()
