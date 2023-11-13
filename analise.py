#importanto as bibliotecas para trabalhar com os dados padrao pep8

#primeiro grupo de imports deve ser as bibliotecas nativas
import os
import time
import json
from random import random
from datetime import datetime

#segundo grupo de imports deve ser as bibliotecas de terceiros
import requests
import csv
from sys import argv

#terceiro grupo de imports deve ser as bibliotecas específicas ou locais
import pandas as pd
import seaborn as sns

#fim da importação de bibliotecas

#definindo url para extrair dados do site da b3
URL = 'https://www2.cetip.com.br/ConsultarTaxaDi/ConsultarTaxaDICetip.aspx'

#inicio função para extrair dados
def extrair_dados():
    for _ in range(0, 10): #executa o loop 10 vezes
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')
        
        try:
            response = requests.get(URL)
            response.raise_for_status()
        except requests.HTTPError as exc:
            print("Dado não encontrado, continuando.")
            cdi = None
        except Exception as exc:
            print("Erro, parando a execução.")
            raise exc
        else:
            dado = json.loads(response.text)
            cdi = float(dado['taxa'].replace(',', '.')) + (random() - 0.5)

        if not os.path.exists('./taxa-cdi.csv'):
            with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n')

        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')

        time.sleep(2 + (random() - 0.5))

    print("Sucesso")

def visualizar_dados(titulo):
    df = pd.read_csv('./taxa-cdi.csv')
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{titulo}.png")

if __name__ == '__main__':
    extrair_dados()
    titulo = argv[1]
    visualizar_dados(titulo)
    