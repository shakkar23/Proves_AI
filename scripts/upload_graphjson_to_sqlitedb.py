import json
import sqlite3
from tqdm import tqdm
from collections import defaultdict

# Local Database Configuration
DB_FILE = "local_graph.db"
BATCH_SIZE = 1000  # SQLite handles larger batches efficiently

def setup_database():
    """Initializes the local SQLite database and tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create Nodes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            globalId TEXT PRIMARY KEY,
            label TEXT,
            properties TEXT
        )
    ''')
    
    # Create Relationships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_id TEXT,
            end_id TEXT,
            rel_type TEXT,
            FOREIGN KEY (start_id) REFERENCES nodes (globalId),
            FOREIGN KEY (end_id) REFERENCES nodes (globalId)
        )
    ''')
    
    conn.commit()
    return conn

def ingest_data(file_path):
    conn = setup_database()
    cursor = conn.cursor()

    node_label_counts = defaultdict(int)
    relationship_label_counts = defaultdict(int)
    node_count = 0
    relationship_count = 0

    # Open with specific encoding to fix your Unicode errors
    # 'errors=replace' will prevent the script from crashing on bad characters
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        node_batch = []
        rel_batch = []

        for line in tqdm(f, desc="Processing JSON Lines"):
            try:
                obj = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            if obj["type"] == "node":
                global_id = obj["properties"].get("globalId")
                label = obj["labels"][0] if obj["labels"] else "None"
                # Store properties as a JSON string
                props_json = json.dumps(obj["properties"])
                
                node_batch.append((global_id, label, props_json))
                node_label_counts[label] += 1
                node_count += 1

            elif obj["type"] == "relationship":
                start_id = obj["start"]["properties"]["globalId"]
                end_id = obj["end"]["properties"]["globalId"]
                rel_type = obj["label"]
                
                rel_batch.append((start_id, end_id, rel_type))
                relationship_label_counts[rel_type] += 1
                relationship_count += 1

            # Commit Node batches
            if len(node_batch) >= BATCH_SIZE:
                cursor.executemany('INSERT OR REPLACE INTO nodes VALUES (?, ?, ?)', node_batch)
                conn.commit()
                node_batch = []

            # Commit Relationship batches
            if len(rel_batch) >= BATCH_SIZE:
                cursor.executemany('INSERT INTO relationships (start_id, end_id, rel_type) VALUES (?, ?, ?)', rel_batch)
                conn.commit()
                rel_batch = []

        # Final commit for remaining items
        if node_batch:
            cursor.executemany('INSERT OR REPLACE INTO nodes VALUES (?, ?, ?)', node_batch)
        if rel_batch:
            cursor.executemany('INSERT INTO relationships (start_id, end_id, rel_type) VALUES (?, ?, ?)', rel_batch)
        
        conn.commit()
        conn.close()

    print("\n=== Data Statistics ===")
    print(f"Total Nodes: {node_count}")
    print(f"Total Relationships: {relationship_count}")
    print(f"Database saved to: {DB_FILE}")

if __name__ == "__main__":
    # Path to your JSON file
    JSON_FILE_PATH = "graph.json" 
    ingest_data(JSON_FILE_PATH)