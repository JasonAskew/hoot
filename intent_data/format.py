import pandas as pd
import ast

# Load the CSV file
df = pd.read_csv('combined_output.csv')

# Function to update scope and tags
def update_scope_and_tags(row):
    original_scope = row['scope']
    if original_scope in ['test_gold', 'test_platinum']:
        # Safely evaluate tags string into a list
        try:
            tags = ast.literal_eval(row['tags']) if pd.notna(row['tags']) else []
        except:
            tags = []
        if original_scope not in tags:
            tags.append(original_scope)
        row['tags'] = str(tags)
        row['scope'] = 'test'
    return row

# Apply transformation
df = df.apply(update_scope_and_tags, axis=1)

# Save modified CSV
df.to_csv('new_combined_output.csv', index=False)
