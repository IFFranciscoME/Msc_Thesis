
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Project: Masters in Data Science Thesis Project                                                     -- #
# -- Statistical Learning and Genetic Methods to Design, Optimize and Calibrate Trading Systems          -- #
# -- File: document.py - python script with all the output elements for the thesis report                -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- Repository: https://github.com/IFFranciscoME/Msc_Thesis                                             -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from rich import print
from rich import inspect

import pandas as pd
import numpy as np

from data import ohlc_data as data

import functions as fn
import visualizations as vs
import data as dt

# Reproducible results
import random
random.seed(123)

# ---------------------------------------------------------------- PLOT 1: OHLC DATA PLOT (ALL DATA SET) -- #
# ---------------------------------------------------------------- ------------------------------------- -- #

# Candlestick chart for historical OHLC prices
plot_1 =vs.g_ohlc(p_ohlc=data, p_theme=dt.theme_plot_1, p_vlines=None)

# Show plot in script
# plot_1.show()

# Generate plot online with chartstudio
# py.plot(plot_1)

# ------------------------------------------------------------------------------------ LOAD RESULTS DATA -- #
# ------------------------------------------------------------------------------------ ----------------- -- #

# Fold size
fold_size = 'semester'

# Timeseries data division in t-folds
folds = fn.t_folds(p_data=data, p_period=fold_size)

# List with the names of the models
ml_models = list(dt.models.keys())

# File name to save the data
file_name = 'files/pickle_rick/respaldo/s_auc-inv-weighted_post-features_robust.dat'

# Load previously generated data
memory_palace = dt.data_save_load(p_data_objects=None, p_data_action='load', p_data_file=file_name)
memory_palace = memory_palace['memory_palace']

# -- ----------------------------------------------------------------- PLOT 2: TIME SERIES BLOCK T-FOLDS -- #
# -- ----------------------------------------------------------------- --------------------------------- -- #

# Dates for vertical lines in the T-Folds plot
dates_folds = []
for n_fold in list(folds.keys()):
    dates_folds.append(folds[n_fold]['timestamp'].iloc[0])
    dates_folds.append(folds[n_fold]['timestamp'].iloc[-1])

# Plot_1 with t-folds vertical lines
plot_2 = vs.g_ohlc(p_ohlc=data, p_theme=dt.theme_plot_2, p_vlines=dates_folds)

# Show plot in script
# plot_2.show()

# Generate plot online with chartstudio
# py.plot(plot_2)

# ----------------------------------------------------------------------------------------- DATA PROFILE -- #
# ----------------------------------------------------------------------------------------- ------------ -- #

# period to explore results
period = list(folds.keys())[0]

# ------------------------------------------------------------------------------------------- input data -- # 

# all the input data
in_profile = memory_palace[period]['metrics']['data_metrics']

# -------------------------------------------------------------------------------------- target variable -- #

# train and test data sets with only target variable
tv_profile_train = memory_palace[period]['metrics']['feature_metrics']['train_y']
tv_profile_test = memory_palace[period]['metrics']['feature_metrics']['test_y']

# ------------------------------------------------------------------------------------- linear variables -- #
# amount of symbolic features
n_sf = dt.symbolic_params['n_features']

# train and test data sets with only autoregressive variables
lf_profile_train = memory_palace[period]['metrics']['feature_metrics']['train_x'].iloc[:, :-n_sf]
lf_profile_test = memory_palace[period]['metrics']['feature_metrics']['test_x'].iloc[:, :-n_sf]

# ------------------------------------------------------------------------------------ symbolic variables -- #

# train and test data sets with only symbolic variables
sm_profile_train = memory_palace[period]['metrics']['feature_metrics']['train_x'].iloc[:, -n_sf:]
sm_profile_test = memory_palace[period]['metrics']['feature_metrics']['test_x'].iloc[:, -n_sf:]

# ---------------------------------------------------------------------------------------- All variables -- #

# correlation among all variables
all_corr_train = memory_palace[period]['features']['train_x'].corr()
all_corr_test = memory_palace[period]['features']['test_x'].corr()

# correlation of all variables with target variable
tgv_corr_train = pd.concat([memory_palace[period]['features']['train_y'],
                            memory_palace[period]['features']['train_x']], axis=1).corr().iloc[:, 0]
tgv_corr_test = pd.concat([memory_palace[period]['features']['test_y'],
                           memory_palace[period]['features']['test_x']], axis=1).corr().iloc[:, 0]

# --------------------------------------------------------------------------------------- VISUAL PROFILE -- #
# ----------------------------------------------------------------------------------------- ------------ -- #

# (pending)

# -- ------------------------------------------------------------------------------- PARAMETER SET CASES -- #
# -- ------------------------------------------------------------------------------- ------------------- -- #

# models to explore results
model = list(dt.models.keys())[2]

# -- Min, max and mode cases
met_cases = fn.model_cases(p_models=ml_models, p_global_cases=memory_palace, p_data_folds=folds,
                           p_cases_type='logloss-inv-weighted')
 
# periods of the mode(s)
mode_periods = met_cases[model]['met_mode']['period']

# whole data of repetitions
mode_repetitions = pd.DataFrame(met_cases[model]['met_mode']['data']).T

# -- ------------------------------------------------------------------------ SYMBOLIC FEATURES ANALYSIS -- #
# -- ------------------------------------------------------------------------ -------------------------- -- #

# data
sym_data = met_cases[model]['hof_metrics']['data']['s_01_2011']['features']['sym_features']

# parsimony metrics
# sym_data['best_programs']['depth']
# sym_data['best_programs']['length']

# fitness metric
# sym_data['best_programs']['fitness']

# -- --------------------------------------------------------------- PLOT 3: CLASSIFICATION FOLD RESULTS -- #
# -- ----------------------------------------------------------------------------- --------------------- -- #

# Pick case
case = 'met_max'

# Pick model to generate the plot
case_model = 'logistic-elasticnet'

# Generate title
plot_title = 'inFold ' + case + ' for: ' + case_model + met_cases[case_model]['met_max']['period']

# Plot title
dt.theme_plot_3['p_labels']['title'] = plot_title

# Get data from met_cases
train_y = met_cases[case_model][case]['data']['results']['data']['train']
test_y = met_cases[case_model][case]['data']['results']['data']['test']

# Get data for prices and predictions
ohlc_prices = folds[met_cases[case_model][case]['period']]
ohlc_class = {'train_y': train_y['y_train'], 'train_y_pred': train_y['y_train_pred'],
              'test_y': test_y['y_test'], 'test_y_pred': test_y['y_test_pred']}

# Make plot
plot_3 = vs.g_ohlc_class(p_ohlc=ohlc_prices, p_theme=dt.theme_plot_3, p_data_class=ohlc_class, p_vlines=None)

# Show plot in script
# plot_3.show()

# Generate plot online with chartstudio
# py.plot(plot_3)

# -- -------------------------------------------------------------------------- PLOT 4: All ROCs in FOLD -- #
# -- -------------------------------------------------------------------------- ------------------------ -- #

# metric to plot
metric = 'auc'

# metric to plot
case = 'met_max'

# Model to evaluate
model = 'l1-svm'

# data subset to use
subset = 'test'

# period 
period = 's_02_2011'

# parameters of the evaluated models
d_params = memory_palace[period][model]['p_hof']['hof']

# get all fps and tps for a particular model in a particular fold
d_plot_4 = {i: {'tpr': memory_palace[period][model]['e_hof'][i]['metrics'][subset]['tpr'],
                'fpr': memory_palace[period][model]['e_hof'][i]['metrics'][subset]['fpr'],
                'auc': memory_palace[period][model]['e_hof'][i]['metrics'][subset]['auc'],
                'acc': memory_palace[period][model]['e_hof'][i]['metrics'][subset]['acc'],
                'logloss': memory_palace[period][model]['e_hof'][i]['metrics'][subset]['logloss']}
            for i in range(0, len(d_params))}

# Plot title
dt.theme_plot_4['p_labels']['title'] = 'in Fold max & min ' + metric + ' ' + subset + ' data'

# Timeseries of the AUCs
plot_4 = vs.g_multiroc(p_data=d_plot_4, p_metric=metric, p_theme=dt.theme_plot_4)

# Show plot in script
# plot_4.show()

# Generate plot online with chartstudio
# py.plot(plot_4)

# -- --------------------------------------------------------------------------------- GLOBAL EVALUATION -- #
# -- --------------------------------------------------------------------------------- ----------------- -- #

# metric to plot
metric = 'auc'

# metric to plot
case = 'met_max'

# Model to evaluate
model = 'ann-mlp'

# data subset to use
subset = 'train'

# period 
period = 's_02_2011'

# Function
global_model = fn.global_evaluation(p_memory_palace=memory_palace, p_data=data, p_cases=met_cases, 
                                    p_model=model, p_case=case, p_metric=metric)

# Model parameters
global_model['global_parameters']

# Model auc
global_model['model']['metrics']['train']['auc']

# Model accuracy
global_model['model']['metrics']['train']['acc']

# -- ------------------------------------------------------------- PLOT 5: GLOBAL CLASSIFICATION RESULTS -- #
# -- ------------------------------------------------------------- ------------------------------------- -- #

# Get data for prices and predictions
ohlc_prices = data

ohlc_class = {'train_y': global_model['model']['results']['data']['train']['y_train'],
              'train_y_pred': global_model['model']['results']['data']['train']['y_train_pred'],
              'test_y': global_model['model']['results']['data']['test']['y_test'],
              'test_y_pred': global_model['model']['results']['data']['test']['y_test_pred']}

# Plot title
dt.theme_plot_3['p_labels']['title'] = 'Global results with t-fold optimized parameters'

# Make plot
plot_5 = vs.g_ohlc_class(p_ohlc=ohlc_prices, p_theme=dt.theme_plot_3, p_data_class=ohlc_class, p_vlines=None)

# Show plot in script
# plot_5.show()

# Generate plot online with chartstudio
# py.plot(plot_5)
