import numpy as np 
import pandas as pd 

import tensorflow as tf
import matplotlib.pyplot as plt

import nltk 
# Caso queira pegar a última versão das stopwords.
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from wordcloud import WordCloud

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense, Dropout, LSTM, Bidirectional

import re

# Lê o .csv e carrega para um DataFrame
#data = pd.read_csv('/home/pulgatti/Dropbox/Doutorado/Materias/CI1030-ERE2-CienciaDeDados/CDadosSeg/Projeto/spam_ham_dataset.csv')
data = pd.read_csv('./spam_ham_dataset.csv')
#print(data)

# Apaga a primeira coluna. Apenas o sequêncial das mensagens, não influi no resultado
data = data.drop(['Unnamed: 0', 'label'], axis=1)

# Mostra as primeiras linhas dos dadso carregados
print(data.head())

# Conta quantas entrada de cada tipo ( ham , spam ) o dataset possui
val_count = data.label_num.value_counts()


#Plota um gráfico com a distribuiçao dos dados por label
''' plt.figure(figsize=(8,4))
plt.bar(val_count.index, val_count.values)
plt.title("Distribuição dos Dados")
print(plt.show())
'''
#A amostra está desbalanceda.
# 5171 linhas
# 3672 Ham  71.01 %
# 1499 Spam 28.99 %
# Downsampling pode melhorar a acurácia, mas neste caso o ganho é pequeno


#data = data.replace(to_replace ="Subject:", value =" " )
#print(data.head())
#exit()

stop_words = stopwords.words('english')

# Trata os dados retirando as stopword, palavras que são comuns e não agregam a classificação
# O termo Subject: aparece em todos as entradas, assim não contribui para a classificação, por isto foi retirado tambem
# Testar sem pontuação para ver se melhora o score
# este processo está lento, deve ter uma maneira melhor de fazer
def preprocess(text):
    text = text.replace('\r',' ')
    text = text.replace('\n',' ')
    text = text.replace('#',' ')
    text = text.replace('Subject:','')
    for i in stop_words:
        text = text.replace(' '+i+' ', '')
    return text

data.text = data.text.apply(lambda x: preprocess(x))
#descomentar o bloco abaixo para mostar uma núvem de palavras mais comuns, nos dois grupos de email
'''
plt.figure(figsize = (20,20)) 
wc = WordCloud(max_words = 2000 , width = 1600 , height = 800).generate(" ".join(data[data.label_num == 1].text))
plt.imshow(wc , interpolation = 'bilinear')
plt.title("Nuvem de palavras mais comuns nos e-mail classificados como Spam")
print(plt.show())

plt.figure(figsize = (20,20)) 
wc = WordCloud(max_words = 2000 , width = 1600 , height = 800).generate(" ".join(data[data.label_num == 0].text))
plt.imshow(wc , interpolation = 'bilinear')
plt.title("Nuvem de palavras mais comuns nos e-mail classificados como Spam")
print(plt.show())
'''

#Definie os parâemtros para treinamento
# 80% para treinamento e 20% pata teste
# Os melhores resultados foram alcaçados om uma divisão de 60/40,
TRAIN_SIZE = 0.8
MAX_NB_WORDS = 100000
MAX_SEQUENCE_LENGTH = 50


x = data['text']
y = data['label_num']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1-TRAIN_SIZE,
                                         random_state=7) # Splits Dataset em treino e teste
print("Tamanho Base Treino:", len(x_train))
print("Tamanho Base Teste", len(x_test))

# x_train.head(10)


tokenizer = Tokenizer()
tokenizer.fit_on_texts(x_train)

word_index = tokenizer.word_index
vocab_size = len(tokenizer.word_index) + 1000
print("Quantidade de palavras no dataset :", vocab_size)


x_train = pad_sequences(tokenizer.texts_to_sequences(x_train),
                        maxlen = MAX_SEQUENCE_LENGTH)
x_test = pad_sequences(tokenizer.texts_to_sequences(x_test),
                       maxlen = MAX_SEQUENCE_LENGTH)

# Vai seu utilizada uma rede LSTM bi-direcional
# Estas redes são varioações das Redes Neurais Recorrentes ( RNN ) que não "esquecem" os dados de entrada
# São muito utilizadas em tarefas de PLN pois capturam melhor a semântica das palavras, ou seja, p contexto
# no qual a palavra está inserida pode influenciar no seu significado.
# Nos esperimentos foi obtida uma média de 98% de Acurácia na base de treinamento e de 93% na base de testes

#LSTM hyperparameters
n_lstm = 200
drop_lstm =0.2
embeding_dim = 16

# Biderecional LSTM 
model2 = Sequential()
model2.add(Embedding(vocab_size, embeding_dim, input_length=MAX_SEQUENCE_LENGTH))
model2.add(Bidirectional(LSTM(n_lstm, dropout=drop_lstm, return_sequences=True)))
model2.add(Dense(1, activation='sigmoid'))


model2.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics=['accuracy'])


# Training
num_epochs = 30
# Para o treinamento antes, caso o os ganhos estejam muito pequenos
early_stop = EarlyStopping(monitor='val_loss', patience=2)
history = model2.fit(x_train, y_train, epochs=num_epochs, 
                    validation_data=(x_test, y_test),callbacks =[early_stop], verbose=2)

# Testa o delo após a última iteração
test_results = model2.evaluate(x_test, y_test, verbose=False)
print(f'Resultado do teste - Perda: {test_results[0]} - Acurácia: {100*test_results[1]}%')


# Create a dataframe
metrics = pd.DataFrame(history.history)

metrics.rename(columns = {'loss': 'Training_Loss', 'accuracy': 'Training_Accuracy',
                         'val_loss': 'Validation_Loss', 'val_accuracy': 'Validation_Accuracy'}, inplace = True)
def plot_graphs1(var1, var2, string):
    metrics[[var1, var2]].plot()
    plt.title('BiLSTM : Treinamento e Validação ' + string)
    plt.xlabel ('Numero de épocas')
    plt.ylabel(string)
    plt.legend([var1, var2])
    print(plt.show())
# Plot
plot_graphs1('Training_Loss', 'Validation_Loss', 'loss')
plot_graphs1('Training_Accuracy', 'Validation_Accuracy', 'accuracy')


print(metrics.head())

# O resultado final da rede, seu estado final treuinado pode ser salvo para utilização posterior.
# from tensorflow.keras.models import load_model
# model2.save('spam_detection.h5')
