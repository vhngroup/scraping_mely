import requests
import datetime
from flask import Flask, jsonify
from bs4 import BeautifulSoup
from lxml import etree
import json

app = Flask(__name__)

@app.route('/mercadoLibre', methods=['GET'])
def mercadoLibre():
    lista_titulos = []
    lista_urls = []
    lista_precios = []
    start = datetime.datetime.now()
    siguiente = 'https://listado.mercadolibre.com.co/auv240-32g-rbk'
    while True:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}
        r = requests.get(siguiente, headers=headers, timeout=(None, 10))
        if r.status_code == 200:
            soup =BeautifulSoup(r.content, 'html.parser')
            #Xpatch del titulo
            #//h2[@class="ui-search-item__title"]
            titulos = soup.find_all('h2', attrs={"class":"ui-search-item__title"})
            #hacemos list convergetions
            titulos = [ i.text for i in titulos]
            lista_titulos.extend(titulos)
            #Xpatch de la URL
            #//a[@class="ui-search-result__content ui-search-link"] 
            urls = soup.find_all('a', attrs={"class":"ui-search-item__group__element ui-search-link"})
            #hacemos list convergetions para las URLs
            urls = [i.get('href') for i in urls]
            lista_urls.extend(urls)
            #Treamos los precios.
            dom = etree.HTML(str(soup))
            #precios = soup.find_all('span', attrs={"class":"price-tag-text-sr-only"})
            precios = dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__wrapper"]//div[@class="andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default"]//div[@class="ui-search-result__content-wrapper"]//div[@class="ui-search-result__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left"]//div[@class="ui-search-item__group ui-search-item__group--price"]//div[@class="ui-search-item__group__element ui-search-price__part-without-link"]//div[@class="ui-search-price__second-line"]//span[@class="price-tag-amount"]//span[@class="price-tag-fraction"]')
            precios = [i.text for i in precios]
            lista_precios.extend(precios)
            inicial = soup.find('span', attrs={"class":"andes-pagination__link"})
            final = soup.find('li', attrs={"class":"andes-pagination__page-count"})
            if inicial == None:
                break
            else:
                inicial = int(inicial.text)
                final = int(final.text.split(" ")[1])
        else:
            break
        print(f'{inicial}, {final}')
        
        if inicial == final:
            break
        siguiente = dom.xpath('//div[@class="ui-search-pagination"]/ul/li[contains(@class,"--next")]/a')[0].get('href')
        
    return jsonify({"datos":{"Titulo":lista_titulos, "Precio":lista_precios, "Url":lista_urls}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=(5500) , debug=True)