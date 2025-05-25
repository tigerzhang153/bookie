import pandas as pd
from goodish_model import predicter

def recommend_bet(games_df, betting_line):
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
    predicted_total = predicter(games_df)
    

    # Calculate edge
    edge = abs(predicted_total - betting_line)
    recommendation = "bet the OVER" if predicted_total > betting_line else "bet the UNDER"

    # Display results
    print("Betting Recommendation:")
    print(f"Model prediction: {predicted_total:.2f}")
    print(f"Betting line: {betting_line:.2f}")
    print(f"Edge: {edge:.2f} points")
    print(f"Suggested bet: {recommendation}")

    return {
        "predicted_total": predicted_total,
        "betting_line": betting_line,
        "edge": edge,
        "recommendation": recommendation
    }



if __name__ == "__main__":
    test_games_df = pd.DataFrame([
    {
        "avgpointtotal_home": 220,
        "avgpointtotal_away": 215,
        "meanpointtotal": (220 + 215) / 2
    }
]  )
    recommend_bet(test_games_df, 200)