import networkx as nx
import json
from pyvis.network import Network
import os

class CareerGraph:
    def __init__(self):
        self.graph = nx.DiGraph() # Directed Graph

    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # 1. Add Roles as Nodes
        for role in data['roles']:
            # We add a custom color to roles so they stand out (blue)
            self.graph.add_node(role['title'], type="role", salary=role['salary_range'], desc=role['description'], color="#97C2FC", title=role['description'])
            
            # 2. Add Skills as Nodes and Connect to Role
            for skill in role['skills']:
                self.graph.add_node(skill, type="skill", color="#FFFF00", title="Skill") # Yellow for skills
                self.graph.add_edge(role['title'], skill, relation="requires")
            
            # 3. Add Prerequisites (Role depends on another Role or Skill)
            for prereq in role['prerequisites']:
                # Find the actual title if it's an ID
                found_role = next((r['title'] for r in data['roles'] if r['id'] == prereq), prereq)
                self.graph.add_node(found_role, type="concept", color="#FB7E81", title="Prerequisite") # Red/Pink for prereqs
                self.graph.add_edge(role['title'], found_role, relation="depends_on")

        # 4. Add Explicit Skill Relations
        for rel in data.get('skills_relations', []):
            self.graph.add_edge(rel['source'], rel['target'], relation=rel['relation'])

        print(f"Graph Built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges.")

    def get_neighbors(self, node_name):
        """Finds immediate connections (skills, prereqs) for a node."""
        if node_name in self.graph:
            return list(self.graph.neighbors(node_name))
        return []

    def get_role_details(self, role_name):
        if role_name in self.graph and self.graph.nodes[role_name].get('type') == 'role':
            return self.graph.nodes[role_name]
        return None

    def visualize(self, output_file="graph.html"):
        """Creates the Full Network Map."""
        # Create a visual network
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        
        # Convert NetworkX graph to PyVis
        net.from_nx(self.graph)
        
        # Add physics controls
        net.show_buttons(filter_=['physics'])
        
        try:
            net.save_graph(output_file)
            return output_file
        except Exception as e:
            print(f"Error saving graph: {e}")
            return None

    def visualize_path(self, center_node, output_file="graph_path.html"):
        """Creates a focused graph for just ONE career path (Ego Graph)."""
        
        # 1. Check if node exists (Case-insensitive matching)
        actual_node = next((n for n in self.graph.nodes if n.lower() == center_node.lower()), None)
        
        if not actual_node:
            print(f"Node '{center_node}' not found.")
            return None

        # 2. Create the Subgraph (The "Ego Graph")
        # radius=2 means: Show me the node, its neighbors, AND its neighbors' neighbors
        subgraph = nx.ego_graph(self.graph, actual_node, radius=2, undirected=True) 

        # 3. Visual Styling
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(subgraph)

        # Highlight the Central Node in Red so it stands out
        if actual_node in net.get_nodes():
            # PyVis nodes are dictionaries, we need to find the specific node dictionary in the list
            for node in net.nodes:
                if node['id'] == actual_node:
                    node['color'] = '#ff4b4b'  # Bright Red
                    node['size'] = 40
                    break

        net.show_buttons(filter_=['physics'])
        
        try:
            net.save_graph(output_file)
            return output_file
        except Exception as e:
            print(f"Error saving focused graph: {e}")
            return None