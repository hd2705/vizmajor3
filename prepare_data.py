import pandas as pd


# Load the CSV file
df = pd.read_csv('/Users/hrushitha/Desktop/vizmajor-3/data_scopus.csv')

# Filter out rows with missing Year, Authors, or Authors with affiliations
filtered_df = df.dropna(subset=['Year', 'Authors', 'Authors with affiliations'])

# Save the filtered data to a new CSV file
filtered_df.to_csv('filtered_data.csv', index=False)

print("Data filtering complete. Filtered data saved as 'filtered_data.csv'")