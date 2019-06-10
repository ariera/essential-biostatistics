# %%
import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import scipy.stats as stats
import matplotlib.pyplot as plt
import altair as alt

plt.style.use('tableau-colorblind10')
sns.set(style="ticks")

def save_figure(fig, name, format='pdf', dpi=300, **kwargs):
    fig.savefig(
        name,
        facecolor=fig.get_facecolor(),
        format=format,
        dpi=dpi,
        **kwargs
    )

# %% [markdown]
# ## What does 95% confidence really mean? - A simulation
# We have a bowl with 100 balls, 25 of which are read and 75 of which are black
# We pretend not to know this distrubution
#
red_balls = ['red' for i in range(25)]
black_bals = ['black' for i in range(75)]
bowl = red_balls + black_bals
# %% [markdown]
# We mix the balls, choose one randomly and put it back again. We repeat this process
# 15 times and calculate the 95% CI for this proportion
import random
from statsmodels.stats.proportion import proportion_confint

def simulation():
    number_of_red_balls_observed = 0
    NUMBER_OF_TRIALS = 15
    CONFIDENCE_LEVEL = 0.95
    for i in range(NUMBER_OF_TRIALS):
        random.shuffle(bowl)
        ball = random.choice(bowl)
        if ball == 'red':
            number_of_red_balls_observed += 1
    ci_low, ci_up = proportion_confint(number_of_red_balls_observed, NUMBER_OF_TRIALS, alpha=1.0 - CONFIDENCE_LEVEL)
    return (ci_low, ci_up, number_of_red_balls_observed/NUMBER_OF_TRIALS)

# %% [markdown]
# We repeat the same simulation 20 times
df = pd.DataFrame(columns=['ci_low', 'ci_up', 'observed_proportion'])
NUMBER_OF_SIMULATIONS = 20
for i in range(NUMBER_OF_SIMULATIONS):
    ci_low, ci_up, observed_proportion = simulation()
    df = df.append({
        'ci_low': ci_low,
        'ci_up': ci_up,
        'observed_proportion': observed_proportion,
    }, ignore_index=True)
# %%
def plot_confidence_intervals(df):
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Rectangle
    BAR_WIDTH = 1
    BAR_STEP = 1
    fig, ax = plt.subplots(1)

    for i, row in df.iterrows():
        bar_height = row['ci_up'] - row['ci_low']
        r = Rectangle((i*BAR_STEP, row['ci_low']), BAR_WIDTH-0.1, bar_height)
        pc = PatchCollection([r], facecolor='r', edgecolor='None', alpha=0.5)
        plt.plot([i*BAR_STEP, i*BAR_STEP+BAR_WIDTH-0.2], [row['observed_proportion'], row['observed_proportion']], 'k-')
        ax.add_collection(pc)

    plt.plot([0, NUMBER_OF_SIMULATIONS], [0.25,0.25])
    plt.ylim(bottom=0, top=1)
    plt.xlim(left=0, right=NUMBER_OF_SIMULATIONS)
    plt.show()
    return fig, ax

# %% [markdown]
# The following figure shows the results of our 20 simulations.
# Each bar represents the 95% confidence interval of the simulation. The black
# line inside the bar represent the observed proportion. The horizontal line
# shows the true proportion (25% red balls
#
# In about half of the simulations the sample proportion is higher the 25%, and
# in about half the sample proportion is lower
#
# In the long run, 5% of the of 95% confidence intervals will not incude the
# population value.
fig, ax = plot_confidence_intervals(df)
save_figure(fig, 'confidence_intervals/confidence_intervals.png', format="png")