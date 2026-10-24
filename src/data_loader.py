import os

def load_topology(file_path):
    """Parses the tab-separated upstream topology text file into a dictionary."""
    topology_map = {}
    
    if not os.path.exists(file_path):
        return topology_map # Fails gracefully if file isn't placed yet
        
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if not parts or len(parts) < 2:
                continue
            
            premise_id = parts[0]
            equipment_chain = []
            
            # Parse each upstream node delimited by '*'
            for node in parts[1:]:
                node_details = node.split('*')
                if len(node_details) >= 4:
                    equipment_chain.append({
                        'table': node_details[0],
                        'object_id': node_details[1],
                        'asset_type': node_details[2],
                        'asset_number': node_details[3]
                    })
            topology_map[premise_id] = equipment_chain
            
    return topology_map

# Hardcoded labor constants extracted from Install_Labor_HackOHIO.xlsx
INDIRECT_LABOR_MULTIPLIER = 4.5

# Baseline install hours
LABOR_RATES = {
    "Crossarm": 0.37,
    "Bracket": 0.61,
    "Transformer (Medium)": 2.5,
    "Fuse": 0.5,
    "Recloser (Hydraulic)": 1.5,
    "Recloser (Electronic)": 1.5,
    "Circuit Breaker": 2.0,
    "Pole (Medium)": 4.0
}