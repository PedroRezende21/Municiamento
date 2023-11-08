import pandas as pd

dados1 = pd.read_excel('./Input/Execução Financeira do Municiamento(1).xlsx')
dados2 = pd.read_excel('./Input/Empenhos_municiamento.xlsx')

dados1 = dados1[5:]
dados1 = dados1.drop('Execução Financeira do Municiamento', axis=1)
dados1.iloc[0, 0] = 'Favorecido'
dados1.iloc[0, 1] = 'Nota de Empenho'
dados1.columns = dados1.iloc[0]
dados1 = dados1.reset_index(drop=True)
dados1 = dados1.drop(0, axis=0)
dados1['CREDITO DISPONIVEL'] = dados1['CREDITO DISPONIVEL'].astype(float)
dados1['DESPESAS EMPENHADAS A LIQUIDAR (CONTROLE EMP)'] = dados1['DESPESAS EMPENHADAS A LIQUIDAR (CONTROLE EMP)'].astype(float)
dados1['DESPESAS LIQUIDADAS A PAGAR(CONTROLE EMPENHO)'] = dados1['DESPESAS LIQUIDADAS A PAGAR(CONTROLE EMPENHO)'].astype(float)
dados1['DESPESAS PAGAS (CONTROLE EMPENHO)'] = dados1['DESPESAS PAGAS (CONTROLE EMPENHO)'].astype(float)
dados1['RESTOS A PAGAR NAO PROCESSADOS A LIQUIDAR'] = dados1['RESTOS A PAGAR NAO PROCESSADOS A LIQUIDAR'].astype(float)
dados1 = dados1.fillna(0)
dados1 = dados1.loc[~((dados1['DESPESAS EMPENHADAS A LIQUIDAR (CONTROLE EMP)'] == 0) & 
                   (dados1['DESPESAS LIQUIDADAS A PAGAR(CONTROLE EMPENHO)'] == 0) & 
                   (dados1['DESPESAS PAGAS (CONTROLE EMPENHO)'] == 0) &
                   (dados1['RESTOS A PAGAR NAO PROCESSADOS A LIQUIDAR'] == 0))]
#dados1['Data de emissão'] = None
#dados1['Data de emissão'] = pd.to_datetime(dados1['Data de emissão'], format="%d/%m/%Y")
dados2 = dados2[5:]
dados2 = dados2.drop('Empenhos_municiamento', axis=1)
dados2.iloc[0, 0] = 'Favorecido'
dados2.iloc[0, 1] = 'Data de emissão'
dados2.iloc[0, 2] = 'Nota de Empenho'
dados2.columns = dados2.iloc[0]
dados2 = dados2.reset_index(drop=True)
dados2 = dados2.drop(0, axis=0)
dados2 = dados2.loc[dados2['Data de emissão'] != 'NAO SE APLICA']
dados2['Data de emissão'] = pd.to_datetime(dados2['Data de emissão'], format="%d/%m/%Y")
dados2 = dados2.reset_index(drop=True)
dados1 = dados1.merge(dados2[['Nota de Empenho', 'Data de emissão']], how='inner', on='Nota de Empenho')
#reorganizando as colunas:
dados1 = dados1.loc[:, ['Favorecido', 'Nota de Empenho', 'Data de emissão', 'CREDITO DISPONIVEL',
                        'DESPESAS EMPENHADAS A LIQUIDAR (CONTROLE EMP)', 'DESPESAS LIQUIDADAS A PAGAR(CONTROLE EMPENHO)',
                        'DESPESAS PAGAS (CONTROLE EMPENHO)', 'RESTOS A PAGAR NAO PROCESSADOS A LIQUIDAR']]
dados1['VALOR TOTAL DO EMPENHO'] = dados1['DESPESAS EMPENHADAS A LIQUIDAR (CONTROLE EMP)'] + dados1['DESPESAS LIQUIDADAS A PAGAR(CONTROLE EMPENHO)'] + dados1['DESPESAS PAGAS (CONTROLE EMPENHO)'] + dados1['RESTOS A PAGAR NAO PROCESSADOS A LIQUIDAR']
