import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from sklearn.linear_model import Ridge
import joblib
from scipy.stats import randint, uniform
from sklearn.ensemble import RandomForestRegressor, StackingRegressor


# Load datasets
gamesdata = pd.read_csv("data/cleandata2.csv")
gamesdata2017 = pd.read_csv("data/games.csv")
gamesdata2017 = gamesdata2017.loc[gamesdata2017.SEASON >= 2010]

# Add point_total to gamesdata2017
gamesdata2017["point_total"] = gamesdata2017["PTS_home"] + gamesdata2017["PTS_away"]
gamesdata2017 = gamesdata2017[["GAME_DATE_EST", "HOME_TEAM_ID", "VISITOR_TEAM_ID", "point_total"]].copy()

# Helper function to calculate average point total
def get_avg_point_total(date, team_id, df_main, df_fallback):
    home_games = df_main[(df_main["GAME_DATE_EST"] < date) & (df_main["HOME_TEAM_ID"] == team_id)]
    away_games = df_main[(df_main["GAME_DATE_EST"] < date) & (df_main["VISITOR_TEAM_ID"] == team_id)]

    if len(home_games) >= 25:
        avg_home = home_games.sort_values("GAME_DATE_EST").iloc[-25:]["point_total"].mean()
    else:
        avg_home = df_fallback[(df_fallback["GAME_DATE_EST"] < date) & 
                               (df_fallback["HOME_TEAM_ID"] == team_id)].sort_values("GAME_DATE_EST").iloc[-25:]["point_total"].mean()

    if len(away_games) >= 25:
        avg_away = away_games.sort_values("GAME_DATE_EST").iloc[-25:]["point_total"].mean()
    else:
        avg_away = df_fallback[(df_fallback["GAME_DATE_EST"] < date) & 
                               (df_fallback["VISITOR_TEAM_ID"] == team_id)].sort_values("GAME_DATE_EST").iloc[-25:]["point_total"].mean()

    return (avg_home + avg_away) / 2

# Feature engineering
avg_home_list = []
avg_away_list = []

for _, row in gamesdata.iterrows():
    home_avg = get_avg_point_total(row["GAME_DATE_EST"], row["HOME_TEAM_ID"], gamesdata, gamesdata2017)
    away_avg = get_avg_point_total(row["GAME_DATE_EST"], row["VISITOR_TEAM_ID"], gamesdata, gamesdata2017)
    avg_home_list.append(home_avg)
    avg_away_list.append(away_avg)

gamesdata["avgpointtotal_home"] = avg_home_list
gamesdata["avgpointtotal_away"] = avg_away_list
gamesdata["meanpointtotal"] = (gamesdata["avgpointtotal_home"] + gamesdata["avgpointtotal_away"]) / 2

# Define features and target
features = ["avgpointtotal_home", "avgpointtotal_away", "meanpointtotal"]
gamesdata["point_total"] = gamesdata["PTS_home"] + gamesdata["PTS_away"]
X = gamesdata[features]
y = gamesdata["point_total"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#param distinctions
param_distributions = {
    'n_estimators': [100, 200, 300, 500, 700],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 4, 6, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}



# --- Random Forest Model ---
rf = RandomForestRegressor(random_state=42)

# --- Randomized Search ---
random_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_distributions,
    n_iter=50,  # Number of random combinations to try
    cv=5,       # 5-fold cross-validation
    verbose=2,
    n_jobs=-1,
    scoring='neg_mean_absolute_error',
    random_state=42
)

xgb = XGBRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

meta_model = Ridge()

stack = StackingRegressor(
    estimators=[('rf', rf), ('xgb', xgb)],
    final_estimator=meta_model,
    passthrough=True,  # optional: passes original features to final estimator
    n_jobs=-1
)

stack.fit(X_train, y_train)
preds = stack.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print(f"Stacked Model MAE: {mae:.2f}")

# --- Fit the Search ---
random_search.fit(X_train, y_train)

# --- Best Model ---
best_model = random_search.best_estimator_
print("Best parameters:", random_search.best_params_)

# --- Evaluate on Test Set ---
y_pred = stack.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Optimized MAE on test set: {mae:.2f}")