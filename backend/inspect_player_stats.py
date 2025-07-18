import pandas as pd

# Path to your data file
file_path = 'data/raw/weekly_player_stats_offense.csv'

# Load the data
df = pd.read_csv(file_path)

# Show all column names
print('Columns:', df.columns.tolist())

# Show the first 5 rows
print(df.head()) 