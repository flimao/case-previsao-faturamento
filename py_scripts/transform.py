
from typing import List, Tuple
import pandas as pd

def wide2long(tswide: pd.DataFrame) -> pd.DataFrame:
    sim_ts = pd.melt(tswide.reset_index(), id_vars = 'date', var_name = 'produto', value_name = 'vlr')

    return sim_ts

def long2wide(ts: pd.DataFrame) -> pd.DataFrame:
    tswide = ts.pivot(index = 'date', values = 'vlr', columns = 'produto')

    return tswide

# pipeline de limpeza
# limpeza 1: conversão de tipos
def conversao_tipos(df):
    df = df.copy()

    df['date'] = df['date'].astype('datetime64[ns]')
    df['produto'] = df['produto'].astype('category')
    return df

# limpeza 2: setar a coluna de data como indice
def setar_indice_data(df):
    df = df.copy()

    s = df.set_index('date')['vlr']

    return s

# limpeza 3: gerar dados de meses faltantes

def gerar_dados_faltantes(s):
    s = s.copy()

    s = s.asfreq('MS')

    return s

# limpeza 4: preencher missings
def preencher_missings(s):
    s = s.copy()

    # s = s.interpolate()

    return s

def pipeline(ts_raw: pd.DataFrame) -> Tuple[dict, pd.DataFrame]:
    ts = (ts_raw
        .pipe(conversao_tipos)
    )   

    produtos = ts['produto'].cat.categories

    tsd = {}
    for produto in produtos:
        ts_produto = ts[ts['produto'] == produto]

        # finalizar limpeza para Series dentro do dicionário
        s_prod = (ts_produto
            .pipe(setar_indice_data)
            .pipe(gerar_dados_faltantes)
            .pipe(preencher_missings)
        )
        s_prod.name = f'faturamento_{produto}'
        tsd[produto] = s_prod

    tswide = pd.DataFrame(tsd)

    sprodtotal = tswide.sum(axis = 1)
    sprodtotal.name = 'faturamento_total'
    tsd['total'] = sprodtotal

    return tsd, tswide