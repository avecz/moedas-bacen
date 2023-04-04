# -*- coding: utf-8 -*-

from bcb import sgs
from .base_functions import format_date_to_BacenAPI

import pandas as pd
from datetime import datetime
import os

def query_API_Selic(ano = datetime.now().year):
    """
    """
    início = datetime(ano, 1, 1)
    fim = datetime(ano, 12, 31)

    # formato de data precisa ser 'YYYY-MM-DD'
    # a função format_date_to_BacenAPI retorna a data no formato correto
    início = format_date_to_BacenAPI(início,'IPCA')
    fim = format_date_to_BacenAPI(fim, 'IPCA')

    # fazer a consulta
    # 432: Taxa de juros - Meta Selic definida pelo Copom (% a.a.)
    df = sgs.get({'Selic':432}, start=início, end=fim)

    # o df retornado tem as datas no index
    # transformar o index para meses
    # df.index = df.index.to_period('M')
    # transformar o index em uma coluna normal
    df.reset_index(inplace=True)

    return df


def buscar_selic(caminho,
                    ano_início = 2000,
                    ano_fim = datetime.now().year,
                    arquivo = 'taxa_selic.csv'
                    ):

    print(f'arquivo {arquivo}')
    print(f'\tbuscando taxa selic de {ano_início} a {ano_fim}')

    df_consolidado = pd.DataFrame()
    for a in range(ano_início,ano_fim+1):
        print(f'\t{a}')
        df_temp = query_API_Selic(a)
        if df_consolidado.empty:
            df_consolidado = df_temp
        else:
            df_consolidado = pd.concat([df_consolidado, df_temp], ignore_index=True)

    pasta_QS = os.path.join(caminho, arquivo)
    df_consolidado.to_csv(pasta_QS, sep=';',decimal=',', encoding='iso-8859-1', index=False, date_format='%d/%m/%Y')
    print(f'\tarquivo salvo com sucesso')

