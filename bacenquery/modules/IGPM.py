# -*- coding: utf-8 -*-

from .functions import format_date_to_BacenAPI, rolling_cumulative_product
from bcb import sgs
from pandas import DataFrame, concat
from datetime import datetime
from os.path import join

def consultar_API_IGPM(ano):
    """
    """
    início = datetime(ano, 1, 1)
    fim = datetime(ano, 12, 31)

    # formato de data precisa ser 'YYYY-MM-DD'
    # a função format_date_to_BacenAPI retorna a data no formato correto
    início = format_date_to_BacenAPI(início,'IGPM')
    fim = format_date_to_BacenAPI(fim, 'IGPM')

    # fazer a consulta
    df = sgs.get({'IGPM':189}, start=início, end=fim)

    # o df retornado tem as datas no index
    # transformar o index em uma coluna normal
    df.reset_index(inplace=True)

    return df

def buscar_IGPM(caminho,
                ano_início = 2022,
                ano_fim = 2023,
                ):

    # buscar IGPM e consolidar o arquivo
    print(f'buscando IGPM de {ano_início} a {ano_fim}')
    df_consolidado = DataFrame()
    for a in range(ano_início,ano_fim+1):
        print(f'\t{a}')
        df_temp = consultar_API_IGPM(a)
        if df_consolidado.empty:
            df_consolidado = df_temp
        else:
            df_consolidado = concat([df_consolidado, df_temp], ignore_index=True)
    # acumular
    períodos_acumulados = [3, 6, 12]
    col_data = 'Date'
    col_acumular = 'IGPM'
    for p in períodos_acumulados:
        nova_col = col_acumular+'_'+str(p)+'M'
        df_consolidado[nova_col] = rolling_cumulative_product(df_consolidado,p,col_data,col_acumular)

    # gravar arquivos
    # o primeiro ano não é salvo (por isso o ano_início+1), uma vez que
    # as colunas de acumulado não foram calculadas adequadamente.
    print(f'Gravando arquivos IGPM')
    for a in range(ano_início+1,ano_fim+1):
        print(f'\t{a}')
        df_por_ano = df_consolidado[df_consolidado['Date'].dt.year == a]
        nome_arquivo = 'IGPM_'+str(a)+'.csv'
        pasta_QS = join(caminho, nome_arquivo)
        df_por_ano.to_csv(pasta_QS, sep=';',decimal=',', encoding='iso-8859-1', index=False, date_format='%d/%m/%Y')
        print(f'\t\tarquivo salvo com sucesso')