import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd 
import numpy as np

#Web Scraping a la web de Mely

# r = requests.get('https://listado.mercadolibre.com.co/c5c')
# r.status_code #validamos el estado de la conexiòn
# #habilitamos y parsemos con BeautifullSoup
# soup =BeautifulSoup(r.content, 'html.parser')
# #Xpatch del titulo
# #//h2[@class="ui-search-item__title"]
# titulos = soup.find_all('h2', attrs={"class":"ui-search-item__title"})
# # imprimimos el titulo texto en la posiciòn 0
# # print(f'{titulos[0].text}') 
# #hacemos list convergetions
# titulos = [ i.text for i in titulos]
# #buscamos las URLs
# #Xpatch de la URL
# #//a[@class="ui-search-result__content ui-search-link"] 
# urls = soup.find_all('a', attrs={"class":"ui-search-result__content ui-search-link"})
# #hacemos list convergetions para las URLs
# urls = [i.get('href') for i in urls]
# #imprimimos todos los titulos traemos todos los titulos
# #print(f'{titulos}')
# #imprimimos todos las urls
# #print(f'{urls}')

# #//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-wrapper"]/div[2]/div[1]/div[@class="ui-search-price__second-line"]//span[@class="price-tag-amount"]/span[2]
# dom = etree.HTML(str(soup))
# precios = dom.xpath('//li[@class="ui-search-layout__item"]//div[1]/div[1]//div[@class="ui-search-price__second-line"]//span[@class="price-tag-amount"]//span[@class="price-tag-fraction"]')
# precios = [i.text for i in precios]
# # Imprimimos precios
# #print(f'{precios}')
# #creamos un data frame usando pandas
# #df = pd.DataFrame({"Titulo":titulos, "Precio":precios, "Url":urls})
# #df.to_csv("Export.csv", sep =";")
# siguiente = dom.xpath('//div[@class="ui-search-pagination"]/ul/li[contains(@class,"--next")]/a')[0].get('href')
# inicial = soup.find('span', attrs={"class":"andes-pagination__link"}).text
# inicial = int(inicial)
# final = soup.find('li', attrs={"class":"andes-pagination__page-count"})
# final = int(final.text.split(" ")[1])
# print(f'{final}')

lista_titulos = []
lista_urls = []
lista_precios = []
siguiente = 'https://listado.mercadolibre.com.co/auv240-32g-rbk'
while True:
    r = requests.get(siguiente)
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

print(len(lista_titulos))
print(len(lista_urls))
print(len(lista_precios))

#df = pd.DataFrame({"Titulo":lista_titulos, "Precio":lista_precios, "Url":lista_urls})
#df.to_csv("Export.csv", sep ="!")