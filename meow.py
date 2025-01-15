"""
This file runs all of the catboost models in the pipeline
"""

from catboost import CatBoostRegressor, Pool
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd

xvars = ['Cell abundance (cells/g)',
    'Mean dry electrical Resistivity (ohmm)',
    # 'Bulk density (g/cm³)',
    'AMS bulk susceptibility',
    'LOI wt%',
    'CO2 wt%',
    'H20 wt%',
    'CaCO3 calc',
    # 'SECTION_UNIT',
    '% of fractures',
    # 'IMAGES',
    # 'SEGMENTATION',
    # 'TOP_DEPTH',
    # 'ALTERATION',
    # 'REMARKS1',
    # 'REMARKS2',
    # 'REMARKS4',
    # 'REMARKS5',
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
    'UNIT_TYPE_Dunite',
    'UNIT_TYPE_Fault rock',
    'UNIT_TYPE_Gabbro',
    'UNIT_TYPE_Harzburgite',
    'UNIT_TYPE_Metagabbro',
    'UNIT_TYPE_Other',
    'UNIT_CLASS_OPHIO',
    'UNIT_CLASS_UND',
    'TEXTURES_Brecciated',
    'TEXTURES_Sheared',
    'GRAINSIZE_Cryptocrystalline',
    'GRAINSIZE_Fine grained',
    'GRAINSIZE_Medium grained',
    'GRAINSIZE_Microcrystalline',
    'GRAINSIZE2_Coarse grained',
    'GRAINSIZE2_Cryptocrystalline',
    'GRAINSIZE2_Fine grained',
    'GRAINSIZE2_Medium grained',
    'GRAINSIZE2_Pegmatitic',
    # 'Alteration_dummies_50%-90%',
    # 'Alteration_dummies_>90%',
    'Veins',
    'Serpentine vein',
    'Oxidation',
    'Carbonate veins',
    'Network',
    'Dyke',
    'Black serpentinization',
    'White veins',
    'Open cracks',
    'Dunite',
    'Gabbro',
    'Microgabbro',
    'Green veins',
    'Open crack',
    'Irregular',
    'Waxy green',
    'Alteration',
    'Subvertical',
    'Fine grained',
    'Subhorizontal',
    'Lineation',
    'Magnetite',
    'Thickness',
    'Harzburgite',
    'Altered gabbro',
    'Offset',
    'Altered',
    'Crack',
    'Pxenites',
    'Microbio sample',
    'Bulk serp',
    'Bulk',
    'Coalescence',
    'Waxy',
    'Wavy',
    'Slickensides',
    'Alteration halo',
    'Plagioclase',
    'Fracture',
    'Sheared',
    'Pyroxenite',
    'Striations',
    'Branching',
    'Blue patches',
    'Magmatic intrusions',
    'Hydrothermal',
    'Rodingite',
    'Magmatic veins',
    'Offsets',
    'Shearing',
    'Dark green',
    'Dunitic zone',
    'SiO2',
    'TiO2',
    'Al2O3',
    'Fe2O3t',
    'MnO',
    'MgO',
    'CaO',
    'Na2O',
    'K2O',
    'P2O5',
    '100*Fe(III)/FeT',
    'Vrecal',
    'Crrecal',
    'Co',
    'Nirecal',
    'Curecal',
    'Znrecal',
    'Srrecal',
    'Redness',
    'Greenness',
    'Blueness',
    'Y (luminance)']

geo_comp = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3t', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5', '100*Fe(III)/FeT'
            , 'Vrecal', 'Crrecal', 'Co', 'Nirecal', 'Curecal', 'Znrecal', 'Srrecal']

physical_props = ['Mean dry electrical Resistivity (ohmm)', 'AMS bulk susceptibility'
                  , 'LOI wt%', 'CO2 wt%', 'H20 wt%', 'CaCO3 calc']

bio = ['Cell abundance (cells/g)',]

fractures = ['% of fractures', 'PnS2_sum', 'PnL_sum', 'PnP3V_sum', 'PnP3H_sum', 'PnP4_sum', 'PnP6V_sum'
             , 'FnS2_sum', 'FnL_sum', 'FnP3V_sum', 'FnP3H_sum', 'FnP4_sum', 'FnP6V_sum']

rock_type = ['UNIT_TYPE_Dunite', 'UNIT_TYPE_Fault rock', 'UNIT_TYPE_Gabbro', 'UNIT_TYPE_Harzburgite'
             , 'UNIT_TYPE_Metagabbro', 'UNIT_TYPE_Other', 'UNIT_CLASS_OPHIO', 'UNIT_CLASS_UND']

textural = ['TEXTURES_Brecciated', 'TEXTURES_Sheared', 'GRAINSIZE_Cryptocrystalline', 'GRAINSIZE_Fine grained'
            , 'GRAINSIZE_Medium grained', 'GRAINSIZE_Microcrystalline', 'GRAINSIZE2_Coarse grained'
            , 'GRAINSIZE2_Cryptocrystalline', 'GRAINSIZE2_Fine grained', 'GRAINSIZE2_Medium grained', 'GRAINSIZE2_Pegmatitic']

color_viz = ['Redness', 'Greenness', 'Blueness', 'Y (luminance)']

chatgpt = [ 'Veins',
 'Serpentine vein',
 'Oxidation',
 'Carbonate veins',
 'Network',
 'Dyke',
 'Black serpentinization',
 'White veins',
 'Open cracks',
 'Dunite',
 'Gabbro',
 'Microgabbro',
 'Green veins',
 'Open crack',
 'Irregular',
 'Waxy green',
 'Alteration',
 'Subvertical',
 'Fine grained',
 'Subhorizontal',
 'Lineation',
 'Magnetite',
 'Thickness',
 'Harzburgite',
 'Altered gabbro',
 'Offset',
 'Altered',
 'Crack',
 'Pxenites',
 'Microbio sample',
 'Bulk serp',
 'Bulk',
 'Coalescence',
           'Waxy',
 'Wavy',
 'Slickensides',
 'Alteration halo',
 'Plagioclase',
 'Fracture',
 'Sheared',
 'Pyroxenite',
 'Striations',
 'Branching',
 'Blue patches',
 'Magmatic intrusions',
 'Hydrothermal',
 'Rodingite',
 'Magmatic veins',
 'Offsets',
 'Shearing',
 'Dark green',
 'Dunitic zone',]

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

def meow_reg(df, X_cols, Y_col):
    """
    trains catboost regressor for data 
    """
    # print(X_cols)

    X = df[X_cols]
    y = df[Y_col]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_pool = Pool(X_train, y_train)
    eval_pool = Pool(X_test, y_test)
    
    # Instantiate the CatBoost regressor
    catboost_reg = CatBoostRegressor(iterations=1000, learning_rate=0.1, depth=6, loss_function='RMSE')
    
    # Fit the model to the training data
    catboost_reg.fit(X_train, y_train, eval_set=eval_pool, verbose=100, early_stopping_rounds=10)
    
    # Predict on the test data
    y_pred = catboost_reg.predict(X_test)
    
    # Calculate the Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    print('r2 score:', r2_score(y_test, y_pred))
    print('\n')
    return catboost_reg


if __name__=='__main__':

    print(xvars)
    df = import_dataset()
    # print(df.head())
    print('-------- everything --------')
    meow_reg(df=df, X_cols=xvars, Y_col='Bulk density (g/cm³)')

    print('\n############ CHATGPT SELECTED ##############\n')    
    print('-------- geo --------')
    meow_reg(df=df, X_cols=geo_comp, Y_col='Bulk density (g/cm³)')
    
    print('-------- physics --------')
    meow_reg(df=df, X_cols=physical_props, Y_col='Bulk density (g/cm³)')
    
    print('-------- bio --------')
    meow_reg(df=df, X_cols=bio, Y_col='Bulk density (g/cm³)')
    
    print('-------- fractures --------')
    meow_reg(df=df, X_cols=fractures, Y_col='Bulk density (g/cm³)')
    
    print('-------- rock type --------')
    meow_reg(df=df, X_cols=rock_type, Y_col='Bulk density (g/cm³)')
    
    print('-------- textural --------')
    meow_reg(df=df, X_cols=textural, Y_col='Bulk density (g/cm³)')
    
    print('-------- colorviz --------')
    meow_reg(df=df, X_cols=color_viz, Y_col='Bulk density (g/cm³)')
    
    print('-------- chatgpt ---------')
    meow_reg(df=df, X_cols=chatgpt, Y_col='Bulk density (g/cm³)')

    print('######## PERSON SELECTED ##########\n')
    chemistry_biology = ['Cell abundance (cells/g)','LOI wt%',
     'CO2 wt%',
     'H20 wt%',
     'CaCO3 calc',
    'SiO2',
     'TiO2',
     'Al2O3',
     'Fe2O3t',
     'MnO',
     'MgO',
     'CaO',
     'Na2O',
     'K2O',
     'P2O5',
     '100*Fe(III)/FeT',
    ]
    print('---catboost for chemistry and biology---')
    cb = meow_reg(df=df, X_cols=chemistry_biology, Y_col='Bulk density (g/cm³)')
    
    fractures = ['% of fractures',
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
     'FnP6V_sum',]
    print('---catboost for fractures---')
    frac = meow_reg(df=df, X_cols=fractures, Y_col='Bulk density (g/cm³)')
    
    geology = ['UNIT_TYPE_Dunite',
     'UNIT_TYPE_Fault rock',
     'UNIT_TYPE_Gabbro',
     'UNIT_TYPE_Harzburgite',
     'UNIT_TYPE_Metagabbro',
     'UNIT_TYPE_Other',
     'UNIT_CLASS_OPHIO',
     'UNIT_CLASS_UND',
     'TEXTURES_Brecciated',
     'TEXTURES_Sheared',
     'GRAINSIZE_Cryptocrystalline',
     'GRAINSIZE_Fine grained',
     'GRAINSIZE_Medium grained',
     'GRAINSIZE_Microcrystalline',
     'GRAINSIZE2_Coarse grained',
     'GRAINSIZE2_Cryptocrystalline',
     'GRAINSIZE2_Fine grained',
     'GRAINSIZE2_Medium grained',
     'GRAINSIZE2_Pegmatitic',]
    print('---catboost for geology---')
    geo = meow_reg(df=df, X_cols=geology, Y_col='Bulk density (g/cm³)')
    
    physics = ['Mean dry electrical Resistivity (ohmm)',
     'AMS bulk susceptibility',]
    print('---catboost for physics---')
    phys = meow_reg(df=df, X_cols=physics, Y_col='Bulk density (g/cm³)')
    
    chatgpt = [ 'Veins',
     'Serpentine vein',
     'Oxidation',
     'Carbonate veins',
     'Network',
     'Dyke',
     'Black serpentinization',
     'White veins',
     'Open cracks',
     'Dunite',
     'Gabbro',
     'Microgabbro',
     'Green veins',
     'Open crack',
     'Irregular',
     'Waxy green',
     'Alteration',
     'Subvertical',
     'Fine grained',
     'Subhorizontal',
     'Lineation',
     'Magnetite',
     'Thickness',
     'Harzburgite',
     'Altered gabbro',
     'Offset',
     'Altered',
     'Crack',
     'Pxenites',
     'Microbio sample',
     'Bulk serp',
     'Bulk',
     'Coalescence',
               'Waxy',
     'Wavy',
     'Slickensides',
     'Alteration halo',
     'Plagioclase',
     'Fracture',
     'Sheared',
     'Pyroxenite',
     'Striations',
     'Branching',
     'Blue patches',
     'Magmatic intrusions',
     'Hydrothermal',
     'Rodingite',
     'Magmatic veins',
     'Offsets',
     'Shearing',
     'Dark green',
     'Dunitic zone',]
    print('---catboost for chatgpt---')
    gpt = meow_reg(df=df, X_cols=chatgpt, Y_col='Bulk density (g/cm³)')
    
    other = ['Vrecal',
     'Crrecal',
     'Co',
     'Nirecal',
     'Curecal',
     'Znrecal',
     'Srrecal',
     'Redness',
     'Greenness',
     'Blueness',
     'Y (luminance)']
    print('---catboost for other---')
    oth = meow_reg(df=df, X_cols=other, Y_col='Bulk density (g/cm³)')

    models = [cb, frac, geo, phys, gpt, oth]
    vars = [chemistry_biology, fractures, geology, physics, chatgpt, other]

    print('plotting residuals')
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(1, len(models), figsize=(5*len(models), 5), sharex=True, sharey=True)
    
    ax[0].set_ylabel('Predicted Bulk Density')
    for a in ax:
        a.set_xlabel('True Bulk Density')
    ax[0].set_title('Chemistry and Biology')
    ax[1].set_title('Fractures')
    ax[2].set_title('Geology')
    ax[3].set_title('Physics')
    ax[4].set_title('ChatGPT')
    ax[5].set_title('Other')
    
    ytrue = df['Bulk density (g/cm³)'].values
    
    for n, a in enumerate(ax):
        ypred = models[n].predict(df[vars[n]])
        a.scatter(ytrue, ypred)
    
    fig.tight_layout()
    fig.savefig('residuals.pdf', bbox_inches='tight')

    