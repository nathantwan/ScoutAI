import pandas as pd
import numpy as np
import os

# File paths
player_file = 'data/raw/weekly_player_stats_offense.csv'
team_off_file = 'data/raw/weekly_team_stats_offense.csv'
team_def_file = 'data/raw/weekly_team_stats_defense.csv'

# Output path
os.makedirs('data/processed', exist_ok=True)
output_file = 'data/processed/modeling_dataset.csv'

# Load data
print('Loading data...')
df_player = pd.read_csv(player_file)
df_team_off = pd.read_csv(team_off_file)
df_team_def = pd.read_csv(team_def_file)

# Basic cleaning: ensure consistent column names
for df in [df_player, df_team_off, df_team_def]:
    df.columns = [c.lower() for c in df.columns]

# 1. Rolling averages and season-to-date stats for each player
print('Engineering player rolling averages...')
rolling_cols = ['passing_yards', 'rushing_yards', 'receiving_yards', 'receptions', 'targets', 'rush_attempts', 'pass_touchdown', 'rush_touchdown', 'receiving_touchdown']
for col in rolling_cols:
    if col in df_player.columns:
        df_player[f'{col}_last3'] = (
            df_player.groupby(['player_id', 'season'])[col]
            .transform(lambda x: x.rolling(3, min_periods=1).mean())
        )
        df_player[f'{col}_season_avg'] = (
            df_player.groupby(['player_id', 'season'])[col]
            .transform(lambda x: x.expanding().mean())
        )

# 2. Infer depth chart role (e.g., WR1/2/3, RB1/2) by team/season/week
print('Inferring depth chart roles...')
if 'position' in df_player.columns and 'targets' in df_player.columns:
    is_wr = df_player['position'] == 'WR'
    df_player.loc[is_wr, 'wr_rank'] = (
        df_player[is_wr]
        .groupby(['team', 'season', 'week'])['targets']
        .rank(method='first', ascending=False)
    )
    df_player['wr_role'] = df_player['wr_rank'].apply(lambda x: f'WR{int(x)}' if pd.notnull(x) and x <= 3 else None)

# 3. Teammate quality features (sum/avg of other WRs' targets/yards, QB's stats)
print('Engineering teammate quality features...')
def teammate_stats(row, stat, pos):
    team = row['team']
    season = row['season']
    week = row['week']
    player = row['player_id']
    mask = (df_player['team']==team) & (df_player['season']==season) & (df_player['week']==week) & (df_player['position']==pos) & (df_player['player_id']!=player)
    return df_player.loc[mask, stat].sum() if stat in df_player.columns else np.nan
for stat in ['targets', 'receiving_yards', 'receptions']:
    df_player[f'other_wr_{stat}'] = df_player.apply(lambda row: teammate_stats(row, stat, 'WR'), axis=1)
for stat in ['passing_yards', 'pass_touchdown']:
    df_player[f'team_qb_{stat}'] = df_player.apply(lambda row: teammate_stats(row, stat, 'QB'), axis=1)

# 4. Join team offense stats (team, season, week)
print('Joining team offense stats...')
df_player = df_player.merge(df_team_off, on=['team', 'season', 'week'], suffixes=('', '_teamoff'), how='left')

# 5. Join opponent defense stats (opponent, season, week)
# Assume 'opponent' column exists in player data; if not, skip this step
if 'opponent' in df_player.columns:
    df_player = df_player.merge(df_team_def, left_on=['opponent', 'season', 'week'], right_on=['team', 'season', 'week'], suffixes=('', '_oppdef'), how='left')

# 6. Save processed dataset
print(f'Saving processed dataset to {output_file}...')
df_player.to_csv(output_file, index=False)
print('Done!') 