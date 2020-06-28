"""
Created on Mon Jun  3
@author: benjaminobando
"""

import pandas as pd 
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

import wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image



import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.data import load
from nltk.stem import SnowballStemmer
from string import punctuation
from nltk.stem import WordNetLemmatizer


from datetime import date
today = date.today()
today = str(today)

import os
path = os.getcwd()


def generate_wordcloud(logo_image,text, stopwords_list, portal, today, path):
    custom_mask = np.array(Image.open(logo_image))

    wordcloud = WordCloud(stopwords = stopwords_list, background_color="white",mask=custom_mask)
    wordcloud.generate(text)


    image_colors = ImageColorGenerator(custom_mask)
    wordcloud.recolor(color_func=image_colors)

    plt.figure(figsize=(10,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig( path + "/wordclouds/wordcloud_"+portal+"_"+today+".png")



con = sqlite3.connect(path+'/data/noticias.sqlite')

query = """SELECT noticias_extract.id, noticias_extract.categoria,
            noticias_extract.titulo, noticias_extract.fecha,noticias_extract.texto as texto,
            noticias_extract.keywords, noticias_extract.autores,
            noticias_extract.nro_palabras, noticias_extract.nro_parrafos,
            noticias_raw.url, portales_noticias.name
        FROM noticias_extract, noticias_raw, portales_noticias
        WHERE noticias_extract.noticias_raw_id = noticias_raw.id  AND 
        noticias_raw.portal_noticias_id = portales_noticias.id"""

noticias_df = pd.read_sql_query(query, con)



noticias_df["texto_mod"] = noticias_df.texto.str.lower()
noticias_df.texto_mod = noticias_df.texto_mod.str.replace(r'[^\w\s]','')
noticias_df.texto_mod = noticias_df.texto_mod.str.replace(r'[\d]','')


noticias_df.texto_mod = noticias_df.texto_mod.str.replace("grupo copesa  la tercera red de medios lt otros medios grupo dial","")
noticias_df.texto_mod = noticias_df.texto_mod.str.replace("\xa0","")

spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

with open(path+'/data/lista_stopwords.txt', 'r',encoding='utf-8') as stopwords_file:
    more_stopwords = stopwords_file.read()
more_stopwords = more_stopwords.split()


non_words.extend(more_stopwords)

stopwords_spanish = spanish_stopwords+non_words


cnn_noticias = noticias_df[noticias_df.name == "cnn_chile"].texto.sum()
emol_noticias = noticias_df[noticias_df.name == "emol"].texto_mod.sum()
la_tercera_noticias = noticias_df[noticias_df.name == "la_tercera"].texto_mod.sum()

logo_cnn =path+ "/logos/logo_cnn.png"
logo_emol = path+ "/logos/logo_emol.png"
logo_la_tercera = path+ "/logos/logo_la_tercera1.jpg"

generate_wordcloud(logo_cnn,cnn_noticias, stopwords_spanish, "cnn", today, path)
generate_wordcloud(logo_emol,emol_noticias, stopwords_spanish, "emol", today, path)
generate_wordcloud(logo_la_tercera,la_tercera_noticias, stopwords_spanish, "la_tercera", today, path )

con.close()
"""
Created on Mon Jun  3
@author: benjaminobando
"""

import pandas as pd 
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

import wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image



import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.data import load
from nltk.stem import SnowballStemmer
from string import punctuation
from nltk.stem import WordNetLemmatizer


from datetime import date
today = date.today()
today = str(today)

import os
path = os.getcwd()


def generate_wordcloud(logo_image,text, stopwords_list, portal, today, path):
    custom_mask = np.array(Image.open(logo_image))

    wordcloud = WordCloud(stopwords = stopwords_list, background_color="white",mask=custom_mask)
    wordcloud.generate(text)


    image_colors = ImageColorGenerator(custom_mask)
    wordcloud.recolor(color_func=image_colors)

    plt.figure(figsize=(10,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig( path + "/wordclouds/wordcloud_"+portal+"_"+today+".png")



con = sqlite3.connect(path+'/data/noticias.sqlite')

query = """SELECT noticias_extract.id, noticias_extract.categoria,
            noticias_extract.titulo, noticias_extract.fecha,noticias_extract.texto as texto,
            noticias_extract.keywords, noticias_extract.autores,
            noticias_extract.nro_palabras, noticias_extract.nro_parrafos,
            noticias_raw.url, portales_noticias.name
        FROM noticias_extract, noticias_raw, portales_noticias
        WHERE noticias_extract.noticias_raw_id = noticias_raw.id  AND 
        noticias_raw.portal_noticias_id = portales_noticias.id"""

noticias_df = pd.read_sql_query(query, con)



noticias_df["texto_mod"] = noticias_df.texto.str.lower()
noticias_df.texto_mod = noticias_df.texto_mod.str.replace(r'[^\w\s]','')
noticias_df.texto_mod = noticias_df.texto_mod.str.replace(r'[\d]','')


noticias_df.texto_mod = noticias_df.texto_mod.str.replace("grupo copesa  la tercera red de medios lt otros medios grupo dial","")
noticias_df.texto_mod = noticias_df.texto_mod.str.replace("\xa0","")

spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

with open(path+'/data/lista_stopwords.txt', 'r',encoding='utf-8') as stopwords_file:
    more_stopwords = stopwords_file.read()
more_stopwords = more_stopwords.split()


non_words.extend(more_stopwords)

stopwords_spanish = spanish_stopwords+non_words


cnn_noticias = noticias_df[noticias_df.name == "cnn_chile"].texto.sum()
emol_noticias = noticias_df[noticias_df.name == "emol"].texto_mod.sum()
la_tercera_noticias = noticias_df[noticias_df.name == "la_tercera"].texto_mod.sum()

logo_cnn =path+ "/logos/logo_cnn.png"
logo_emol = path+ "/logos/logo_emol.png"
logo_la_tercera = path+ "/logos/logo_la_tercera1.jpg"

generate_wordcloud(logo_cnn,cnn_noticias, stopwords_spanish, "cnn", today, path)
generate_wordcloud(logo_emol,emol_noticias, stopwords_spanish, "emol", today, path)
generate_wordcloud(logo_la_tercera,la_tercera_noticias, stopwords_spanish, "la_tercera", today, path )

con.close()
