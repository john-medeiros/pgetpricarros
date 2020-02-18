import sys
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import logging.handlers
import datetime
import os.path
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import signal
from selenium.common.exceptions import TimeoutException

MIN_PYTHON = (3, 7)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

def init():
    logFileName='./'+os.path.basename(__file__).replace('.py', '.log')
    logger = logging.getLogger()
    #fh = logging.handlers.RotatingFileHandler('./app.log', maxBytes=102400, backupCount=5, encoding='utf-8')
    fh = logging.handlers.RotatingFileHandler(logFileName, encoding='utf-8')
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

class Anuncio:
    
    def __init__(self,id,url,titulo=None,preco=None,ano=None,km=None,cor=None,cambio=None,portas=None,acessorio=None,info_veiculo=None):
        self.__id = str(id)
        self.__url = str(url)
        self.__titulo = str(titulo)
        self.__preco = str(preco)
        self.__ano = str(ano)
        self.__km = str(km)
        self.__cor = str(cor)
        self.__cambio = str(cambio)
        self.__portas = str(portas)  
        self.__acessorio = str(acessorio)
        self.__info_veiculo = str(info_veiculo)
        self.__data_inicio =  datetime.datetime.now()
        self.__data_fim = None
        self.__valido = False
    
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
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, value):
        self.__titulo = str(value)

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, value):
        self.__preco = str(value)        

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, value):
        self.__ano = str(value)          

    @property
    def km(self):
        return self.__km

    @km.setter
    def km(self, value):
        self.__km = str(value)  

    @property
    def cor(self):
        return self.__cor

    @cor.setter
    def cor(self, value):
        self.__cor = str(value)   

    @property
    def cambio(self):
        return self.__cambio

    @cambio.setter
    def cambio(self, value):
        self.__cambio = str(value)

    @property
    def portas(self):
        return self.__portas

    @portas.setter
    def portas(self, value):
        self.__portas = str(value)

    @property
    def acessorio(self):
        return self.__acessorio

    @acessorio.setter
    def acessorio(self, value):
        self.__acessorio = str(value).replace(';','|||')

    @property
    def info_veiculo(self):
        return self.__info_veiculo

    @info_veiculo.setter
    def info_veiculo(self, value):
        self.__info_veiculo = str(value).replace(';','|||')

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
    def valido(self):
        return self.__valido

    @valido.setter
    def valido(self, value):
        self.__valido = value        

    def valida_conteudo_obtido(self):
        if self.titulo is None:
            logging.warning('Título do id: ' + str(self.id) + ' está vazio.')
        if self.preco is None:
            logging.warning('Preço do id: ' + str(self.preco) + ' está vazio.')
        if self.ano is None:
            logging.warning('Ano do id: ' + str(self.ano) + ' está vazio.')
        if self.km is None:
            logging.warning('Km do id: ' + str(self.km) + ' está vazio.')
        if self.cor is None:
            logging.warning('Cor do id: ' + str(self.cor) + ' está vazio.')
        if self.cambio is None:
            logging.warning('Cambio do id: ' + str(self.cambio) + ' está vazio.')
        if self.portas is None:
            logging.warning('Portas do id: ' + str(self.portas) + ' está vazio.')
        if self.acessorio is None:
            logging.warning('Acessorio do id: ' + str(self.acessorio) + ' está vazio.')                                                                        
        if self.info_veiculo is None:
            logging.warning('Informações de veículo do id: ' + str(self.info_veiculo) + ' está vazio.')   

        if ((self.titulo is None) or (self.preco is None) or (self.ano is None) or (self.km is None)):
            self.valido=False
        else:
            self.valido=True

    def Salva_CSV(self,filename):
        try:
            if not os.path.isfile(filename):
                Anuncio.Cria_Arquivo(filename)

            with open(filename, 'a', newline='\n', encoding='utf8') as f:
                writer = csv.writer(f,delimiter=';')
                writer.writerow([self.data_inicio, self.data_fim, self.id, self.titulo, self.preco, self.ano, self.km, self.cor, self.cambio, self.portas, self.url, self.acessorio, self.info_veiculo])      
            f.close()
        except Exception as e:
            logging.error('Erro ao salvar o arquivo: ' + filename)
            logging.exception(e)
            raise e

    def Obtem_Tempo_Processamento(self):
        if self.data_fim is None:
            return None
        else:
            duracao = self.data_fim - self.data_inicio
            return 'Id: ' + self.id + ' levou ' + str(duracao.total_seconds()) + ' segundos ou ' + str(int(duracao.total_seconds() * 1000)) + ' milissegundos para ser processado.'

    @staticmethod
    def Cria_Arquivo(filename):
            with open(filename, 'a', newline='\n', encoding='utf8') as f:
                writer = csv.writer(f)
                writer.writerow(['data_inicio; data_fim; id; titulo; preco; ano; km; cor; cambio; portas; url; acessorio; info_veiculo'])
            f.close()

def obter_detalhe_anuncio(id,url,p):
    try:
        anuncio = Anuncio(id,url)
        logging.info('Id: ' + id + ' url: ' + url)
        p.get(url)

        titulo = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctdoTopo"]/h1')))
        #titulo = p.find_element_by_xpath('//*[@id="ctdoTopo"]/h1')
        if titulo is not None:
            anuncio.titulo=titulo.text  
        preco = p.find_element_by_xpath('//*[@id="cardProposta"]/div/h2')
        if preco is not None:
            anuncio.preco=preco.text

        if (leitura_bloqueada(p)):
            logging.info('Leitura bloqueada pelo site.')
            anuncio.valido = False
            return anuncio

        element = p.find_element_by_xpath('/html/body/div/div[1]/div/div[5]/div[1]/div[2]/div')
        html = element.get_attribute('innerHTML')
        sub_html = BeautifulSoup(html,'html.parser') 
        ul = sub_html.find('ul')
        li = ul.find_all('li')

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

        element = p.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div[1]')    
        html = element.get_attribute('innerHTML') 
        sub_html = BeautifulSoup(html,'html.parser')   
        ul = sub_html.find('ul')
        li = ul.find_all('li')

        for liItem in li:
            
            if (len(liItem.find_all('span', attrs={'class':'icone-carro-info'}))>0):
                if not anuncio.acessorio:
                    anuncio.acessorio=''
                else:
                    anuncio.acessorio+=','
                anuncio.acessorio+=liItem.find('p').text.replace('\n', ' ').replace('\r', '').replace('  ','')
                continue
            if (len(liItem.find_all('span', attrs={'class':'icone-SEGURANCA'}))>0):
                if not anuncio.acessorio:
                    anuncio.acessorio=''
                else:
                    anuncio.acessorio+=','
                anuncio.acessorio+=' '+liItem.find('p').text.replace('\n', ' ').replace('\r', '').replace('  ','')
                continue
            if (len(liItem.find_all('span', attrs={'class':'icone-CONFORTO'}))>0):
                if not anuncio.acessorio:
                    anuncio.acessorio=''
                else:
                    anuncio.acessorio+=','
                anuncio.acessorio+=' '+liItem.find('p').text.replace('\n', ' ').replace('\r', '').replace('  ','')
                continue
            if (len(liItem.find_all('span', attrs={'class':'icone-JANELAS'}))>0):
                if not anuncio.acessorio:
                    anuncio.acessorio=''
                else:
                    anuncio.acessorio+=','
                anuncio.acessorio+=' '+liItem.find('p').text.replace('\n', ' ').replace('\r', '').replace('  ','')
                continue
            if (liItem.find('strong') and (liItem.find('strong').text=='Informações do veículo:')):
                anuncio.info_veiculo+=' '+liItem.find('p').text.replace('\n', ' ').replace('\r', '').replace('  ','')
                continue

        anuncio.data_fim=datetime.datetime.now()

    except TimeoutException as e:
        logging.error('Erro de timeout ao obter dados do anúncio: ' + str(id) + ' com a url: ' + str(url))
        anuncio.valido = False
        #logging.exception(e)
    except Exception as e:
        #print(e)
        logging.error('Ocorreu um erro ao processar o Id: ' + id)
        logging.exception(e)
        raise
    finally:
        #logging.info(anuncio.Obtem_Tempo_Processamento())
        return anuncio

def leitura_bloqueada(d):
    element = d.find_element_by_xpath('/html/body')
    if (element.text.strip() == "401 Unauthorized! You aren't authorized to get this content."):
        return True
    else:
        return False

def main():
    try:
        init()
        opts = Options()
        #opts.headless = True
        driver = webdriver.Firefox(executable_path=r"C:/Users/F0127173/git/pric-mego/vendor/geckodriver-v0.26.0-win64/geckodriver.exe", options=opts)
        with open ('d:/anuncio_resumido_ford_ka.txt') as csvFile:
            reader = csv.reader(csvFile, delimiter=';')
            next(reader,None)
            for row in reader:
                anuncio_retornado = obter_detalhe_anuncio(row[3],row[4],driver)
                anuncio_retornado.valida_conteudo_obtido()
                print('')
                if anuncio_retornado.valido == True:
                    anuncio_retornado.Salva_CSV("d:/teste_ford_ka.txt")
                else:
                    logging.warning('Anúncio inacessível. id: ' + str(row[3]) + ' com a url: ' + str(row[4]))
    except Exception as e:
        logging.error('Ocorreu um erro ao processar o Id: ' + str(id))
        logging.exception(e)
        raise e
    finally:
        if driver is not None:
            driver.quit()
        logging.info('Processamento finalizado.')

if __name__ == '__main__':
    main()