from bcb import PTAX
from pandas import to_datetime
from datetime import datetime, timedelta
from dateutil.parser import parse

def check_if_datetime(any_day):
    """"""
    if not isinstance(any_day, datetime):
        any_day = parse(any_day)
    return any_day

def first_day_of_month(any_day):
    """
    """
    # check if any_day is a datetime object.
    # if it is a string, convert to datetime.
    any_day = check_if_datetime(any_day)
    # replace the day part of the datetime
    # object to 1.
    return any_day.replace(day=1)

def last_day_of_month(any_day):
    """
    function idea here https://stackoverflow.com/a/13565185
    """
    # check if any_day is a datetime object.
    # if it is a string, convert to datetime.
    any_day = check_if_datetime(any_day)

    # The day 28 exists in every month. 4 days later, it's always next month
    next_month_date = any_day.replace(day=28) + timedelta(days=4)

    # subtracting the number of the current day brings us back one month
    return next_month_date - timedelta(days=next_month_date.day)


def obter_cotações(início='1/1/2023', fim='1/31/2023', moeda='USD'):
    """
    Função que busca as cotações diárias de um intervalo determinado,
    para uma [moeda] (por padrão 'USD').
    É possível passar uma lista de moedas para obter as cotações de todas
    em um DataFrame.
    """

    def consultar_bacen(início, fim, moeda):
        ep = PTAX().get_endpoint('CotacaoMoedaPeriodo')
        df_temp = (ep.query()
            .parameters(moeda=moeda,
            dataInicial=início,
            dataFinalCotacao=fim).collect())
        df_temp['moeda'] = moeda
        return df_temp

    if isinstance(moeda, str):
        df = consultar_bacen(início, fim, moeda)
        return df
    if isinstance(moeda,list):
        df = None
        for m in moeda:
            df_temp = consultar_bacen(início, fim, moeda=m)

            if df is not None:
                df = df.append(df_temp)
            else:
                df = df_temp

    # filtrar apenas as cotações de fechamento
    df = df[df['tipoBoletim']=='Fechamento']
    # selecionar apenas as colunas que interessam
    df = df[['moeda','dataHoraCotacao','cotacaoCompra','cotacaoVenda']]
    # renomear
    col_nomes = {'moeda':'moeda',
                'dataHoraCotacao':'data',
                'cotacaoCompra': 'cotação de compra',
                'cotacaoVenda': 'cotação de venda'}
    df.rename(columns=col_nomes, inplace=True)
    # transformar data e hora
    df['data'] = to_datetime(df['data'])
    return df