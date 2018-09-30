import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


df_sport = pd.read_csv("sport.csv")
df_books = pd.read_csv("books.csv")
df_environment = pd.read_csv("environment.csv")
df_politics = pd.read_csv("politics.csv")
df_world = pd.read_csv("world.csv")


frames = [df_sport, df_world, df_environment, df_politics, df_books]

df = pd.concat( frames )


groups = df.groupby('theme')


#for name,group in groups:
#    print name
#    print group



STAT_TO_PLOT="mean_sentence_compound"

# Violin + swarmplots of whole-article article scores from
# the different news themes
ncols = 3
f, axes = plt.subplots(nrows=2, ncols=ncols)
for i,(nm,grp) in enumerate(groups):
    sns.violinplot(  y=STAT_TO_PLOT, data=grp, ax=axes[i//ncols][i%ncols], inner=None, alpha=0.5)
    sns.swarmplot(  y=STAT_TO_PLOT, data=grp , ax=axes[i//ncols][i%ncols], alpha=0.9, color="black")
    axes[i//3][i%3].set_title(nm)
    axes[i//3][i%3].set_ylabel("Sentiment")
    axes[i//3][i%3].set_ylim(-1,1)
f.tight_layout()


# Histogram of whole-article scores for various alpha values
n_bins=15
fig, axes = plt.subplots(nrows=2, ncols=3)
for i,(nm,grp) in enumerate(groups):
    axes[i//3][i%3].hist( grp[STAT_TO_PLOT], n_bins, histtype='bar') 
    axes[i//3][i%3].set_title(nm)
    axes[i//3][i%3].set_xlabel("Sentiment")
    axes[i//3][i%3].set_xlim(-1.1,1.1)
fig.tight_layout()
fig.suptitle('Sentiment by topic', fontsize=16)
plt.show()



plt.show()
