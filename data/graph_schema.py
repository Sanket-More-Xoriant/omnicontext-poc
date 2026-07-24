class GraphNode:

    def __init__(
        self,
        node_id,
        node_type,
        properties=None
    ):
        self.id = node_id
        self.type = node_type
        self.properties = properties or {}

    def __repr__(self):

        return f"{self.type}({self.id})"


class GraphEdge:

    def __init__(
        self,
        source,
        target,
        relationship
    ):
        self.source = source
        self.target = target
        self.relationship = relationship

    def __repr__(self):

        return (
            f"{self.source} "
            f"-[{self.relationship}]-> "
            f"{self.target}"
        )


class KnowledgeGraph:

    def __init__(self):

        self.nodes = {}

        self.edges = []

    def add_node(
        self,
        node
    ):

        self.nodes[node.id] = node

    def add_edge(
        self,
        edge
    ):

        self.edges.append(edge)

    def print_graph(self):

        print("\nNODES:")
        print("-" * 50)

        for node in self.nodes.values():

            print(node)

        print("\nEDGES:")
        print("-" * 50)

        for edge in self.edges:

            print(edge)

    def get_imports(
        self,
        file_name
    ):

        imports = []

        for edge in self.edges:

            if (
                edge.source == file_name
                and edge.relationship == "IMPORTS"
            ):

                imports.append(
                    edge.target
                )

        return imports