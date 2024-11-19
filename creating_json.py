import pandas as pd
import json
from collections import Counter

# Load the data
file_path = '/Users/hrushitha/Desktop/vizmajor-3/filtered_data.csv'  
filtered_data = pd.read_csv(file_path)

# Helper function to parse author information
def parse_authors(authors_with_affiliations):
    authors = []
    if pd.notna(authors_with_affiliations):
        for author_info in authors_with_affiliations.split(';'):
            parts = author_info.split(',')
            if len(parts) >= 3:
                name = parts[0].strip()
                affiliation = parts[1].strip()
                country = parts[-1].strip()
                authors.append({"name": name, "affiliation": affiliation, "country": country})
    return authors

# Extract authors and their connections
authors_data = []
author_connections = []
for _, row in filtered_data.iterrows():
    authors = parse_authors(row['Authors with affiliations'])
    authors_data.extend(authors)
    # Create pairwise links between authors in the same publication
    for i in range(len(authors)):
        for j in range(i + 1, len(authors)):
            author_connections.append((authors[i]['name'], authors[j]['name']))

# Deduplicate authors and links
authors_data = {author['name']: author for author in authors_data}  # Deduplicate by author name
links_data = Counter(author_connections)  # Count shared publications

# Prepare nodes and links for JSON
nodes = list(authors_data.values())
links = [{"source": source, "target": target, "value": value} for (source, target), value in links_data.items()]

# Determine top 10 countries by author count
country_counts = Counter(author['country'] for author in nodes)
top_countries = set(country for country, _ in country_counts.most_common(10))

# Assign colors based on the top 10 countries
for node in nodes:
    node['color'] = "gray" if node['country'] not in top_countries else "highlight"

# Create the final JSON structure
network_json = {"nodes": nodes, "links": links}

# Save the JSON to a file
output_file_path = 'author_network.json'  # Replace with your desired output file path
with open(output_file_path, 'w') as f:
    json.dump(network_json, f, indent=2)

print(f"JSON file created at: {output_file_path}")
