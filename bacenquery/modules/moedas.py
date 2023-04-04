# -*- coding: utf-8 -*-

from . base_functions import first_day_of_month, last_day_of_month, get_exchange_rates
import pandas as pd
from datetime import datetime
import os

def consultar_API_Moedas(
        moedas = ['USD','EUR'],
        ano = datetime.now().year,
        mês = datetime.now().month
):
    """
    Consulta por mês.
    Por padrão é o mês atual.
    """

    data = datetime(ano, mês, 1)
    first_day = first_day_of_month(data).strftime('%#m/%#d/%Y')
    last_day = last_day_of_month(data).strftime('%#m/%#d/%Y')
    
    return get_exchange_rates(start=first_day, end=last_day, currency=moedas)

def buscarcotações(caminho,
                   moedas = ['USD','EUR'],
                   ano = datetime.now().year):

    hoje = datetime.now()

    # loop de 1 a 12 (referente aos meses)
    for m in range(1,13):
        data = datetime(ano, m, 1)
        arquivo = 'moedas_'+str(data.year) +'.'+str(data.month).zfill(2)+'.csv'
        pasta_QS = os.path.join(caminho, arquivo)
        print(f'trabalhando com o arquivo {arquivo}')

        # verificar se o período consultado é válido.
        first_day = first_day_of_month(data)
        last_day = last_day_of_month(data)
        if first_day > hoje:
            print(f'\tprimeiro dia é maior que hoje')
            print(f'\tencerrando script')
            break
        if last_day > hoje:
            last_day = hoje
            print(f'\túltimo dia é maior que hoje')
            print(f'\tconsultando datas de {first_day.date()} até {last_day.date()}')

        # consultar e gravar o arquivo csv
        df = consultar_API_Moedas(moedas = moedas, ano = ano, mês = m)
        
        df.to_csv(pasta_QS, sep=';',decimal=',', encoding='iso-8859-1', index=False, date_format='%d/%m/%Y')
        print(f'\tarquivo {arquivo} salvo com sucesso')
