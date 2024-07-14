import pandas as pd
import numpy as np
import re, os
import pickle
import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# Carregar o modelo treinado
model = tensorflow.keras.models.load_model('final_model.h5')

# Carregar o tokenizer usado no treinamento
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Carregar parâmetros
with open('params.pickle', 'rb') as handle:
    params = pickle.load(handle)

max_length = params['max_length']
padding_type = params['padding_type']

#Limpeza
def data_clean(string):
    string = re.sub(r"[^a-zA-ZÀ-ÖØ-öø-ÿÇç(),!?\'\`]", " ", string)
    string = re.sub(r",", " , ", string) #Adiciona espaços antes e depois de vírgulas.
    string = re.sub(r"!", " ! ", string) #Adiciona espaços antes e depois de cada ponto de exclamação na string.
    string = re.sub(r"\(", " \( ", string) #Adiciona espaços antes e depois de parênteses abertos.
    string = re.sub(r"\)", " \) ", string) #Adiciona espaços antes e depois de parênteses fechados.
    string = re.sub(r"\?", " \? ", string) #Adiciona espaços antes e depois de pontos de interrogação.
    string = re.sub(r"\s{2,}", " ", string) #Substitui duas ou mais ocorrências de espaços consecutivos por um único espaço.

    cleanr = re.compile('<.*?>') #compila função para encontrar tags

    string = re.sub(r'\d+', '', string) #Remove todos os dígitos numéricos do texto
    string = re.sub(cleanr, '', string) #remove todas as tags HTML do texto.
    string = re.sub("'", '', string) #Remove todas as aspas simples restantes no texto.
    #string = re.sub(r'\W+', ' ', string) #remove carateres não alfanuméricos
    string = string.replace('_', '') #Remove todos os underscores (sublinhados) do texto.

    return string.strip().lower() #Remove espaços em branco extras do início e do final do texto e converte o texto para minúsculas antes de retornar.

indice_para_rotulo = {0: 'bem-estar', 1: 'comportamental', 2: 'fisiologico', 3: 'psiquico'}

def predict(texto):
    # Limpar e preparar os textos
    texto = [data_clean(text) for text in texto]
    sequences = tokenizer.texts_to_sequences(texto)
    padded_sequences = pad_sequences(sequences, maxlen=max_length, padding=padding_type)

    # Fazer predição
    predictions = model.predict(padded_sequences)
    threshold = 0.5
    final_predictions = []
    for pred in predictions:
        max_prob = np.max(pred)
        if max_prob >= threshold:
            label = indice_para_rotulo[np.argmax(pred)]
            final_predictions.append((label, max_prob))
        else:
            final_predictions.append(("Indefinido", max_prob))

    print(final_predictions)
    return final_predictions

def calcular_media(final_predictions):
    rotulos_depre = ['comportamental', 'psiquico', 'fisiologico']
    contador_depre = 0
    contador_ok = 0
    contador_indefinido = 0

    for i in final_predictions:
        if i[0] in rotulos_depre:
            contador_depre += 1
        elif i[0] == 'Indefinido':
            contador_indefinido += 1
        elif i[0] == 'bem-estar':
            contador_ok += 1

    print(f"Contadores: ok = {contador_ok}, depressivo = {contador_depre}, indefinido = {contador_indefinido}")

    if contador_depre > contador_ok:
        return 1
    elif contador_ok >= contador_depre:
        return 0
    else:
        return "não foi possível calcular"

