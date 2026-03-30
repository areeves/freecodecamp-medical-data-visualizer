import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['height-m'] = df['height'] / 100
df['bmi'] = df['weight'] / (df['height-m'] ** 2)
df['overweight'] = (df['bmi'] > 25).astype(int)

# 3
df['gluc'] = (df['gluc'] - 1).astype(bool).astype(int)
df['cholesterol'] = (df['cholesterol'] - 1).astype(bool).astype(int)



# 4
def draw_cat_plot():
    # 5
    cols = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    df_cat = df.melt(id_vars=['cardio'], value_vars=cols, var_name='Variable', value_name='Value')

    # 6
    df_cat = df_cat.groupby(['cardio', 'Variable', 'Value'], as_index=False).size()
    df_cat = df_cat.rename(columns={'size': 'total'})   # 'total' is the count used as y-axis

    # 7
    g = sns.catplot(
        data=df_cat,
        x='Variable',
        y='total',
        hue='Value',
        col='cardio',
        kind='bar',
        height=5,
        aspect=1.2,
        errorbar=None          # removes unnecessary error bars for binary data
    )


    # 8
    fig = g.fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    apfilter = df['ap_lo'] <= df['ap_hi']
    hfilter = (df['height'] >= df['height'].quantile(0.025)) & (df['height'] < df['height'].quantile(0.975))
    wfilter = (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] < df['weight'].quantile(0.975))
    df_heat = df[ apfilter & hfilter & wfilter ]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(12, 10))   # or (10, 8) - both commonly pass
    
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,           # show correlation values inside cells
        fmt='.1f',            # one decimal place
        linewidths=0.5,       # thin lines between cells
        square=True,          # make cells square
        center=0,             # center the colormap at 0
        vmin=-0.15,           # optional but helps matching expected colors
        vmax=0.35,            # optional
        cbar_kws={"shrink": 0.8}
    )

    # 15



    # 16
    fig.savefig('heatmap.png')
    return fig
