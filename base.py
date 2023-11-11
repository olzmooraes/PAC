
# Pontos para serem abordados

# 1 - proporcionalmente a media de crimes de muriae é sempre menor que a de minas? e sempre a media foi menor? ou teve alguns anos que foram maiores?

# 2 - distribuição do numero de crimes naquela cidade

# 3 - proporcção de cidades grandes e da região comparados com os crimes de muriaé

# 4 - tornar a quantidade de crimes em porcentagem e ver a porcentagem de cada um, proporcionalmente com o numero de habitantes


# importacao

import pandas as pd
import matplotlib.pylab as plt
from html import unescape
import seaborn as sns
from matplotlib.ticker import FuncFormatter
crimes12a17 = pd.read_csv('/kaggle/input/bancodecrimes-2012a2017/BancoCrimesViolentos-Atualizado2012a2017.csv',encoding='latin1',sep=';')
crimes18a23 = pd.read_csv('/kaggle/input/bancodecrimes-2018a2023/BancoCrimesViolentosAtualizadoSetembro2023.csv',encoding='latin1',sep=';')
base = pd.read_excel('/kaggle/input/base-de-habitantes-atualizada/Base-Mg.xlsx')

# arquivos csv pode não lida bem com caracteres especiais, sempre precisamos improvisar para contornar essa situação.
# usei uma decodificação de entidades HTML para caracteres Unicode ou UTF-8.
# a função do 'unescape' do módulo html em Python é converter a entidade HTML "í" para o caractere "í" do python.
# RESUMINDO > passo uma palavra decodificada o python pergunda o 'unescape' do html como decodificar.

def decode_html(value):
    if isinstance(value, str):
        return unescape(value)
    else:
        pass
        return value

# Aplicar a função para todas as colunas
for coluna in base.columns:
    base[coluna] = base[coluna].apply(decode_html)

# promover o cabecario
# def renomearCabecario(df):
#     for i, coluna in enumerate(df.columns):
#         lista = base.values[0]
#         df = df.rename(columns={coluna : lista[i]})

#     df = df.rename(columns = {'Código [-]' : 'Cod IBGE'})
#     df = df.drop([0,df.index[-1:].values[0]])
#     return df

# base = renomearCabecario(base)
display(crimes12a17[:2])
display(crimes18a23[:2])
display(base[:2])







# municipio crimes finais

dadosBrutos = pd.concat([crimes12a17,crimes18a23])
# dadosRegistro = dadosBrutos[dadosBrutos['Registros'] > 0] & dadosBrutos[dadosBrutos['Ano'] < '2023']
dadosRegistro = dadosBrutos[(dadosBrutos['Registros'] > 0) & (dadosBrutos['Ano'] < 2023)]
municipioCrimes = dadosRegistro.groupby('Município')[['Natureza']].count()
municipioCrimesFinal = municipioCrimes.sort_values('Natureza',ascending=False)
display(municipioCrimesFinal)




#Relacionar por período( ex: de 5 em 5 anos).

# axi = range(2012,2019)
# for i,ano in enumerate(range(2017,2024)):
#     print(f'Periodo de {axi[i]} até {ano}.')
#     dadosRegistro = dadosBrutos[(dadosBrutos['Registros'] > 0) & (dadosBrutos['Ano'] >= axi[i]) & (dadosBrutos['Ano']<= ano)]
#     periodoCrimes = dadosRegistro.groupby('Município')[['Natureza']].count()
#     periodoCrimesFinal = periodoCrimes.sort_values('Natureza',ascending=False)
#     display(periodoCrimesFinal)

axi = range(2012, 2019, 6)
for i, ano in enumerate(range(2017, 2024, 5)):
    print(f'Período de {axi[i]} até {ano}.')
    dadosRegistro = dadosBrutos[(dadosBrutos['Registros'] > 0) & (dadosBrutos['Ano'] >= axi[i]) & (dadosBrutos['Ano'] <= ano)]
    periodoCrimes = dadosRegistro.groupby('Município')[['Natureza']].count()
    periodoCrimesFinal = periodoCrimes.sort_values('Natureza', ascending=False)
    display(periodoCrimesFinal)



# criminalidade por tempo no estado

dadosRegistro = dadosBrutos[(dadosBrutos['Registros'] > 0) & (dadosBrutos['Ano'] < 2023)]
tempoCrimes = dadosRegistro.groupby('Ano')[['Natureza']].count()
tempoCrimesFinal = tempoCrimes.sort_values('Ano',ascending=True)
# display(tempoCrimesFinal)

sns.lineplot(data=tempoCrimesFinal, x='Ano', y='Natureza', marker='o', color='skyblue')
plt.xticks(tempoCrimesFinal.index, rotation=45)
plt.show()





# Criminalidade por tempo em Muriaé

nome_do_municipio = "MURIAE"
filtradosMuriae = dadosRegistro.query('Município == @nome_do_municipio')
agrupadosMuriae = filtradosMuriae.groupby('Ano')[['Natureza']].count().round(0).astype(int)

sns.lineplot(data=agrupadosMuriae, x='Ano', y='Natureza', marker='o', color='skyblue')
plt.xticks(agrupadosMuriae.index, rotation=45)

ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))

plt.show()