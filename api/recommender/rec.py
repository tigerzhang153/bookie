import pandas as pd
from .goodish_model import predicter

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
    
    # Calculate confidence based on edge size
    # Larger edge = higher confidence (capped at 95%, minimum 50%)
    # Edge of 10+ points = 95% confidence, edge of 0 = 50% confidence
    max_edge = 10.0
    confidence = min(95, max(50, 50 + (edge / max_edge) * 45))

    # Display results
    print("Betting Recommendation:")
    print(f"Model prediction: {predicted_total:.2f}")
    print(f"Betting line: {betting_line:.2f}")
    print(f"Edge: {edge:.2f} points")
    print(f"Confidence: {confidence:.1f}%")
    print(f"Suggested bet: {recommendation}")

    return {
        "predicted_total": round(predicted_total, 1),
        "betting_line": round(betting_line, 1),
        "edge": round(edge, 1),
        "confidence": round(confidence, 1),
        "recommendation": recommendation,
        "model_features": {
            "avgpointtotal_home": round(games_df.iloc[0]["avgpointtotal_home"], 1),
            "avgpointtotal_away": round(games_df.iloc[0]["avgpointtotal_away"], 1),
            "meanpointtotal": round(games_df.iloc[0]["meanpointtotal"], 1)
        }
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