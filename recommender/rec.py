import pandas as pd

def recommend_best_game_to_bet(games_df, betting_lines, model):
    """
    Recommends the game with the highest edge vs sportsbook line.
    
    Parameters:
        games_df: pd.DataFrame with one row per game, containing all necessary model features.
        betting_lines: list of sportsbook over/under totals, same order as games_df.
        model: trained model with a .predict() method that takes a DataFrame and outputs total point predictions.
        
    Returns:
        DataFrame with predictions, lines, and differences.
        Also prints the best game to bet.
    """
    
    # Predict point totals
    predictions = model.predict(games_df)
    
    # Create result dataframe
    result = games_df.copy()
    result["predicted_total"] = predictions
    result["betting_line"] = betting_lines
    result["edge"] = abs(result["predicted_total"] - result["betting_line"])
    
    # Sort by biggest edge
    result = result.sort_values(by="edge", ascending=False).reset_index(drop=True)
    
    # Print recommendation
    top_game = result.iloc[0]
    print("Recommended bet: ")
    print(f"Game {top_game['HOME_TEAM_ID']} vs {top_game['VISITOR_TEAM_ID']} on {top_game['GAME_DATE_EST']}")
    print(f"Model prediction: {top_game['predicted_total']:.2f}")
    print(f"Betting line: {top_game['betting_line']:.2f}")
    print(f"Edge: {top_game['edge']:.2f} points")
    
    return result