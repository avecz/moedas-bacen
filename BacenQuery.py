from bcb import PTAX

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
    return df