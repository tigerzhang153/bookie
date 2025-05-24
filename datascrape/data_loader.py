from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import numpy as np

def load_nba_game_data():
    gamefinder = leaguegamefinder.LeagueGameFinder(season_type_nullable="Regular Season")
    games = gamefinder.get_data_frames()[0]
    games = games[['GAME_ID', 'TEAM_ID', 'TEAM_NAME', 'GAME_DATE', 'MATCHUP', 'WL', 'PTS']]
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])

    # Simulate odds (replace with real odds later)
    np.random.seed(42)
    games['odds_team'] = np.random.uniform(1.6, 2.4, size=len(games))
    return games