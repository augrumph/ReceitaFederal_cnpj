from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
import os
import pandas as pd
import csv
import pymongo
import json

def download_and_unzip(url, extract_to='.'):
     """Realiza o download do arquivo e descompacta o mesmo

    Parameters:
        url : url do download desejado 

    Returns:
        O arquivo descompactado na pasta em que o arquipo py esta salvo.

   """
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)
    print("Arquivo Baixado e Descompactado com sucesso")
    
def change_name(path,old,new):
     """Muda o nome e tipo do arquivo

    Parameters:
        path : caminho ate o arquivo 
        old  : nome atual do arquivo 
        new  : nome novo do arquivo

    Returns:
        O arquivo com o novo nome

   """
    old_file = os.path.join(path, old)
    new_file = os.path.join(path, new)
    os.rename(old_file, new_file)
    print("Nome alterado com sucesso")

def database(path,db_name):
     """ Cria um banco de dados e aloca os dados extraidos do arquivo desejado nesse banco

    Parameters:
        path : caminho ate o arquivo
        db_name : nome do novo banco de dados 

    Returns:
        Os dados do arquivo salvos no banco de dados

   """
    client = pymongo.MongoClient("mongodb://localhost:27017")
    col_names = ["cnpj_base", "identificador", "nome_razao_social", "cnpj_cpf", "qualificacao", "data_entrada", "pais","representante_legal" , "nome_representante", "qualificacao_representante","faixa_etaria"]
    df = pd.read_csv(path, names=col_names,error_bad_lines=False,delimiter=";",encoding='latin-1')
    df['data_entrada'] = pd.to_datetime(df['data_entrada'])
    data = df.to_dict(orient ="records")
    db =  client[db_name]
    db.df.insert_many(data)
    print("Arquivos salvos no banco de dados com sucesso")


download_and_unzip(url)
change_name(path,old,new)
database(path,db_name)