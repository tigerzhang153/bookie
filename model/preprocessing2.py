import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder

X_full = pd.read_csv("data/cleandata2.csv")
X_full["GAME_DATE_EST"] = pd.to_datetime(X_full["GAME_DATE_EST"])
X_full = X_full.sort_values(by=["GAME_DATE_EST"], ascending=False).reset_index(drop=True)

# One-hot encode team IDs with separate encoders to avoid column mismatch
home_encoder = OneHotEncoder(sparse_output=False)
away_encoder = OneHotEncoder(sparse_output=False)

ohe_home = home_encoder.fit_transform(X_full[["HOME_TEAM_ID"]])
ohe_away = away_encoder.fit_transform(X_full[["VISITOR_TEAM_ID"]])

# Create one-hot DataFrames
home_team_df = pd.DataFrame(ohe_home, columns=[f"HOME_TEAM_{int(c)}" for c in home_encoder.categories_[0]])
away_team_df = pd.DataFrame(ohe_away, columns=[f"AWAY_TEAM_{int(c)}" for c in away_encoder.categories_[0]])

# Subtract base season
X_full["SEASON"] = X_full["SEASON"] - 2010

# Drop unneeded columns
X_full = X_full.drop(columns=["HOME_TEAM_ID", "VISITOR_TEAM_ID", "PTS_home", "PTS_away", "GAME_DATE_EST"])

# Reset indices to align and merge
home_team_df = home_team_df.reset_index(drop=True)
away_team_df = away_team_df.reset_index(drop=True)
X_full = X_full.reset_index(drop=True)


plt.figure(figsize=(17, 13))
sns.heatmap(X_full.corr(),
            cmap="Blues",annot=True, fmt='.2f', vmin=0)
plt.show()