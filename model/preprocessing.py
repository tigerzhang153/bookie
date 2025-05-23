import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from sklearn import preprocessing 
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns


# Load your dataset
X_full = pd.read_csv("data/cleandata2.csv")
X_full["GAME_DATE_EST"] = pd.to_datetime(X_full["GAME_DATE_EST"])
X_full = X_full.sort_values(by=["GAME_DATE_EST"], ascending=False).reset_index()

# One-hot encode HOME_TEAM_ID
home_encoder = OneHotEncoder(sparse_output=False)
ohe_home = home_encoder.fit_transform(X_full[["HOME_TEAM_ID"]])

# One-hot encode VISITOR_TEAM_ID
away_encoder = OneHotEncoder(sparse_output=False)
ohe_away = away_encoder.fit_transform(X_full[["VISITOR_TEAM_ID"]])

# Drop old columns
X_full = X_full.drop(columns=["HOME_TEAM_ID", "VISITOR_TEAM_ID", "PTS_home", "PTS_away", "GAME_DATE_EST", "index"])

# Optionally convert to DataFrame and merge
home_team_df = pd.DataFrame(ohe_home, columns=[f"HOME_TEAM_{int(c)}" for c in home_encoder.categories_[0]])
away_team_df = pd.DataFrame(ohe_away, columns=[f"AWAY_TEAM_{int(c)}" for c in away_encoder.categories_[0]])

# Reset indices to avoid alignment issues
X_full = X_full.reset_index(drop=True)
home_team_df = home_team_df.reset_index(drop=True)
away_team_df = away_team_df.reset_index(drop=True)

# Combine everything
X_full = pd.concat([X_full, home_team_df, away_team_df], axis=1)

# Final check
print(X_full.head())
print(X_full.describe())

plt.figure(figsize=(16, 12))
sns.heatmap(X_full.corr(),
            cmap="Blues",annot=True, fmt='.2f', vmin=0)

ohe_home_df = pd.DataFrame(ohe_home)
ohe_away_df = pd.DataFrame(ohe_away, columns=list("abcdefghijklmnopqrstuvwxyzABCD"))
X_full = pd.concat([X_full,ohe_home_df], axis=1)
X_full = pd.concat([X_full,ohe_away_df], axis=1)
print(X_full.describe)
