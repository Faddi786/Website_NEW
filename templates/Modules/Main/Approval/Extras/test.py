import pandas as pd

# Create a larger DataFrame with sub DataFrames
data = {'ID': [1, 2, 3],
        'Sub_DF': [pd.DataFrame({'A': [1, 2], 'B': [3, 4]}),
                   pd.DataFrame({'A': [5, 6], 'B': [7, 8]}),
                   pd.DataFrame({'A': [9, 10], 'B': [11, 12]})]}

df = pd.DataFrame(data)

# Initialize an empty list to store the sub DataFrames
dfs_to_append = []

# Iterate over the sub DataFrames in df and append them to the list
for _, row in df.iterrows():
    dfs_to_append.append(row['Sub_DF'])

# Concatenate the list of sub DataFrames into a single DataFrame
result_df = pd.concat(dfs_to_append, ignore_index=True)

print("Result DataFrame:")
print(result_df)
