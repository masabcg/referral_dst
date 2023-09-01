import lightgbm as lgb


encoding = 'utf8'
seed = 1234
target = 'amount_paid'
path_workdir = '/Users/anz.cafe/Documents/会社/2023/230902_リファラルイベント/src'

# path
path_agg = './input/agg_Household_energy.csv'
path_ml = './input/ml_Household energy.csv'

# 可視化関連
facecolor = 'lightblue'
# color = 
title_fontsize = 18
label_fontsize = 16

## LightGBM関連
params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'regression', # 目的 : 回帰  
    'metric': {'rmse'}, # 評価指標 : rmse(平均二乗誤差の平方根) 
    'learning_rate': 0.1,
    'num_leaves': 23,
    'min_data_in_leaf': 1,
    'num_iteration': 1000, #1000回学習
    'verbose': 0
}

# early_stopping
verbose_eval = 0
callbacks = [lgb.early_stopping(
    stopping_rounds=100, 
    verbose=True
                             ), # early_stopping用コールバック関数
    lgb.log_evaluation(verbose_eval)
            ] # コマンドライン出力用コールバック関数
