import pandas as pd

# Path to your data file
file_path = 'data/raw/weekly_team_stats_defense.csv'

df = pd.read_csv(file_path)

print('Columns:', df.columns.tolist())
print(df.head()) 