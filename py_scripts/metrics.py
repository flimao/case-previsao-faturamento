import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error as smape, \
                            mean_squared_error as smse, \
                            mean_absolute_error as smae, \
                            r2_score as sr2

from pmdarima.arima.arima import ARIMA

def mostrar_metricas(y_true: pd.Series, y_pred: pd.Series, n: int = None, dof: int = None, *args, **kwargs) -> None:
    mape = smape(*args, y_true = y_true, y_pred = y_pred, **kwargs)
    rmse = smse(*args, y_true = y_true, y_pred = y_pred, squared = False, **kwargs)
    mae = smae(*args, y_true = y_true, y_pred = y_pred, **kwargs)

    r2 = sr2(*args, y_true = y_true, y_pred = y_pred, **kwargs)

    if n is not None and dof is not None and n - dof > 1:
        adj_r2 = 1 - (1-r2)*(n - 1) / (n - dof - 1)
    else:
        adj_r2 = None

    print('Métricas:')
    print(f'    MAPE: {mape:.3%}')
    print(f'    RMSE: {rmse:.3e}')
    print(f'     MAE: {mae:.3e}')
    print(f'      R²: {r2:.3%}')

    if adj_r2 is not None:
        print(f' R² adj.: {adj_r2:.3%}')
    
    return
