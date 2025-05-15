# -*- coding: utf-8 -*-
"""
Created on Wed May 14 20:25:21 2025

@author: Nickolas
"""

# =======================
# IMPORTAÇÃO DE BIBLIOTECAS
# =======================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =======================
# CARREGAMENTO DOS DADOS
# =======================

data = pd.read_excel("https://raw.githubusercontent.com/Nickolas3211/Barbearia/refs/heads/main/teste.xlsx")

# =======================
# ANÁLISE DE LUCRO POR FORMA DE PAGAMENTO
# =======================

lucroPagamento = data[['Forma de pagto', 'Valor']]

# Agrupamento por Profissional e Forma de Pagamento
lucro_por_pagamento = data.groupby(['Profissional', 'Forma de pagto'])['Valor'].agg(['sum', 'mean']).reset_index()

# Ordenação para melhor visualização
tl = lucro_por_pagamento.sort_values(by=['Forma de pagto', 'sum'], ascending=[True, False])

# Gráfico de barras agrupadas
plt.figure(figsize=(12, 6))
sns.barplot(data=tl, x='Forma de pagto', y='sum', hue='Profissional', palette='Set2')
plt.xlabel("Método de Pagamento")
plt.ylabel("Lucro Total")
plt.title("Lucro por Profissional para cada Método de Pagamento")
plt.legend(title="Profissional")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# =======================
# LUCRO TOTAL POR PROFISSIONAL
# =======================

lucro_por_profissional = lucro_por_pagamento.groupby('Profissional')['sum'].sum().reset_index()
lucro_por_profissional = lucro_por_profissional.sort_values(by='sum', ascending=False)

# Cores para as barras
cores = plt.cm.Set2(np.linspace(0, 1, len(lucro_por_profissional)))

# Gráfico de barras com valores
plt.figure(figsize=(10, 5))
plt.bar(lucro_por_profissional['Profissional'], lucro_por_profissional['sum'], color=cores)
plt.xlabel("Profissional")
plt.ylabel("Lucro Total")
plt.title("Lucro Total por Profissional")

# Rótulos acima das barras
for i, valor in enumerate(lucro_por_profissional['sum']):
    plt.text(i, valor + 50, f'{valor:.2f}', ha='center', fontsize=10)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

# =======================
# GRÁFICO DE PIZZA: PORCENTAGEM POR MÉTODO DE PAGAMENTO
# =======================

lucro_por_pagamento_tipo = lucro_por_pagamento.groupby('Forma de pagto')['sum'].sum().reset_index()
total_lucro = lucro_por_pagamento_tipo['sum'].sum()
lucro_por_pagamento_tipo['porcentagem'] = (lucro_por_pagamento_tipo['sum'] / total_lucro) * 100

plt.figure(figsize=(8, 8))
plt.pie(
    lucro_por_pagamento_tipo['porcentagem'], 
    labels=lucro_por_pagamento_tipo['Forma de pagto'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.Pastel1.colors
)
plt.title("Porcentagem de Lucro por Método de Pagamento")
plt.show()

# =======================
# GRÁFICO DE LINHA INDIVIDUAL POR PROFISSIONAL
# =======================

datas_Valores = data[['Profissional', 'Data', 'Valor']]

crescimento_Valores = datas_Valores.groupby(['Profissional', 'Data'])['Valor'].sum().reset_index()


crescimento_Valores['Data'] = pd.to_datetime(crescimento_Valores['Data'])
crescimento_Valores = crescimento_Valores.sort_values(by='Data')

for profissional in crescimento_Valores['Profissional'].unique():
    dados = crescimento_Valores[crescimento_Valores['Profissional'] == profissional]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dados['Data'], dados['Valor'], marker='o', linestyle='-')
    plt.title(f'Evolução de Valores ao Longo do Tempo - {profissional}')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# =======================
# GRÁFICO ÚNICO COM TODAS AS LINHAS POR PROFISSIONAL
# =======================

plt.figure(figsize=(12, 7))

for profissional in crescimento_Valores['Profissional'].unique():
    dados = crescimento_Valores[crescimento_Valores['Profissional'] == profissional]
    plt.plot(dados['Data'], dados['Valor'], marker='o', linestyle='-', label=profissional)

plt.title('Evolução de Valores ao Longo do Tempo por Profissional')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend(title='Profissional')
plt.tight_layout()
plt.show()
