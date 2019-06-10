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
        f"results/{name}",
        facecolor=fig.get_facecolor(),
        format=format,
        dpi=dpi,
        **kwargs
    )

# %%

