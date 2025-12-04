class HybridRetriever:
    def __init__(self, graph_builder, vector_store):
        self.graph = graph_builder
        self.vector = vector_store

    def retrieve(self, query):
        # 1. Vector Search: Find relevant roles based on user description
        docs = self.vector.search(query)
        context_parts = []

        # 2. Graph Enhancement: For every role found, get its specific graph details
        for doc in docs:
            role_title = doc.metadata['title']
            context_parts.append(f"Found Role: {role_title}")
            context_parts.append(f"Description: {doc.page_content}")
            
            # Query the Graph for specific connections
            neighbors = self.graph.get_neighbors(role_title)
            role_details = self.graph.get_role_details(role_title)
            
            if role_details:
                context_parts.append(f"  - Salary: {role_details.get('salary', 'N/A')}")
            
            if neighbors:
                context_parts.append(f"  - Requires/Related to: {', '.join(neighbors)}")

        return "\n".join(context_parts)