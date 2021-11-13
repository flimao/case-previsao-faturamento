# Previsão do faturamento da empresa de acordo com produtos

Projeto para a disciplina de **Estatística** (Módulo 4) do Data Science Degree (turma de julho de 2020)

## Equipe

* Felipe Lima de Oliveira
* Mário Henrique Romagna Cesa
* Tsuyioshi Valentim Fukuda
* Fernando Raineri Monari

## Case

Imagine que você trabalha numa empresa de benefícios que vende diversos produtos para os RHs clientes, com o intuito de melhorar a qualidade de vida de seus colaboradores por meio de alimentação saudável, transporte, saúde, entre outros.

Para ajudar no direcionamento e estratégia corporativa, bem como definir a meta do time comercial, você ficou encarregado de prever qual seria o faturamento mensal esperado para 2022.

## Etapas de análise

### Etapa I - **EDA - Análise exploratória de dados**

1. Análise das medidas de medidas de posição, dispersão, correlação (análises univaridas e bivariadas) - histograma, boxplot, mapa de calor, etc...
2. Identificação e tratamento de outliers e missings, caso necessário (sempre explicando a opção)

### Etapa II - **Análise de séries temporais**

1. Ajuste um modelo para o faturamento total (sem quebrar por produto) e realize a projeção para os meses faltantes até o final de 2022.
2. Faça ajustes indivíduais para cada produto e consolide os resultados para obter o faturamento total para os meses faltantes até o final de 2022.
3. Qual dos dois cenários obteve a melhor projeção? Qual cenário você usaria dentro da sua empresa pensando nos desdobramentos estratégicos citados acima? Justifique a sua resposta com base em métricas bem definidas e no entendimento do problema.

## Informações sobre o dataset

* **[sim_ts.txt](sim_ts.txt)** - Série temporal sintética com os meses (a data está completa com ano, mês e dia, mas o dia é irrelevante), os valores recebidos e o produto correspondente.

### Campos

* **vlr**: Vlr. faturado no mês
* **date**: Mês de referência do faturamento
* **produto**: Produto ao qual o faturamento diz respeito
