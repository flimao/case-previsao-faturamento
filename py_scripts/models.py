#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from typing import List, Tuple
import pandas as pd
import numpy as np
import datetime as dt
import py_scripts.transform
import pickle

MODELSDIR = r'../models'
DATASET = r'../data/sim_ts_limpo.csv'

class modelo_produtos:
    """ encapsulador para os modelos de cada produto """

    def __init__(self, dataset: str = DATASET, modelsdir: str = MODELSDIR):
        self.dataset = dataset
        self.modelsdir = modelsdir

        # importanto dados limpos
        ts_raw = pd.read_csv(self.dataset)
        tsd, self.tswide = py_scripts.transform.pipeline(ts_raw)

        # produtos
        self.produtos = self.tswide.columns

        # importar modelos
        self.modelo, self.serie_treino = self.importar_modelos()

        self.fat_total = self.tswide.sum(axis = 'columns')

    def importar_modelos(self):

        modelo = {}
        serie_treino = {}

        for produto in self.produtos:
            produto_  = produto.split('_')[0]

            picklefile = fr'produto_{produto_}.model'
            picklefn = os.path.join(os.path.abspath(self.modelsdir), picklefile)

            with open(picklefn, 'rb') as modelo_arq:
                unpickler = pickle.Unpickler(modelo_arq)
                modelo_dict = unpickler.load()
                modelo[produto] = modelo_dict['modelo']
                serie_treino[produto] = modelo_dict['serie_treino']
            
        return modelo, serie_treino        

    def get_models(self):
        return self.modelo, self.serie_treino
    
    def get_test_begin(self, produtos: List or None = None):
        
        if produtos is None:
            produtos = self.produtos

        serie_treino_prods = { p: s for p, s in self.serie_treino.items() if p in produtos }

        train_end = pd.Series(
            [ v.index[-1] for v in serie_treino_prods.values() ],
            index = produtos
        )

        test_start = train_end + pd.offsets.MonthBegin(1)

        return test_start

    def get_all_test_begin(self):
        
        train_end = max([ v.index[-1] for v in self.serie_treino.values() ])

        test_start = train_end + pd.offsets.MonthBegin(1)

        return test_start

    def predict(self, n_periods: int, return_conf_int: bool = False,  
        predict_array: bool = True,
        *args, **kwards
    ) -> pd.Series or pd.DataFrame or np.array or Tuple[np.array, np.array]:

        if n_periods <= 0:
            raise ValueError('Can only predict forward!')

        # construimos um dataframe onde ficar??o as predi????es individuais
        preds = pd.DataFrame([], columns = self.produtos)

        if return_conf_int:
            colsmult = pd.MultiIndex.from_product((self.produtos, ['lb', 'ub']))
            preds_ci = pd.DataFrame([], columns = colsmult)

        # obtemos a maior data em todos os conjuntos de treino

        max_train_right_bound = max([ v.index[-1] for v in self.serie_treino.values() ])

        for produto in self.produtos:
            # maior data de cada conjunto de treino
            train_right_bound = self.serie_treino[produto].index[-1]

            # construimos o ??ndice de datas do conjunto de teste de cada produto: 
            # range entre m??s ap??s o ??ltimo contido no conjunto de treino e 
            idx_test = pd.date_range(
                start = train_right_bound + dt.timedelta(days = 1), 
                end = max_train_right_bound + pd.offsets.MonthBegin(n_periods), freq = 'MS')

            # geramos a predi????o para cada produto. Essa predi????o vem em um np.array
            # como queremos o intervalo de confian??a, o resultado da fun????o ?? uma tupla com
            #    - o array da predi????o m??dia
            #    - um array com duas colunas contendo o lower bound e o upper bound
            arr_pred_all = self.modelo[produto].predict(n_periods = idx_test.shape[0], return_conf_int = return_conf_int)

            # primeiro trataremos das m??dias
            if return_conf_int:
                arr_pred = arr_pred_all[0]
            else:
                arr_pred = arr_pred_all
            
            # convertemos o array para Series
            pred = pd.Series(arr_pred, index = idx_test)
            pred.name = 'predicted_mean'

            # adicionamos a Series ao DataFrame `preds`
            preds[produto] = pred

            # agora trabalharemos nos bounds
            if return_conf_int:
                arr_pred_ci = arr_pred_all[1]

                pred_ci = pd.DataFrame(
                    arr_pred_ci, 
                    columns = pd.MultiIndex.from_product(((produto, ), ('lb', 'ub'))), 
                    index = idx_test
                )


                preds_ci[pred_ci.columns] = pred_ci

        preds_series = preds.dropna().sum(axis = 'columns')
        preds_series.name = 'predicted_mean'

        if return_conf_int:
            fat_test = pd.DataFrame([])

            fat_test['predicted_mean'] = preds_series

            fat_test['lb'] = preds_ci.loc[:, (slice(None), 'lb')].dropna().sum(axis = 'columns')
            fat_test['ub'] = preds_ci.loc[:, (slice(None), 'ub')].dropna().sum(axis = 'columns')
            
            if predict_array:
                return (
                    fat_test['predicted_mean'].values,
                    fat_test[['lb', 'ub']].values
                )
            else:
                return fat_test
        
        else:
            if predict_array:
                return preds_series.values
            else:
                return preds_series

    def __str__(self):
        totalstr = 'Modelos:'

        tamanho_campo = max([ len(produto) for produto in self.produtos ]) + 4

        for produto, modelo in self.modelo.items():
            totalstr += f"\n{produto:>{tamanho_campo}s}: {modelo}"
        
        return totalstr
    
    def __repr__(self):
        return str(self.modelo)