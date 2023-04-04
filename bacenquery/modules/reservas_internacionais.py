# -*- coding: utf-8 -*-

from .base_functions import format_date_to_BacenAPI
from bcb import sgs

import pandas as pd
from datetime import datetime
import os

def consultar_API_reservas(ano = datetime.now().year):
    """
    """
    início = datetime(ano, 1, 1)
    fim = datetime(ano, 12, 31)

    # formato de data precisa ser 'YYYY-MM-DD'
    # a função format_date_to_BacenAPI retorna a data no formato correto
    # a princípio, o formato IGPM funciona para as reservas
    início = format_date_to_BacenAPI(início,'IGPM')
    fim = format_date_to_BacenAPI(fim, 'IGPM')

    # fazer a consulta
    df = sgs.get({'Reservas (US$ MM)':3546}, start=início, end=fim)

    # o df retornado tem as datas no index
    # transformar o index em uma coluna normal
    df.reset_index(inplace=True)

    return df

def buscar_reservas(caminho,
                    ano_início = None,
                    ano_fim = datetime.now().year,
                    ):
    """
    buscar as reservas para um intervalo e salvar em
    arquivos separados por anos.
    """
    
    if ano_início is None:
        ano_início = ano_fim

    print(f'\tbuscando reservas internacionais do Brasil de {ano_início} a {ano_fim}')

    df_consolidado = pd.DataFrame()
    for a in range(ano_início,ano_fim+1):
        print(f'\t{a}')
        df_temp = consultar_API_reservas(a)
        if df_consolidado.empty:
            df_consolidado = df_temp
        else:
            df_consolidado = pd.concat([df_consolidado, df_temp], ignore_index=True)

    # gravar arquivos
    print(f'Gravando arquivos')
    for a in range(ano_início,ano_fim+1):
        print(f'\t{a}')
        df_por_ano = df_consolidado[df_consolidado['Date'].dt.year == a]
        nome_arquivo = 'Reservas_'+str(a)+'.csv'
        pasta_QS = os.path.join(caminho, nome_arquivo)
        df_por_ano.to_csv(pasta_QS, sep=';',decimal=',', encoding='iso-8859-1', index=False, date_format='%d/%m/%Y')
        print(f'\t\tarquivo salvo com sucesso')

