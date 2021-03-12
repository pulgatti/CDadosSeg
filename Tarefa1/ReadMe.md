Parte 1

Exercício A

No mesmo diretório onde se encontra o arquivo AV1.txt executar

./script1.sh > saida1.txt

O arquivo saida1.txt contêm as informações solicitadas

Exercício B

No mesmo diretório onde se encontra o arquivo AV2.txt executar

cat AV2.txt | cut -d':' -f1 | cut -d'.' -f2-4 | tr '.' ',' | tr '-' ',' > saida2.txt

O arquivo saida2.txt contêm as informações solicitadas

PARTE 2:

No mesmo diretório onde se encontra os arquivos community.rules e sid-msg.map executar Gera_dataset.py

O arquivo dataset.txt contêm a saída solicitada