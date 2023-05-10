# Esse projeto visa entender quais campanhas de marketing tiveram sucesso no dataset do kaggle
# As principais perguntas a serem respondidas constam no link https://www.kaggle.com/code/jennifercrockett/marketing-analytics-eda-task-final/notebook
# Código desenvolvido no VSCode 
# Caso queira reproduzir este código, deixe a referência do meu github ao final

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Importando o dataset
df=pd.read_csv('D:\Bruna\Desktop\Área de Trabalho Antiga\BRUNA\Cursos\Programação\Python\datasets\marketing_data.csv')

# Configurações
plt.style.use('ggplot')
pd.set_option('display.max_rows',20)
pd.set_option('display.max_columns',40)

#Primeira análise do dataset

#Mostra as cinco primeiras linhas
print(df.head())

# Mostra as labels das colunas
print(df.columns)

# Mostra informações de nome_coluna das colunas, valores não nulos e tipo de dado
print(df.info())

# Amostra de 10 valores dos dados
print(df.sample(10))


# Mostrar quantos valores unicos tem
df.nunique().sort_values()
# Convertendo dados para uso de memória mais eficiente
# Valores até 127 int8, 32000 int16, 2 bilhoes int32
print(df.max())



#%%

# Substituindo tipos das colunas de acordo com os tamanhos dos dados
colunas=df.columns
colunas_str=[]
for i in colunas:
    coluna=df[i]
    nome_coluna=str(i)
    if coluna.dtype == 'int64' :
        if int(coluna.max()) <127:
            print('primeiro if',coluna.max())
            df[nome_coluna] = df[nome_coluna].astype('int8')
        elif int(coluna.max()) < 32000 :
            print('segundo if',coluna.max())
            df[nome_coluna] = df[nome_coluna].astype('int16')
        else:
            df[nome_coluna] = df[nome_coluna].astype('int32')

# Com essas mudanças, o tamanho do arquivo foi de 400 kb para 155 kb, uma redução de 61%
#%%
from summarytools import dfSummary

# Resumo de valores de todas as colunas
dfSummary(df)
# %%
#Checando se ha valores nan
print(df.isnull().values.any())

# Checando valores null em datas
print(df.isna())

#Vemos que a média do publico nasceu em 1970
# %%
print(df.Kidhome.value_counts(normalize=True))
#print(df.Income.value_counts(normalize=True))

## Essa linha levantou o erro Dataframe has no attribute Income, deve haver um erro no nome da coluna
## Ao observar o df.info, ve-se que a palavra Income parece identada ou com espaços, por isso, a coluna será renomeada para facilitar a análise
nome_income=colunas[4]
print(nome_income)

# Renomeia a coluna no dataframe original
df.rename(columns={' Income ':'Income'},inplace=True)
#%%
# Outro problema observado é que a coluna tem um cifrao e virgulas nos valores numericos, o que atrapalha o processamento em gráficos e operações, por isso serão retirados
df['Income']=df['Income'].str.strip('$')

# Retira o final .00 dos valores
df['Income']=df['Income'].str.slice_replace(6, repl='')

# Retira a vírgula dos valores
df['Income']=df['Income'].str.slice_replace(2, stop=3,repl='')
df['Income'] = df['Income'].astype('int32')
#df['Income']=df['Income'].astype('int32')

# Distribuição normal dos valores de renda
print(df.Income.value_counts(normalize=True))

# Distribuição normal - valores entre 0 e 1 - do numero de compras em lojas
print(df.NumStorePurchases.value_counts(normalize=True))

# %%
plt.title('Distribuição do número de compras em lojas')
plt.ylabel('Frequência',color='slategray')
plt.xlabel('Numero de compras do cliente')
plt.hist(df.NumStorePurchases,bins=14,color='mediumblue')
# %%
plt.hist(df.Year_Birth,bins=50,color='mediumblue')
# %%

# Análise de outliers
plt.figure(1)
plt.boxplot(df.Year_Birth, meanline=True)
plt.figure(2)

plt.boxplot(df.NumStorePurchases)
plt.figure(3)
#%%
plt.scatter(df['Income'])

# %%

# Testando relações entre variáveis
sns.relplot(data=df, x ='Income', y='NumStorePurchases', color='b')
sns.relplot(data=df, x = 'Year_Birth', y = 'NumStorePurchases',color='b')
# %%
