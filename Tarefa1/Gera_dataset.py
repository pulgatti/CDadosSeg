
# Writing to file
#file1 = open('dataset.txt', 'w')
#file1.writelines(L)
#file1.close()
 
# Opening file
file1 = open('/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/CDadosSeg/Tarefa1/community.rules', 'r')
file2 = open('/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/CDadosSeg/Tarefa1/sid-msg.map', 'r')
filesaida = open('/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/CDadosSeg/Tarefa1/dataset.txt', 'w')

tabela = {'ip': '0', 'tcp': '1', 'udp':'2', 'icmp':'3' }


for line in file1:
    # A linha lida não é parte do cabelçalho
    if (line.find(' tcp ' ) > 0 ) or (line.find(' tcp ' ) > 0 ) or (line.find(' udp ' ) > 0 ) or (line.find(' icmp ' ) > 0 ):
        #token = line.split()
        # Monta a tabela do protocolo
        linha=''
        if line.find(' ip ' ) > 0:
                linha=linha + str(tabela.get('ip', -1)) + ','
        elif line.find(' tcp ' ) > 0:
                linha=linha + str(tabela.get('tcp', -1)) + ','
        elif line.find(' udp ' ) > 0:
                linha=linha + str(tabela.get('udp', -1)) + ','
        elif line.find(' icmp ' ) > 0:
                linha=linha + str(tabela.get('icmp', -1)) + ','
        # Lê a porta
        posicao_inicial = line.find('$HOME_NET')+10
        # Não tem $HOME_NET, set avalor para none
        if posicao_inicial > 10:
                posicao_final = line.find(' ', posicao_inicial)
                linha = linha + (line[posicao_inicial:posicao_final]) + ','
        else:
                linha = linha + 'none,'

        # Lê a mensagem
        posicao_inicial = line.find('msg:')+5
        posicao_final = line.find('"', posicao_inicial)
        linha = linha + (line[posicao_inicial:posicao_final])      

        # Lê a mensagem do arquivo 2 fazendo a busca da mensagem pelo sid:
        #posicao_inicial = line.find('sid:')+4
        #posicao_final = line.find(';', posicao_inicial) 
        #codigo_sid = line[posicao_inicial:posicao_final]
        #print(codigo_sid)
        #for line1 in file2:
        #        if codigo_sid in line1:
                #codigo = line1[line1.find(codigo_sid,0,line1.find('||')):line1.find('||')]
                #if line1.find(codigo_sid) >= 0:
        #                print(line1)
                

        # Escreve no arquivo de saída
        filesaida.writelines(linha+'\n')

# Closing files
file1.close()
file2.close()
filesaida.close()