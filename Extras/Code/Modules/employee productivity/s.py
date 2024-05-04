import pandas as pd

# Read the original Excel file
original_file_path = 'data1.xlsx'
df = pd.read_excel(original_file_path)

# Select row 2
selected_rows = df.iloc[3]  # Assuming row indexing starts from 0


# Specify the path for the new Excel file
new_file_path = 'selected_rows.xlsx'

# Save the selected rows to a new Excel file
selected_rows.to_excel(new_file_path, index=False)

print("Selected rows saved to", new_file_path)
