#!/usr/bin/env python3

import argparse
from collections import defaultdict, deque
from typing import Dict, Set, Optional, List

def find_shortest_path(graph, start_id, end_id):
    """
    Finds the shortest path between start_id and end_id using BFS.
    'graph' should be a dictionary where keys are IDs and values are lists of neighbor IDs.
    """
    if start_id == end_id:
        return [start_id]
    
    # Queue for BFS stores the current node being explored
    queue = deque([start_id])
    
    # parent maps a node to its 'predecessor' to reconstruct the path later
    # It also serves as our 'visited' set
    parent = {start_id: None}
    
    while queue:
        current_node = queue.popleft()
        
        # Look at all things this ID references (neighbors)
        neighbors = graph.get(current_node, [])
        
        for neighbor in neighbors:
            if neighbor not in parent:
                parent[neighbor] = current_node
                
                # Check if we found our target
                if neighbor == end_id:
                    return reconstruct_path(parent, start_id, end_id)
                
                queue.append(neighbor)
                
    return None  # No path exists
def reconstruct_path(parent: Dict[str, Optional[str]], start_id: str, end_id: str) -> List[str]:
    """
    Reconstructs the path from start_id to end_id using the parent mapping.
    """
    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

def build_parser():
    parser = argparse.ArgumentParser(
        prog="find_shortest_path",
        description="Find shortest path between two nodes (placeholder).",
    )
    parser.add_argument("start", type=str, help="Start node identifier")
    parser.add_argument("end", type=str, help="End node identifier")
    return parser

def load_graph() -> Dict[str, Set[str]]:
    """
    Placeholder function to load the graph data structure.
    In a real implementation, this would load from a database or file.
    Here, we return a dummy graph for demonstration.
    """
    import json
    # Load JSON data from file
    file_path = "graph.json"  # Replace with your actual file path
    graph_data = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                graph_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON line: {e}")
                continue
    relationship_map : Dict[str, Set[str]] = defaultdict(set)
    for item in graph_data:
        if item['type'] == 'relationship':
            start_id = item['start']['properties']['globalId']
            end_id = item['end']['properties']['globalId']
            relationship_map[start_id].add(end_id)

    return relationship_map

def main():
    parser = build_parser()
    args = parser.parse_args()
    # Placeholder: the user will fill in the processing logic here.
    print(f"finding path from start: {args.start} and end: {args.end}")

    graph = load_graph()
    print(f"loaded graph of size: {len(graph)}")
    path = find_shortest_path(graph, args.start, args.end)

    if path:
        print(f"Shortest path: {' -> '.join(path)}")
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
    exit(0)
    # Using sets for neighbors
    my_graph_map = {
        "node_A": {"node_B", "node_C"},
        "node_B": {"node_D"}
    }
    path = find_shortest_path(my_graph_map, "node_A", "node_D")
    print(path)

