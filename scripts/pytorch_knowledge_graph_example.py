import json
import torch
from torch_geometric.data import HeteroData
from collections import defaultdict

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

# Initialize HeteroData object
data = HeteroData()

# Mapping for node indices per node type
node_mappings = defaultdict(dict)

# Temporary storage for properties to reduce concatenation cost
node_properties = defaultdict(lambda: defaultdict(list))
edge_indices = defaultdict(lambda: defaultdict(list))

# Process each item in the loaded JSON data
for item in graph_data:
    if item['type'] == 'node':
        node_type = item['labels'][0]  # Assuming first label is the node type
        node_id = item['id']
        properties = item['properties']

        # Store the node index mapping
        node_index = len(node_mappings[node_type])
        node_mappings[node_type][node_id] = node_index

        # Store properties temporarily by type
        for key, value in properties.items():
            if isinstance(value, list) and all(isinstance(v, (int, float)) for v in value):
                node_properties[node_type][key].append(torch.tensor(value, dtype=torch.float))
            elif isinstance(value, (int, float)):
                node_properties[node_type][key].append(torch.tensor([value], dtype=torch.float))
            else:
                node_properties[node_type][key].append(value)  # non-numeric properties as lists

    elif item['type'] == 'relationship':
        start_type = item['start']['labels'][0]
        end_type = item['end']['labels'][0]
        start_id = item['start']['id']
        end_id = item['end']['id']
        edge_type = item['label']

        # Map start and end node indices
        start_idx = node_mappings[start_type][start_id]
        end_idx = node_mappings[end_type][end_id]

        # Append to edge list
        edge_indices[(start_type, edge_type, end_type)]['start'].append(start_idx)
        edge_indices[(start_type, edge_type, end_type)]['end'].append(end_idx)

# Finalize node properties by batch processing
for node_type, properties in node_properties.items():
    data[node_type].num_nodes = len(node_mappings[node_type])
    for key, values in properties.items():
        if isinstance(values[0], torch.Tensor):
            data[node_type][key] = torch.stack(values)
        else:
            data[node_type][key] = values  # Keep non-tensor properties as lists

# Finalize edge indices in bulk
for (start_type, edge_type, end_type), indices in edge_indices.items():
    edge_index = torch.tensor([indices['start'], indices['end']], dtype=torch.long)
    data[start_type, edge_type, end_type].edge_index = edge_index

# Display statistics for verification
print("Nodes and Properties:")
for node_type in data.node_types:
    print(f"\nNode Type: {node_type}")
    print(f"Number of Nodes: {data[node_type].num_nodes}")
    for key, value in data[node_type].items():
        if key != 'num_nodes':
            if isinstance(value, torch.Tensor):
                print(f"  - {key}: {value.shape}")
            else:
                print(f"  - {key}: {len(value)} items (non-numeric)")

print("\nEdges and Types:")
for edge_type in data.edge_types:
    edge_index = data[edge_type].edge_index
    print(f"Edge Type: {edge_type} - Number of Edges: {edge_index.size(1)} - Shape: {edge_index.shape}")