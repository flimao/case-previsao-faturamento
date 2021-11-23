import nbformat
#%%
notebook_filenames = [
    r'../notebooks_exploration/1-previsao_faturamento_preproc.ipynb',
    r'../notebooks_exploration/2-faturamento_total.ipynb',
    r'../notebooks_models/total_arima.ipynb',
    r'../notebooks_exploration/3-produto_alimenticio.ipynb',
    r'../notebooks_models/produto_alimenticio_arima.ipynb',
    r'../notebooks_exploration/4-produto_transporte.ipynb',
    r'../notebooks_models/produto_transporte_arima.ipynb',
    r'../notebooks_exploration/5-produto_saude.ipynb',
    r'../notebooks_models/produto_saude_arima.ipynb',
    r'../notebooks_exploration/6-produto_auxilio.ipynb',
    r'../notebooks_models/produto_auxilio_arima.ipynb',
    r'../notebooks_exploration/7-produto_bonificacao.ipynb',
    r'../notebooks_models/produto_bonificacao_arima.ipynb',
    r'../notebooks_models/todos_produtos_arima.ipynb',
    r'../notebooks_exploration/8-comparacao.ipynb',
]

notebooks = [
    nbformat.read(fn, 4)
    for fn in notebook_filenames
]

#%%
one_notebook = nbformat.v4.new_notebook(metadata = notebooks[0].metadata)

notebook_cells = [ notebook.cells for notebook in notebooks ]

one_notebook.cells = notebook_cells[0]
for cell in notebook_cells[1:]:
    one_notebook.cells += cell

nbformat.write(one_notebook, r'../previsao-faturamento.ipynb')


# %%
