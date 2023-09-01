import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import lightgbm as lgb

from _config.columns import *
from _config.params import *


class lgbm_build:
    def __init__(self, df, target, params):
        self.df = df
        self.target = target
        self.params = params
        
        ## データの分割
        # 説明変数、目的変数に分割
        X = df.drop(target, axis=1)
        y = df[target]

        # 学習、検証、評価用にデータを分割
        X_train_valid, X_test, y_train_valid, y_test = train_test_split(X, y,test_size=0.20, random_state=seed)
        X_train, X_valid, y_train, y_valid = train_test_split(X_train_valid, y_train_valid, test_size=0.25, random_state=seed)

        ## モデルの学習
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_valid = lgb.Dataset(X_valid, y_valid, reference=lgb_train)
        
        self.model = lgb.train(
            params, 
            train_set=lgb_train, 
            valid_sets=lgb_valid, 
            callbacks=callbacks
        )

        # 他の関数でも使うのでクラス内変数とする
        self.X_test = X_test
        self.y_test = y_test

    
    ### 予測結果を表示・可視化
    ## 評価指標を表示
    def pred_eval(self, s=0, e=-1):
        # テストデータの予測
        y_pred = self.model.predict(self.X_test)

        # rmse : 平均二乗誤差の平方根
        print('【評価指標の確認】')
        mse = mean_squared_error(self.y_test, y_pred) # MSE(平均二乗誤差)の算出
        rmse = np.sqrt(mse) # RSME = √MSEの算出
        print('RMSE :',rmse)
        
        #　r2 : 決定係数
        r2 = r2_score(self.y_test,y_pred)
        print('R2 :',r2)
        
        # 実測値と予測値の表示
        df_pred = pd.DataFrame({'電気代_実測値':self.y_test,'電気代_予測値':y_pred})
        display(df_pred.iloc[s: e])



    # yyplotの可視化
    def yyplot_visual(self):
        # テストデータの予測
        y_pred = self.model.predict(self.X_test)
        
        # 散布図を描画(真値 vs 予測値)
        fig, ax = plt.subplots(figsize=(6, 6), facecolor=facecolor)
        
        plt.plot(self.y_test, self.y_test, color = 'red') # 直線y = x (真値と予測値が同じ場合は直線状に点がプロットされる)
        plt.scatter(self.y_test, y_pred) # 散布図のプロット
        plt.xlabel('電気代_実測値') # x軸ラベル
        plt.ylabel('電気代_予測値') # y軸ラベル
        plt.title('実測値と予測値のズレを確認') # グラフタイトル
        
        plt.show()        


    # 変数重要度の可視化
    def feature_importance(self):
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=facecolor)
        lgb.plot_importance(self.model, ax=ax)

        ax.set_title('AIが重要視した説明変数を確認')
        ax.set_xlabel('変数重要度')
        ax.set_ylabel('説明変数')
        ax.grid(False)
        
        plt.show()