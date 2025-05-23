import matplotlib.pyplot as plt
import pandas as pd

X_full = pd.read_csv("data/cleandata2.csv")
with plt.style.context("ggplot"):
    plt.scatter(X_full.meanpointtotal, X_full.point_total, marker="o", alpha=0.1, color='#9467bd')
    plt.xlabel("Mean last 50 games")
    plt.ylabel("Total points (y)")
    plt.title("Total points (y) vs mean last 50 games ")
fig1 = plt.figure()


with plt.style.context("ggplot"):
    plt.scatter(X_full["diff"], X_full.point_total, marker="o", alpha=0.1)
    plt.xlabel("Difference")
    plt.ylabel("Total points (y)")
    plt.title("Total points (y) vs mean last 50 games ")
fig2 = plt.figure()

with plt.style.context("ggplot"):
    plt.scatter(X_full["diff"].abs(), X_full.point_total, marker="o", alpha=0.1)
    plt.xlabel("Difference")
    plt.ylabel("Total points (y)")
    plt.title("Total points (y) vs mean last 50 games ")
fig3 = plt.figure()

season_avg = X_full.groupby(by=["SEASON"]).mean()

with plt.style.context("ggplot"):
    plt.scatter(season_avg.index, season_avg.point_total, color = "#d62728" )
    plt.xlabel("Season")
    plt.ylabel("Total points (y)")
    plt.title("Mean Total Points Per Season")
fig4 = plt.figure()

plt.show()