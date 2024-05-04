import pandas as pd
import json
import sys

def create_excel(data):
    # Load JSON data
    try:
        data = json.loads(data)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return
    
    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to Excel
    try:
        df.to_excel('outputdrone.xlsx', index=False)
        print("Data saved to outputdrone.xlsx successfully!")
    except Exception as e:
        print("Error saving data to Excel:", e)

if __name__ == "__main__":
    # Check if JSON data is provided as command-line argument
    if len(sys.argv) < 2:
        print("Usage: python create_excel.py <json_data>")
    else:
        json_data = sys.argv[1]
        create_excel(json_data)
