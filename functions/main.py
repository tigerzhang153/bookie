import os
import sys
import json
import pandas as pd
import logging
from firebase_functions import https_fn
from firebase_admin import initialize_app

# Add paths for imports
functions_dir = os.path.dirname(__file__)
sys.path.insert(0, functions_dir)

# Import the recommender
from recommender.rec import recommend_bet

# Initialize Firebase Admin
initialize_app()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@https_fn.on_request(
    cors=https_fn.CorsOptions(
        cors_origins=["https://bookie-ai-dc1f8.web.app", "http://localhost:3000"],
        cors_methods=["GET", "POST", "OPTIONS"],
    ),
    memory=2048,
    timeout_sec=300,
)
def api(req: https_fn.Request) -> https_fn.Response:
    """Firebase Function for API endpoints"""
    
    # Health check endpoint
    if req.path == "/health" or req.path == "/api/health":
        return https_fn.Response(
            json.dumps({"status": "healthy"}),
            status=200,
            headers={"Content-Type": "application/json"}
        )
    
    # Predict endpoint
    if req.method == "POST" and ("/predict" in req.path or "/api/predict" in req.path):
        try:
            # Parse request body
            request_json = req.get_json(silent=True)
            if not request_json:
                return https_fn.Response(
                    json.dumps({"detail": "Invalid request body"}),
                    status=400,
                    headers={"Content-Type": "application/json"}
                )
            
            home_team_id = request_json.get("home_team_id")
            away_team_id = request_json.get("away_team_id")
            betting_line = request_json.get("betting_line")
            
            if not all([home_team_id, away_team_id, betting_line]):
                return https_fn.Response(
                    json.dumps({"detail": "Missing required fields"}),
                    status=400,
                    headers={"Content-Type": "application/json"}
                )
            
            logger.info(f"Received prediction request for teams: {home_team_id} vs {away_team_id}")
            
            # Get the data directory path
            current_dir = os.path.dirname(__file__)
            data_dir = os.path.join(current_dir, "data")
            
            # Load historical data
            try:
                games_df = pd.read_csv(os.path.join(data_dir, "cleandata2.csv"))
                games2017_df = pd.read_csv(os.path.join(data_dir, "games.csv"))
                logger.info("Successfully loaded historical data")
            except Exception as e:
                logger.error(f"Error loading data files: {str(e)}")
                return https_fn.Response(
                    json.dumps({"detail": "Error loading historical data"}),
                    status=500,
                    headers={"Content-Type": "application/json"}
                )
            
            # Calculate average point totals for both teams
            home_games = games_df[games_df["HOME_TEAM_ID"] == home_team_id].tail(25)
            away_games = games_df[games_df["VISITOR_TEAM_ID"] == away_team_id].tail(25)
            
            home_avg = home_games["PTS_home"].mean() + home_games["PTS_away"].mean()
            away_avg = away_games["PTS_home"].mean() + away_games["PTS_away"].mean()
            
            if pd.isna(home_avg) or pd.isna(away_avg):
                home_avg = 220  # fallback value
                away_avg = 215  # fallback value
            
            mean_total = (home_avg + away_avg) / 2
            
            # Create DataFrame with the required format
            game_data = pd.DataFrame([{
                "avgpointtotal_home": home_avg,
                "avgpointtotal_away": away_avg,
                "meanpointtotal": mean_total
            }])
            
            # Get prediction using the recommend_bet function
            prediction = recommend_bet(game_data, betting_line)
            logger.info(f"Prediction successful: {prediction}")
            
            return https_fn.Response(
                json.dumps(prediction),
                status=200,
                headers={"Content-Type": "application/json"}
            )
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return https_fn.Response(
                json.dumps({"detail": str(e)}),
                status=500,
                headers={"Content-Type": "application/json"}
            )
    
    # 404 for other paths
    return https_fn.Response(
        json.dumps({"detail": "Not found"}),
        status=404,
        headers={"Content-Type": "application/json"}
    )
