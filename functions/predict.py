#!/usr/bin/env python3
import os
import sys
import json
import pandas as pd

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recommender'))

from recommender.rec import recommend_bet

def main():
    try:
        # Get input from environment variables
        home_team_id = int(os.environ.get('HOME_TEAM_ID'))
        away_team_id = int(os.environ.get('AWAY_TEAM_ID'))
        betting_line = float(os.environ.get('BETTING_LINE'))
        
        # Get data directory
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, 'data')
        
        # Load historical data
        games_df = pd.read_csv(os.path.join(data_dir, 'cleandata2.csv'))
        games2017_df = pd.read_csv(os.path.join(data_dir, 'games.csv'))
        
        # Calculate average point totals
        home_games = games_df[games_df['HOME_TEAM_ID'] == home_team_id].tail(25)
        away_games = games_df[games_df['VISITOR_TEAM_ID'] == away_team_id].tail(25)
        
        home_avg = home_games['PTS_home'].mean() + home_games['PTS_away'].mean()
        away_avg = away_games['PTS_home'].mean() + away_games['PTS_away'].mean()
        
        if pd.isna(home_avg) or pd.isna(away_avg):
            home_avg = 220
            away_avg = 215
        
        mean_total = (home_avg + away_avg) / 2
        
        # Create DataFrame
        game_data = pd.DataFrame([{
            'avgpointtotal_home': home_avg,
            'avgpointtotal_away': away_avg,
            'meanpointtotal': mean_total
        }])
        
        # Get prediction
        prediction = recommend_bet(game_data, betting_line)
        
        # Output JSON
        print(json.dumps(prediction))
        
    except Exception as e:
        error = {'detail': str(e)}
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

