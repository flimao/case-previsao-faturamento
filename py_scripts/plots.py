
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

def dados_faltantes(tswide: pd.DataFrame, produtos: List = None) -> None:
    """Function to greet

    Parameters
    ----------
    tswide : pandas.DataFrame
        timeseries in wide format, per product

    """

    if produtos is None:
        produtos = tswide.columns
        n_produtos = produtos.shape[0]
    
    else:
        n_produtos = len(produtos)

    fig, axs = plt.subplots(nrows = n_produtos, ncols = 1, sharex = True, figsize = (10, 10))

    for i, produto in enumerate(produtos):
        data_full = tswide[produto]
        data_missings = data_full[data_full.isna()]
        
        ax = axs[i]
        sns.scatterplot(data = data_full, ax = ax, color = 'gray', alpha = 0.5)
        if data_missings.shape[0] > 0:
            for x in data_missings.index:
                ax.axvline(x = x, color = 'red')

        ax.set_title(f"Produto: '{produto}'")
        ax.set_ylabel('Faturamento')

    fig.suptitle('Dados faltantes', color = 'red', fontweight = 1000)
    plt.tight_layout()
    plt.show()

def decomp_fourier(serie_fat: pd.Series, produto: str, c: str) -> object:
    decomp = seasonal_decompose(serie_fat)

    fig, axs = plt.subplots(nrows = 4, figsize = (10, 8), sharex = True)

    ts_filtro = serie_fat

    sns.lineplot(data = ts_filtro, ax = axs[0], color = c)
    axs[0].set_title('Serie')
    axs[0].set_ylabel('Faturamento (R$ bi)')

    sns.lineplot(data = decomp.trend, ax = axs[1], color = c)
    axs[1].set_ylabel('R$ 100 mi')

    sns.lineplot(data = decomp.seasonal, ax = axs[2], color = c)
    axs[2].set_ylabel('R$ mi')

    resid_standard = (decomp.resid - decomp.resid.mean()) / decomp.resid.std()
    sns.scatterplot(data = resid_standard, ax = axs[3], color = c)
    axs[3].set_ylabel('Resíduos padrão')

    fig.suptitle(f"Decomposicao temporal: produto '{produto}'")
    plt.show()

    return decomp