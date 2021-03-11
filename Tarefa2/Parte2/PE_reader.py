# Dependência necessária 
# pip install pefile

import os , sys
import pefile

# Escreva um script em Python  que receba como entrada um arquivo ou diretório 
# e enumere a seções executáveis do(s) binário(s), imprimindo na saída padrão um dicionário de listas, 
# onde a chave é o nome do binário e o valor é uma lista de seções executáveis.

diretorio = str(sys.argv[1])
#diretorio = '/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/'

def carrega_secao(arquivo):
        pe =  pefile.PE(arquivo)
        lista_secao = ''
        for section in pe.sections:
            lista_secao = lista_secao + str(section.Name)
        # Limpa da string caracteres não representativos retornados pela ferramenta
        lista_secao = lista_secao.replace("'b'", ',')
        lista_secao = lista_secao.replace("b'", '')
        lista_secao = lista_secao.replace("\\x00'", '')
        lista_secao = lista_secao.replace("\\x00", '')
        return lista_secao

dicionario = {}

# Lista o conteúdo do diretório
dirs = os.listdir( diretorio )

# Carrega um dicionário com a lista das seções de cad um dos .exe presentes no diretório indicado
for file in dirs:
    if (file[-4:] == '.exe'):
        dicionario[file] = [str(carrega_secao(diretorio + "/" + file))]

# transforma o valor das entrada que está em uma string para uma lista
for item in dicionario:
    dicionario[item] = str(dicionario[item][0]).split(",")

# imprime na saída padrão, a lista de seções para cada entrada no dicionário
for item in dicionario:
    print(item , ' : ', dicionario[item] )