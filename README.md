# Bookie - Sports Betting Recommendation System

A machine learning-powered sports betting recommendation system that analyzes game data and provides betting suggestions.

## Project Structure
```
bookie/
├── recommender/       # Core recommendation engine
├── data/             # Data storage
├── model/            # Model training and evaluation
├── datascrape/       # Data collection scripts
└── src/              # Web application frontend
```

## Setup

### Python Environment Setup
1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Web Application Setup
1. Install Node.js dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Usage

### Making Predictions
```python
from recommender.rec import recommend_bet
import pandas as pd

# Prepare game data
game_data = pd.DataFrame({
    "avgpointtotal_home": [220],
    "avgpointtotal_away": [215],
    "meanpointtotal": [(220 + 215) / 2]
})

# Get recommendation
result = recommend_bet(game_data, betting_line=200)
```

## Features
- Machine learning model using stacked Random Forest and XGBoost
- Historical game data analysis
- Over/Under betting recommendations
- Edge calculation against betting lines

## License
MIT