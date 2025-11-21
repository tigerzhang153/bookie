from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import logging
from recommender.rec import recommend_bet
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://bookie-ai-dc1f8.web.app",  # Your Firebase hosting URL
        "https://bookie-ai-dc1f8.firebaseapp.com"  # Alternative Firebase URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class GameInput(BaseModel):
    home_team_id: int
    away_team_id: int
    betting_line: float

@app.post("/predict")
async def predict_game(game_input: GameInput):
    try:
        logger.info(f"Received prediction request for teams: {game_input.home_team_id} vs {game_input.away_team_id}")
        
        # Get the absolute path to the data directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        
        # Load historical data
        try:
            games_df = pd.read_csv(os.path.join(data_dir, "cleandata2.csv"))
            games2017_df = pd.read_csv(os.path.join(data_dir, "games.csv"))
            logger.info("Successfully loaded historical data")
        except Exception as e:
            logger.error(f"Error loading data files: {str(e)}")
            raise HTTPException(status_code=500, detail="Error loading historical data")

        # Calculate average point totals for both teams
        home_games = games_df[games_df["HOME_TEAM_ID"] == game_input.home_team_id].tail(25)
        away_games = games_df[games_df["VISITOR_TEAM_ID"] == game_input.away_team_id].tail(25)
        
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
        try:
            prediction = recommend_bet(game_data, game_input.betting_line)
            logger.info(f"Prediction successful: {prediction}")
            return JSONResponse(content=prediction)
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Model file not found: {str(e)}")
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Bookie API",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 