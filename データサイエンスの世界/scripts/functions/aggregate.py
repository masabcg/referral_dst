# モジュールの読み込み
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib

from _config.columns import *
from _config.params import *



# num_basic_stat
def num_basic_stat(df, column):
    series = df[column]

    agg_count = series.count()
    agg_mean = series.mean()
    agg_std = series.std()
    agg_min = series.min()
    agg_q25, agg_median, agg_q75 = np.percentile(series, [25, 50, 75])
    agg_max = series.max()    

    dict_aggs = {
        'データの数': [agg_count],
        '平均値': [agg_mean],
        '標準偏差': [agg_std],
        '最小値': [agg_min],
        '第一四分位数': [agg_q25],
        '中央値': [agg_median],
        '第三四分位数': [agg_q75],
        '最大値': [agg_max]
    }

    df_aggs = pd.DataFrame(dict_aggs)
    # df_aggs.set_axis(['基本統計量'], axis=0, inplace=True)
    df_aggs = df_aggs.set_axis(['基本統計量'], axis=0)

    display(df_aggs)

# str_basic_stat
def str_basic_stat(df, column):
    series = df[column]

    agg_count = series.count()
    dict_value_counts = dict(series.value_counts())

    dict_aggs = {'データの個数': [agg_count]}

    for key in sorted(dict_value_counts):
        dict_aggs[key] = dict_value_counts[key]

    df_aggs = pd.DataFrame(dict_aggs)
    # df_aggs.set_axis(['基本統計量'], axis=0, inplace=True)
    df_aggs = df_aggs.set_axis(['基本統計量'], axis=0)
    
    display(df_aggs)


# num_visual
def num_visual(df, column, hue=None, bins=10, alpha_sc=0.1):
    fig, ax = plt.subplots(1, 2, figsize=(15, 5), facecolor=facecolor)
    # hueの設定あり    
    if hue:
        # ヒストグラム描画
        tuple_hue_unique = sorted(tuple(df[hue].unique()))
        tuple_hue_df1 = [df[df[hue] == value] for value in tuple_hue_unique]
        tuple_hue_df2 = [df[column] for df in tuple_hue_df1]

        ax[0].hist(
            tuple_hue_df2, 
            bins = bins, 
            # alpha = 1/len(tuple_hue_unique), 
            label = list(df[hue].unique()), 
            ec = 'gray'
        )

        ax[0].legend(title=hue)
        ax[0].set_title('データの分布を確認', fontsize=title_fontsize)
        ax[0].set_xlabel(column, fontsize=label_fontsize)
        ax[0].set_ylabel('データの個数', fontsize=label_fontsize)

        # 散布図描画
        list_hue_unique = sorted(list(df[hue].unique()))
        list_hue_df = [df[df[hue] == value] for value in list_hue_unique]

        for i, df_hue in enumerate(list_hue_df):
            ax[1].scatter(
                df_hue[column], 
                df_hue[amount_paid], 
                alpha=alpha_sc, 
                label=list_hue_unique[i]
            )


        ax[1].legend(title=hue)
        ax[1].set_title('電気代との相関を確認', fontsize=title_fontsize)
        ax[1].set_xlabel(column, fontsize=label_fontsize)
        ax[1].set_ylabel(amount_paid, fontsize=label_fontsize)

        plt.show()
    
    # hueの設定なし    
    else:
        # ヒストグラム描画        
        tuple_hist = tuple(df[column])

        ax[0].hist(tuple_hist, bins = bins, ec = 'gray')

        ax[0].set_title('データの分布を確認', fontsize=title_fontsize)
        ax[0].set_xlabel(column, fontsize=label_fontsize)
        ax[0].set_ylabel('データの個数', fontsize=label_fontsize)

        # 散布図描画
        tuple_scatterx = tuple(df[column])
        tuple_scattery = tuple(df[amount_paid])

        ax[1].scatter(tuple_scatterx, tuple_scattery, alpha=alpha_sc)

        ax[1].set_title('電気代との相関を確認', fontsize=title_fontsize)
        ax[1].set_xlabel(column, fontsize=label_fontsize)
        ax[1].set_ylabel(amount_paid, fontsize=label_fontsize)

        plt.show()


# str_visual
def str_visual(df, column, hue=None, fontsize=14):
    fig, ax = plt.subplots(1, 2, figsize=(15, 5), facecolor=facecolor)

    # hueの設定あり        
    if hue:
        # 棒グラフ描画
        list_hue_unique = sorted(list(df[hue].unique()))
        list_hue_df = [df[df[hue] == value] for value in list_hue_unique]

        list_hue_barx = [sorted(list(df_hue[column].unique())) for df_hue in list_hue_df]
        list_hue_bary = [[len(df_hue[df_hue[column]==value]) for value in list_barx] for list_barx, df_hue in zip(list_hue_barx, list_hue_df)]

        zip_bar = zip(
            list_hue_barx, 
            list_hue_bary, 
            [-0.3, 0.3], 
            list_hue_unique
                     )

        for list_barx, list_bary, width, hue_tmp in zip_bar:
            ax[0].bar(
                list_barx, 
                list_bary, 
                align='edge', 
                width=width, 
                label=hue_tmp, 
                ec='gray'
            )

        ax[0].legend(title=hue)


        ax[0].set_title('データの分布を確認', fontsize=title_fontsize)
        ax[0].set_xlabel(column, fontsize=label_fontsize)
        ax[0].set_xticks([i for i in range(len(list_hue_barx[0]))])   # warning回避
        ax[0].set_xticklabels(list_hue_barx[0], fontsize=fontsize)
        ax[0].set_ylabel('データの個数', fontsize=label_fontsize)

        # 箱ひげ図描画

        sns.boxplot(x=column, y=amount_paid, hue=hue, data=df)

        ax[1].set_title('電気代との関係を確認', fontsize=title_fontsize)
        ax[1].set_xlabel(column, fontsize=label_fontsize)
        ax[1].set_xticks([i for i in range(len(list_barx))])   # warning回避
        ax[1].set_xticklabels(list_barx, fontsize=fontsize)
        ax[1].set_ylabel(amount_paid, fontsize=label_fontsize)

        plt.show()
        
    # hueの設定なし
    else:
        # 棒グラフ描画
        list_barx = sorted(list(df[column].unique()))
        list_bary = [len(df[df[column]==value]) for value in list_barx]

        ax[0].bar(list_barx, list_bary, ec='gray')

        ax[0].set_title('データの分布を確認', fontsize=title_fontsize)
        ax[0].set_xlabel(column, fontsize=label_fontsize)
        ax[0].set_xticks([i for i in range(len(list_barx))])   # warning回避
        ax[0].set_xticklabels(list_barx, fontsize=fontsize)
        ax[0].set_ylabel('データの個数', fontsize=label_fontsize)
        
        # 箱ひげ図描画
        sns.boxplot(x=column, y=amount_paid, data=df)

        ax[1].set_title('電気代との関係を確認', fontsize=title_fontsize)
        ax[1].set_xlabel(column, fontsize=label_fontsize)
        ax[1].set_xticks([i for i in range(len(list_barx))])   # warning回避
        ax[1].set_xticklabels(list_barx, fontsize=fontsize)
        ax[1].set_ylabel(amount_paid, fontsize=label_fontsize)

        plt.show()
        
        
# aggregate_display
def aggregate_display(df, column, hue=None, bins=10, alpha_sc=0.1):
    if cols_dtypes[column] == int:
        # 基本統計量表示
        num_basic_stat(df=df, column=column) 
        # グラフ表示
        num_visual(df=df, column=column, hue=hue, bins=bins, alpha_sc=alpha_sc)

    elif cols_dtypes[column] == str:
        # 基本統計量表示
        str_basic_stat(df=df, column=column) 
        # グラフ表示
        str_visual(df=df, column=column, hue=hue)