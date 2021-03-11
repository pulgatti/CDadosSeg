#Dependência necessária 
#Download: #https://github.com/kzjeef/AxmlParserPY
#Install: #sudo python -m pip install AxmlParserPY-master.zip

import os , sys
import axmlparserpy.apk as apk
diretorio = str(sys.argv[1])
#diretorio = "/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/APK/"


# Lista o conteúdo do diretório
dirs = os.listdir( diretorio )

lista_apk = []

# loop que lê o diretório informado e para todas as .apk presentes cria uma lista das propriedades
# a lista possui o nome do APK e uma lista com as permissões
for file in dirs:
    if (file[-4:] == '.apk'):
        ap = apk.APK(diretorio + "/" + file)
        lista_apk.append([ap.get_package(),ap.get_permissions(),''])
        #Caso se queira recuperar o arquivo AndroidManifest.xml em um formato legível de dentro do APK
        #from axmlparserpy import axmlprinter
        #from xml.dom import minidom

        #def main():
        #ap = axmlprinter.AXMLPrinter(open('dirs = os.listdir( diretorio + "/" + AndroidManifest.xml', 'rb').read())
        #buff = minidom.parseString(ap.getBuff()).toxml()
        #print(buff)


# Permissões que todos as apks possuem
# inicializa com a lista do primeiro apk, como é uma intersecção esta lista só diminui
perm_glo = lista_apk[0][1:2][0]

print('=================')
print('Permissões únicas por APK')
print('=================')

for i, elementos in enumerate(lista_apk):
    nome_apk = elementos[0:1][0]  # nome da APK
    perm_apk = elementos[1:2]  # Permissões da APK
    perm_uni = set(perm_apk[0]) - set('')  # Permissões únicas desta apk

    perm_glo = list(set(perm_apk[0]) & set(perm_glo)) # Retira da lista global as permisões que não são comuns
    
    # loop que compara as permissões do app com todas as outras, deixando apenas as que são únicas
    for w, elementos_internos in enumerate(lista_apk):
            if w != i:
                perm_uni = list(set(perm_uni) - set(elementos_internos[1]))
  
    print(nome_apk, ' - ' , perm_uni)

print('=================')
print('Permissões comuns das APKs')
print('=================')

print(perm_glo)


