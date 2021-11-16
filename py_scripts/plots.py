
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
