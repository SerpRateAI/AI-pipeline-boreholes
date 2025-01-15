"""
python script that generates all of the plots for the paper

necessary data must exist in the following locations for this script to work:

dataset_path = 'Datasets/Dataset_BA1B.xlsx'
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
import numpy as np
import matplotlib.colors as mcolors
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics as 


def import_dataset():
    dataset_path = 'Datasets/Dataset_BA1B.xlsx'
    
    df = pd.read_excel(dataset_path)
    [c for c in df.columns]
    geology_columns = ['UNIT_TYPE_Dunite',
     'UNIT_TYPE_Fault rock',
     'UNIT_TYPE_Gabbro',
     'UNIT_TYPE_Harzburgite',
     'UNIT_TYPE_Metagabbro',
     'UNIT_TYPE_Other',
    'TOP_DEPTH'
                      ]
    df.dropna(subset='TOP_DEPTH', inplace=True)

    return df

def plot_fig2_legend():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pcolormesh(np.vstack([1, 2, 3, 4, 5, 6]), cmap='rainbow', vmin=0, vmax=6)
    ax.text(s='Dunite', x=0.1, y=0.25, fontsize=20)
    ax.text(s='Fault Rock', x=0.1, y=1.25, fontsize=20)
    ax.text(s='Gabbro', x=0.1, y=2.25, fontsize=20)
    ax.text(s='Harzburgite', x=0.1, y=3.25, fontsize=20)
    ax.text(s='Metagabbro', x=0.1, y=4.25, fontsize=20)
    ax.text(s='Other', x=0.1, y=5.25, fontsize=20)
    # ax.set_xlim(0, 0.6)
    ax.set_yticks([])
    ax.set_xticks([])
    fig.savefig('geology_legend.pdf', bbox_inches='tight')

def plot_fig2(df):
    """
    plots the raw data for the physical, chemical, and bio
    measurements made in the BA1B borehole.
    """
   fig2_cols = ['Cell abundance (cells/g)',
     'Mean dry electrical Resistivity (ohmm)',
     'Bulk density (g/cm³)',
     'AMS bulk susceptibility',
     'LOI wt%',
     'CO2 wt%',
     'H20 wt%',
     'CaCO3 calc',
    '% of fractures',
    'TOP_DEPTH',
    'ALTERATION',
    'PnS2_sum',
     'PnL_sum',
     'PnP3V_sum',
     'PnP3H_sum',
     'PnP4_sum',
     'PnP6V_sum',
     'FnS2_sum',
     'FnL_sum',
     'FnP3V_sum',
     'FnP3H_sum',
     'FnP4_sum',
     'FnP6V_sum',
    'Alteration_dummies_50%-90%',
     'Alteration_dummies_>90%',]
    
    connectivity = ['PnS2_sum',
     'PnL_sum',
     'PnP3V_sum',
     'PnP3H_sum',
     'PnP4_sum',
     'PnP6V_sum',
     'FnS2_sum',
     'FnL_sum',
     'FnP3V_sum',
     'FnP3H_sum',
     'FnP4_sum',
     'FnP6V_sum',]
    
    fig2_df = df[fig2_cols].copy()
    fig2_df.sort_values(by='TOP_DEPTH', inplace=True)
    fig, ax = plt.subplots(1, 11, figsize=(14, 7), sharey=True)
    
    y = fig2_df.TOP_DEPTH
       
    ax[0].pcolormesh(xx, yy, Z[:-1], vmin=0, vmax=6, cmap='rainbow', shading='auto')
    ax[0].set_title('Geology', fontsize=8)
    ax[0].set_xticks([])
    
    ax[1].plot(fig2_df['Bulk density (g/cm³)'], y, color='darkblue')
    ax[1].set_title('Bulk density\n(g/cm³)', fontsize=8)
    ax[1].set_xticks([2.6, 2.8])
    
    ax[2].plot(fig2_df['% of fractures'], y, color='red', linewidth=1)
    ax[2].set_title('% of fractures', fontsize=8)
    
    for c in connectivity:
        if c == 'PnL_sum':
            color = 'red'
            ax[3].plot(fig2_df[c], y, color=color, linewidth=0.5)
    
        else:
            color = 'cyan'
    ax[3].set_title('Connectivity', fontsize=8)
        
    ax[4].plot(fig2_df['Cell abundance (cells/g)'], y, color='limegreen')
    ax[4].set_xscale('log')
    ax[4].set_title('Cell abundance\n(cells/g)', fontsize=8)
    ax[4].set_xlim(1.9e1, 1e8)
    ax[4].set_xticks([1e3, 1e5, 1e7])
    
    ax[5].plot(fig2_df['Mean dry electrical Resistivity (ohmm)'], y, color='darkorange')
    ax[5].set_xscale('log')
    ax[5].set_title('Mean dry\nelectrical\nresistivity\n(ohm)', fontsize=8)
    ax[5].set_xlim(1e1, 1e5)
    ax[5].set_xticks([1e2, 1e4])
    
    ax[6].plot(fig2_df['AMS bulk susceptibility'], y, color='forestgreen')
    ax[6].set_title('AMS bulk\nsusceptibility', fontsize=8)
    ax[6].set_xlim(-0.01, 0.05)
    ax[6].set_xticks([0.0, 0.04])
    
    ax[7].plot(fig2_df['LOI wt%'], y, color='gold')
    ax[7].set_title('LOI wt%', fontsize=8)
    
    ax[8].plot(fig2_df['CO2 wt%'], y, color='brown')
    ax[8].set_title(r'CO$_{2}$ wt%', fontsize=8)
    ax[8].set_xlim(-0.1, 1.2)
    
    ax[9].plot(fig2_df['H20 wt%'], y, color='dodgerblue')
    ax[9].set_title('H$_{2}$0 wt%', fontsize=8)
    
    ax[10].plot(fig2_df['CaCO3 calc'], y, color='grey')
    ax[10].set_title('CaCO$_{3}$ calc', fontsize=8)
    ax[10].set_xlim(-0.1, 3)
    
    ax[0].set_ylabel('Depth (m)')
    fig.subplots_adjust(wspace=0, hspace=0)
    ax[0].set_ylim(400, 0)
    
    fig.savefig('physical_measurements.pdf', bbox_inches='tight')


def plot_fig3(df):
    """

    """
    groups = [
        ['Veins', 'Serpentine vein', 'Carbonate veins', 'White veins', 'Green veins',
         'Blue patches', 'Magmatic veins', 'Dark green', 'Magmatic intrusions',
         'Hydrothermal', 'Offsets', 'Rodingite'],
        ['Oxidation', 'Black serpentinization', 'Alteration', 'Alteration halo',
         'Altered gabbro', 'Altered', 'Pyroxenite'],
        ['Network', 'Coalescence', 'Dyke', 'Shearing', 'Crack'
         ,  'Open cracks'
         , 'Open crack', 'Irregular', 'Subvertical',
         'Subhorizontal', 'Lineation', 'Thickness', 'Offset', 'Fracture',
         'Sheared', 'Striations', 'Branching', 'Slickensides'],
        ['Dunite', 'Gabbro', 'Microgabbro', 'Harzburgite', 'Pxenites', 'Dunitic zone','Magnetite'],
        ['Plagioclase', 'Microbio sample', 'Bulk serp', 'Bulk'],
        ['Fine grained', 'Waxy green', 'Waxy', 'Wavy']
    ]
    words = []
    for group in groups:
        for word in group:
            words.append(word)

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.set_ylim(400, 0)
    ax.set_xticks(np.arange(len(words)))
    
    data = df[words].copy()
    vals = data.to_numpy()
    
    cmaps = ['Reds', 'Blues', 'Greens', 'Purples', 'Oranges', 'Greys']
    
    glen = 0
    for n, g in enumerate(groups):
        start = glen
        end = glen + len(g)
        
        x = np.arange(vals[:,start:end].shape[1]) + glen
        y = df.TOP_DEPTH.values
        xx, yy = np.meshgrid(x, y)
        data[data == 0] = np.nan
        ax.pcolormesh(xx, yy, data[g], cmap=cmaps[n], shading='nearest', vmin=0, vmax=1.5)
        glen += len(g)
        
    ax.set_xticklabels(words, rotation=90)
    ax.text(s='Veins and Alteration', color='red', x=2, y= -10)
    ax.text(s='Oxidation\nand Alteration', color='blue', x=13, y= -10)
    ax.text(s='Structural Features', color='green', x=25, y= -10)
    ax.text(s='Rock Type', color='purple', x=38, y= -10)
    ax.text(s='Mineralogy', color='red', x=43.5, y= -10)
    ax.text(s='Physical\nCharacteristics', color='grey', x=47, y= -10)
    
    ax.text(s='ChatGPT Keywords', color='black', x=20, y=550, fontsize=15)
    ax.text(s='ChatGPT Topics', color='black', x=20, y=-50, fontsize=15)
    ax.set_ylabel('Depth (m)')

    fig.savefig('topics_keywords.pdf', bbox_inches='tight')


if __name__=='__main__':
    df = import_dataset()
    plot_fig2_legend()
    plot_fig2(df=df)
    plot_fig3(df=df)