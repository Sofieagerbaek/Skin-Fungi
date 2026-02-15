import re

# Read tree from file
with open("../results/Results_Aug23/Species_tree/SpeciesTree_rooted_node_labels.txt") as f:
    tree = f.read()

# List to store extracted IDs
ids = []

# Function to replace and collect IDs
def replace_id(match):
    ids.append(match.group(1))
    return ":"  # keep the colon for branch lengths

# Replace last _<ID> before : using regex
clean_tree = re.sub(r'_([^_:]+):', replace_id, tree)

# Save cleaned tree
with open("tree_clean.txt", "w") as f:
    f.write(clean_tree)

# Save extracted IDs
with open("tree_ids.txt", "w") as f:
    f.write("\n".join(ids))

# Optional: print results

