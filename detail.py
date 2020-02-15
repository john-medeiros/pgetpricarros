import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

MIN_PYTHON = (3, 7)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

class Anuncio:

    def __init__(self,id,url,titulo=None,preco=None,ano=None,km=None,cor=None,cambio=None,portas=None):
        self.id = str(id)
        self.url = str(url)
        self.titulo = str(titulo)
        self.valor = str(preco)
        self.ano = str(ano)
        self.km = str(km)
        self.cor = str(cor)
        self.cambio = str(cambio)
        self.portas = str(portas)  

    def Salva_CSV(self,filename):
        with open(filename, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f,delimiter=';')
            writer.writerow([self.id, self.titulo, self.preco, self.ano, self.km, self.cor, self.cambio, self.portas, self.url])      
        f.close()

    @staticmethod
    def Cria_Arquivo(filename):
        print('Não implementado')

def obter_detalhe_anuncio(id,url):
    try:
        anuncio = Anuncio(id,url)
        driver = webdriver.Firefox(executable_path=r"C:/Users/F0127173/git/pric-mego/vendor/geckodriver-v0.26.0-win64/geckodriver.exe")
        driver.get(url)
        titulo = driver.find_element_by_xpath('//*[@id="ctdoTopo"]/h1')
        if titulo is not None:
            anuncio.titulo=titulo.text  
        preco = driver.find_element_by_xpath('//*[@id="cardProposta"]/div/h2')
        if preco is not None:
            anuncio.preco=preco.text

        element = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[5]/div[1]/div[2]/div')
        
        html = element.get_attribute('innerHTML')

        sub_html = BeautifulSoup(html,'html.parser') 

        ul = sub_html.find('ul')
        li = ul.find_all('li')
        print('teste1')

        for i in li:
            item = i.find('h6')
            if item.text.strip() == "Ano":
                anuncio.ano = i.find('span').text
                continue
            if item.text.strip() == "Km":
                anuncio.km = i.find('span').text
                continue
            if item.text.strip() == "Cor":
                anuncio.cor = i.find('span').text
                continue
            if item.text.strip() == "Câmbio":
                anuncio.cambio = i.find('span').text
                continue
            if item.text.strip() == "Portas":
                anuncio.portas = i.find('span').text
                continue     

        

        element = driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div[1]')    
        html = element.get_attribute('innerHTML') 
        sub_html = BeautifulSoup(html,'html.parser')   
        ul = sub_html.find('ul')
        li = ul.find_all('li')


        for liItem in li:
            
            if (len(liItem.find_all('span', attrs={'class':'icone-carro-info'}))>0):
                #print("tem")
                print(liItem.find('p').text.split())
            if (len(liItem.find_all('span', attrs={'class':'icone-SEGURANCA'}))>0):
                #print("tem")
                print(liItem.find('p').text.split())
            if (len(liItem.find_all('span', attrs={'class':'icone-CONFORTO'}))>0):
                #print("tem")
                print(liItem.find('p').text.split())
            if (len(liItem.find_all('span', attrs={'class':'icone-JANELAS'}))>0):
                #print("tem")
                print(liItem.find('p').text.split())


            print('------------')
            
    except Exception as e:
        raise e
    finally:
        if driver is not None:
            driver.quit()
        return anuncio

def main():
    
    anuncio_retornado = obter_detalhe_anuncio("ac28542875","https://www.icarros.com.br/comprar/sao-paulo-sp/chevrolet/onix/2019/d28510029")
    #print('Id: ', anuncio_retornado.id)
    #print('Url: ', anuncio_retornado.url)
    #print('Titulo: ', anuncio_retornado.titulo)
    #print('Preço: ', anuncio_retornado.preco)
    #print('Ano: ', anuncio_retornado.ano)
    #print('Km: ', anuncio_retornado.km)
    #print('Cor: ', anuncio_retornado.cor)
    #print('Cambio: ', anuncio_retornado.cambio)
    #print('Portas: ', anuncio_retornado.portas)

    anuncio_retornado.Salva_CSV('D:/teste.txt')
    #anuncio_retornado.Salva_CSV('D:/teste.txt')
    #anuncio_retornado.Salva_CSV('D:/teste.txt')
    #anuncio_retornado.Salva_CSV('D:/teste.txt')

if __name__ == '__main__':
    main()