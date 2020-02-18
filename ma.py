import sys
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import logging
import logging.handlers
import datetime
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import signal
from selenium.common.exceptions import TimeoutException

def init():
    logger = logging.getLogger()
    fh = logging.handlers.RotatingFileHandler('./main_app.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)#no matter what level I set here
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logging.info('PID: ' + str(os.getpid()))

class AnuncioResumido:

    def __init__(self,id=None,url=None,pagina=None):
        self.__pagina = str(pagina)
        self.__id = str(id)
        self.__url = str(url)    
        self.__data_inicio =  datetime.datetime.now()
        self.__data_fim = None         

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

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, value):
        self.__data_inicio = value

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, value):
        self.__data_fim = value

    @property
    def pagina(self):
        return self.__pagina

    @pagina.setter
    def pagina(self, value):
        self.__pagina = value        

    def Salva_CSV(self,filename):
        try:
            if not os.path.isfile(filename):
                AnuncioResumido.Cria_Arquivo(filename)

            with open(filename, 'a', newline='\n', encoding='utf8') as f:
                writer = csv.writer(f,delimiter=';')
                writer.writerow([self.data_inicio, self.data_fim, self.pagina, self.id, self.url])      
            f.close()
        except Exception as e:
            logging.error('Erro ao salvar o arquivo: ' + filename)
            logging.exception(e)
            raise e          

    @staticmethod
    def Cria_Arquivo(filename):
            with open(filename, 'w', newline='\n', encoding='utf8') as f:
                writer = csv.writer(f)
                writer.writerow(['data_inicio; data_fim; pagina; id; url'])
            f.close()

def obter_proxima_pagina(p):
    try:
        url = None
        element = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudoLista"]/div[3]/div[2]/div[4]/div[2]')))
        #element = p.find_element_by_xpath('//*[@id="conteudoLista"]/div[3]/div[2]/div[4]/div[2]')
        html = element.get_attribute('innerHTML')
        sub_html = BeautifulSoup(html,'html.parser') 
        url = None
        ul = sub_html.find('ul')
        liProximaPagina = ul.find('li',{'class': 'proxima'})
        if liProximaPagina:
            url = 'https://www.icarros.com.br' + str(liProximaPagina.a.get('href'))
    except TimeoutException as e:
        logging.error('Erro de timeout ao obter a próxima página.')
    except Exception as e:
        logging.error('Ocorreu um erro ao obter a próxima página.')
        logging.exception(e)
        raise
    finally:
        return url

def obter_pagina_atual(p):
    try:
        pagina = None
        element = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudoLista"]/div[3]/div[2]/div[4]/div[2]')))
        #element = p.find_element_by_xpath('//*[@id="conteudoLista"]/div[3]/div[2]/div[4]/div[2]')
        html = element.get_attribute('innerHTML')
        sub_html = BeautifulSoup(html,'html.parser') 
        ul = sub_html.find('ul')
        liPaginaAtual = ul.find('li',{'class': 'selected'})
        pagina = liPaginaAtual.text.strip()
    except TimeoutException as e:
        logging.error('Erro de timeout ao obter a página atual.')
    except Exception as e:
        logging.error('Ocorreu um erro ao obter a página atual.')
        logging.exception(e)
        raise
    finally:
        return pagina  

def obter_lista_anuncios(p):
    try:
        listaAnunciosResumida = []
        element = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*')))
        #element = p.find_element_by_xpath("//*")
        html = element.get_attribute("outerHTML")
        soup = BeautifulSoup(html,'html.parser') 

        pagina_atual = obter_pagina_atual(p)

        for formTag in soup.find_all('form', {'id' : 'anunciosForm'}):
            for ul in formTag.find_all('ul', {'class': 'listavertical'}):
                for litag in ul.find_all('li'):
                    id = litag.get("id")
                    if id is not None:
                        aTag=litag.find('a')
                        url = 'https://www.icarros.com.br' + aTag.get("href")
                        anuncioResumido = AnuncioResumido(id,url,pagina_atual)
                        anuncioResumido.data_fim = datetime.datetime.now()
                        listaAnunciosResumida.append(anuncioResumido)
    except Exception as e:
        logging.error('Ocorreu um erro ao obter a lista de anúncios.')
        logging.exception(e)
        raise
    finally:
        return listaAnunciosResumida    

def processar_pagina(p):
    anunciosResumidos = obter_lista_anuncios(p)
    for anuncio in anunciosResumidos:
        anuncio.Salva_CSV('d:/anuncio_resumido_ford_ka.txt')
    logging.info('Quantidade de anúncios obtidos: ' + str(len(anunciosResumidos)))
    pass

def main():
    try:
        init()
        url_busca = 'https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&anunciosUsados=1&marca1=15&modelo1=287&anomodeloinicial=2016&anomodelofinal=2021&precominimo=0&precomaximo=0&cidadeaberto=&escopo=2&locationSop=est_SP.1_-cid_9668.1_-esc_2.1_-rai_50.1_'
        #url_busca='https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&anunciosUsados=1&marca1=5&modelo1=2317&anomodeloinicial=2016&anomodelofinal=2021&precominimo=0&precomaximo=0&cidadeaberto=&escopo=2&locationSop=est_SP.1_-cid_9668.1_-esc_2.1_-rai_50.1_'
        logging.info('url inicial: ' + str(url_busca))

        opts = Options()
        opts.headless = True
        #opts.headless = True
        driver = webdriver.Firefox(executable_path=r"C:/Users/F0127173/git/pric-mego/vendor/geckodriver-v0.26.0-win64/geckodriver.exe", options=opts)

        while url_busca:
            logging.info('Atual url: ' + str(url_busca))
            driver.get(url_busca)
            processar_pagina(driver)
            url_proxima_pagina = obter_proxima_pagina(driver)
            if url_proxima_pagina:
                logging.info('Próxima url: ' + str(url_proxima_pagina))
            else:
                logging.info('Todas as páginas foram processadas para esta busca.')
                break
            url_busca = url_proxima_pagina
    except Exception as e:
        #print(e)
        logging.error('Ocorreu um erro ao processar listas de anúncios. url: ' + str(url_busca))
        logging.exception(e)
        raise
    finally:
        #if driver is not None:
            #driver.quit()        
        logging.info('Processamento finalizado.')

if __name__ == '__main__':
    main()    