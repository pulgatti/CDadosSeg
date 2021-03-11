# Dependência necessária 
# pip install pefile

import os , sys
import pefile

# Escreva um script em Python  que receba como entrada um arquivo ou diretório 
# e enumere a seções executáveis do(s) binário(s), imprimindo na saída padrão um dicionário de listas, 
# onde a chave é o nome do binário e o valor é uma lista de seções executáveis.

diretorio = '/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/'

dicionario = {}

linha = ['.text', '.data']

dicionario['ping.exe'] = linha
dicionario['calc.exe'] = {'Lista' : [".text", ".data", '.rscp']}

print(dicionario['ping.exe'])
print(dicionario['calc.exe']['Lista'])


# Lista o conteúdo do diretório
dirs = os.listdir( diretorio )

for file in dirs:
    if (file[-4:] == '.exe'):
        pe =  pefile.PE(diretorio + "/" + file)
        lista_secao = ''
        for section in pe.sections:
            lista_secao = lista_secao + str(section.Name)
        # Limpa da string caracteres não representativos retornados pela ferramenta
        lista_secao = lista_secao.replace("'b'", ',')
        lista_secao = lista_secao.replace("b'", '')
        lista_secao = lista_secao.replace("\\x00'", '')
        lista_secao = lista_secao.replace("\\x00", '')
        dicionario[file] = [str(lista_secao)]
print(dicionario)

teste = dicionario['ping.exe']
print(teste[0].split(","))

print(dicionario.keys())
