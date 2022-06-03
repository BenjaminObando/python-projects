#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 21:00:02 2020

@author: benjaminobando
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString,Tag
import re

def get_noticia(url):
    
    m = re.search('www.(.+?).com', url)
    found = m.group(1)
    
    document = urlopen(url)
    
    html = document.read()

    soup = BeautifulSoup(html, "html.parser")

    lista_span=[]
    
    if found=="emol":
        iterable=soup.find_all("div",{"id":"cuDetalle_cuTexto_textoNoticia" })
        
    elif found in ["latercera","cnnchile"]:
        iterable=soup.find_all("p")
        
    for body_child in iterable:
        if isinstance(body_child, NavigableString):
            continue
        if isinstance(body_child, Tag):
            lista_span.append(body_child.getText())    
    return(lista_span)

#url="https://www.emol.com/noticias/Nacional/2020/04/10/982731/Gobierno-variables-cuarentena-coronavirus-Chile.html"
#url="https://www.emol.com/noticias/Nacional/2020/04/10/982724/Gobierno-Coronavirus-Balance.html"
#url="https://www.emol.com/noticias/Nacional/2020/04/11/982770/Minsal-Coronavirus-Balance.html"
#url="https://www.latercera.com/mundo/noticia/oms-advierte-sobre-peligro-de-levantar-restricciones/RPABRLQNH5BXPAEU2WG3JEFLFA/"
#print(get_noticia(url))
    
#text = 'gfgfdAAA1234ZZZuijjk'

