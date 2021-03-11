# Dependência necessária 
# pip install pefile

import os , sys
import pefile

# Escreva um script em Python  que receba como entrada um arquivo ou diretório 
# e enumere a seções executáveis do(s) binário(s), imprimindo na saída padrão um dicionário de listas, 
# onde a chave é o nome do binário e o valor é uma lista de seções executáveis.

# Pequena consistência para verificar se são passados pelo menos 2 argumentos
#if (len(sys.argv) != 3):
#    print('Devem ser passados 2 argumentos, os dois .exe a serem comparados !')
#    exit()

executavel1 = str(sys.argv[1])
executavel2 = str(sys.argv[2])

#executavel1 = '/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/ping.exe'
#executavel2 = '/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/notepad++.exe'
nomeexec1 = executavel1[executavel1.rfind('/')+1:]
nomeexec2 = executavel2[executavel2.rfind('/')+1:]

dicionario = {}

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

# Carrega um dicionário com a lista das seções de cada um dos .exe recebidos como parâmetro
# Sim, eu sei que está feio codificar no braço as variáveis...
dicionario[nomeexec1] = [str(carrega_secao(executavel1))]
dicionario[nomeexec2] = [str(carrega_secao(executavel2))]

# transforma o valor das entrada que está em uma string para uma lista
for item in dicionario:
    dicionario[item] = str(dicionario[item][0]).split(",")

# imprime na saída padrão, os valores únicos e os comuns aos dois executáveis
print('=================')
print('Seções únicas por .exe')
print('=================')

print( nomeexec1, ' : ', set(dicionario[nomeexec1]) - set(dicionario[nomeexec2]) )
print( nomeexec2, ' : ', set(dicionario[nomeexec2]) - set(dicionario[nomeexec1]) )

print('=================')
print('Seções comuns a todos os .exe analizados')
print('=================')

print(  set(dicionario[nomeexec1]) & set(dicionario[nomeexec2]) )
