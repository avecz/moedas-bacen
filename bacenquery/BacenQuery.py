from bcb import PTAX
from pandas import to_datetime, concat
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

def format_date_to_BacenAPI(any_day=None):
    """
    Take a datetime object, or any
    string that could be parsed to
    a datetime object and format it
    to the format that the Bacen API
    expects: month/day/year, without
    leading zeros for month and day.
    """
    # check if a object was passed
    if any_day is None:
        any_day = datetime.now()
    # check if any_day is a datetime object.
    # if it is a string, convert to datetime.
    any_day = check_if_datetime(any_day)
    return str(any_day.month)+'/'+str(any_day.day)+'/'+str(any_day.year)

def get_exchange_rates(start=None, end=None, currency='USD'):
    """
    Fetching the daily exchange rates between a currency and BRL.
    It is possible:
    - to fetch a period by providing the 'end' parameter.
    - to fetch several currencies, if provided a list
      of strings.
      Defaults to current day and BRL/USD.

    """
    start = format_date_to_BacenAPI(start)
    end = format_date_to_BacenAPI(end)

    def query_API(start, end, currency):
        ep = PTAX().get_endpoint('CotacaoMoedaPeriodo')
        df_temp = (ep.query()
            .parameters(moeda=currency,
            dataInicial=start,
            dataFinalCotacao=end).collect())
        df_temp['moeda'] = currency
        return df_temp

    if isinstance(currency, str):
        df = query_API(start, end, currency)
        return df
    if isinstance(currency,list):
        df = None
        for m in currency:
            df_temp = query_API(start, fim, currency=m)
            if df is not None:
                df = concat([df, df_temp], ignore_index=True)
            else:
                df = df_temp.copy()

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
    df['data'] = to_datetime(df['data']).dt.date
    # found examples of duplicated rows in the last day of month
    df.drop_duplicates(inplace=True)
    return df