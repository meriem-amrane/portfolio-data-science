import pandas as pd
import os

# Path to the data directory (one level above the extract directory)
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Check if the directory exists
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"Directory {data_dir} does not exist. Please create a 'data' folder in the main project directory.")

summary = []

for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        path = os.path.join(data_dir, file)
         
        try:
            df = pd.read_csv(path)
            summary.append({
                'file_name': file,
                'num_rows': len(df),
                'num_columns': len(df.columns)
            })
        except Exception as e:
            summary.append({
                'file_name': file,
                'error': str(e)
            })

# Create a DataFrame from the summary list
df_summary = pd.DataFrame(summary)

# Display the table with improved formatting
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("\nCSV Files Summary:")
print(df_summary.to_string(index=False))
