import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from test import get_noticia
import os

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
from datetime import date

today=date.today()

print(os.getcwd())
conn = sqlite3.connect("../data/noticias.sqlite")
cur = conn.cursor()



##### tabla con portales de noticias
urls={"emol":"https://www.emol.com",
      "la_tercera":"https://www.latercera.com",
      "cnn_chile":"https://www.cnnchile.com"}

cur.execute('''CREATE TABLE IF NOT EXISTS portales_noticias
    (id INTEGER PRIMARY KEY, name TEXT UNIQUE,url TEXT UNIQUE)''')

for name,url in urls.items():
    print(name,url)
    cur.execute('INSERT OR IGNORE INTO portales_noticias ( name, url) VALUES ( ?, ? )', ( name, url ) )
conn.commit()


cur.execute('''CREATE TABLE IF NOT EXISTS dias_ejecutados
    (id INTEGER PRIMARY KEY, ex_dt DATETIME, portal_noticias_id INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS noticias_raw
            (id INTEGER PRIMARY KEY, portal_noticias_id INT, url TEXT UNIQUE, html TEXT)''')


#cur.execute('''CREATE TABLE IF NOT EXISTS noticias
#    (id INTEGER PRIMARY KEY, titulo TEXT,portal_noticias_id INTEGER, url TEXT UNIQUE,
#     descripcion TEXT, contenido TEXT, error TEXT, html TEXT)''')

# Check to see if we are already in progress...



cur.execute('SELECT ex_dt FROM dias_ejecutados ORDER BY ex_dt DESC')
row = cur.fetchone()
if row is None:
    print("No hay noticias extraidas")
else :
    print("Ultimo dia de ejecucion:", row)

# Get the current webs
cur.execute('''SELECT url,id FROM portales_noticias''')
webs = list()
for row in cur:
    webs.append((str(row[0]),row[1]))

print(webs)

many = 0
for url, id_portal in webs:
    print(url,id_portal)
    try:
        document = urlopen(url, context=ctx)

        html = document.read()
        if document.getcode() != 200 :
            print("Error on page: ",document.getcode())
           
        if 'text/html' != document.info().get_content_type() :
            print("Ignore non text/html page")
            continue


        soup = BeautifulSoup(html, "html.parser")
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except:
        print("Unable to retrieve or parse page")
        continue

    conn.commit()

    # Retrieve all of the anchor tags
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href', None)
        if ( href is None ) : continue
        # Resolve relative references like href="/contact"
        up = urlparse(href)
        if ( len(up.scheme) < 1 ) :
            href = urljoin(url, href)
        ipos = href.find('#')
        if ( ipos > 1 ) : href = href[:ipos]
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') ) : continue
        if ( href.endswith('/') ) : href = href[:-1]
        # print href
        if ( len(href) < 1 ) : continue

		# Check if the URL is in any of the webs
        found = False
        for web in url:
            if ( href.startswith(web) ) :
                found = True
                break
        if not found : continue
        print(href)
        try:
            document = urlopen(href, context=ctx)
            html_page = document.read()
        except:
            continue
        cur.execute('INSERT OR IGNORE INTO noticias_raw (portal_noticias_id,url, html) VALUES ( ?, ?, ? )', ( id_portal, href,html_page) )
        count = count + 1
        conn.commit()
    cur.execute("""INSERT OR IGNORE INTO dias_ejecutados (ex_dt ,portal_noticias_id) 
                    VALUES ( ?, ?)""", ( id_portal, today))

    print(count)

cur.close()
