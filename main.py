from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class AnuncioResumido:
    
    def __init__(self,id,url):
        self.__id = str(id)
        self.__url = str(url)        
    
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = str(value)

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = str(value)


def processa_lista():
    selenium_server="C:/Users/F0127173/git/pric-mego/vendor/selenium-server-standalone-3.141.59.jar"
    selenium_driver="C:/Users/F0127173/git/pric-mego/vendor/geckodriver-v0.26.0-win64"

    driver = webdriver.Firefox(executable_path=r"C:/Users/F0127173/git/pric-mego/vendor/geckodriver-v0.26.0-win64/geckodriver.exe")
    driver.get("https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&cidadeaberto=&escopo=2&anunciosNovos=1&anunciosUsados=1&marca1=5&modelo1=2428&anomodeloinicial=2016&anomodelofinal=2021&locationSop=est_SP.1_-cid_9668.1_-esc_2.1_-rai_50.1_")

    element = driver.find_element_by_xpath("//*")
    html = element.get_attribute("outerHTML")
    soup = BeautifulSoup(html)

    for formTag in soup.find_all('form', {'id' : 'anunciosForm'}):
        for ul in formTag.find_all('ul', {'class': 'listavertical'}):
            for litag in ul.find_all('li'):
                id = litag.get("id")
                if id is not None:
                    print(id)
                    print(litag.find('h3').text)
                    #preco = (soup.select("#"+id+" > div > a"))
                    #print(preco.get("href"))
                    links=litag.find('a')
                    print(links.get("href"))
                    #print(preco.find('h3', {'class': 'direita preco_anuncio'}))
                    #preco2 = litag.find_element_by_xpath('//*[@id="'+id+'"]/div/a/h3')
                    #print(preco2)
                    
                    #//*[@id="ac28542875"]/div/a
    #ac28542875 > div > a
    driver.quit()
    #ac28542875 > div > a > h3



