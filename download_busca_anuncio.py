import sys
import getopt
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import logging
import logging.handlers
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import csv
from bs4 import BeautifulSoup
from bs4.element import Tag
import random
import time 
import psutil

MIN_PYTHON = (3, 7)

if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

class Busca:

    def __init__(self,marca_id,marca,modelo_id,modelo,arquivo):
        self.__marca_id = str(marca_id)
        self.__marca = str(marca)
        self.__modelo_id = str(modelo_id)    
        self.__modelo =  str(modelo)
        self.__arquivo =  str(arquivo)

    @property
    def marca_id(self):
        return self.__marca_id

    @marca_id.setter
    def marca_id(self, value):
        self.__marca_id = str(value)

    @property
    def marca(self):
        return self.__marca

    @marca.setter
    def marca(self, value):
        self.__marca = str(value)

    @property
    def modelo_id(self):
        return self.__modelo_id

    @modelo_id.setter
    def modelo_id(self, value):
        self.__modelo_id = str(value)        

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, value):
        self.__modelo = str(value)

    @property
    def arquivo(self):
        return self.__arquivo

    @arquivo.setter
    def arquivo(self, value):
        self.__arquivo = str(value)

    def url(self):
        try:
            url='https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&anunciosUsados=1&marca1='+self.marca_id+'&modelo1='+self.modelo_id+'&anomodeloinicial=2016&anomodelofinal=2021&precominimo=0&precomaximo=0&cidadeaberto=&escopo=2&locationSop=est_SP.1_-cid_9668.1_-esc_2.1_-rai_50.1_'
            return url
        except Exception as e:
            logging.error('Erro ao criar a url de busca')
            logging.exception(e)
            raise e  

class AnuncioResumido:

    def __init__(self,id=None,url=None,pagina=None):
        self.__pagina = str(pagina)
        self.__id = str(id)
        self.__url = str(url)    
        self.__data_inicio =  datetime.now()
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

def init():
    # É executada no começo do programa
    logger = logging.getLogger()
    fh = logging.handlers.RotatingFileHandler('./download_busca_anuncio.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)#no matter what level I set here
    #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(funcName)s() - %(message)s')
    fh.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logging.info('Início do processamento com PID: ' + str(os.getpid()))

def get_data_to_scrap(filename):
    # Retorna um data frame com o conteúdo de um arquivo de parâmetros informados.
    try:
        data = pandas.read_csv(filename, delimiter=';',encoding = 'utf8')
        return data
    except Exception as e:
        logging.error('Ocorreu um erro ao ler o arquivo de origem para o processamento.')
        logging.exception(e)
        raise e

def get_random_user_agent():
    # Retorna um user agent para ser usado ao criar uma sessão de navegação com o objetivo de evitar a detecção da automação.
    try:
        software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MACOS.value, OperatingSystem.FREEBSD.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1000)
        #user_agents = user_agent_rotator.get_user_agents()
        user_agent = user_agent_rotator.get_random_user_agent()
        return str(user_agent)        
    except Exception as e:
        logging.error('Ocorreu um erro ao gerar um User Agent para navegação.')
        logging.exception(e)        
        raise e

def close_driver(driver):
    # Fecha o driver e finaliza os processos do browser no sistema operacional
    try:
        if driver is not None:
            driver.quit()
        for process in psutil.process_iter():
            if process.name == 'chrome.exe':
                process.kill()
    except Exception as e:
        logging.error('Erro ao finalizar o driver.')
        logging.exception(e)
        raise e

def check_blocked_search(element):
    # Valida se a busca foi bloqueada no site de origem
    try:
        rv=False
        html = element.get_attribute("outerHTML")
        sub_html = BeautifulSoup(html,'html.parser') 
        body_html = sub_html.find('body')
        if isinstance(body_html, Tag):
            if body_html.text.strip() == "401 Unauthorized! You aren't authorized to get this content.":
                rv=True
            else:
                rv=False
    except Exception as e:
        logging.error('Erro ao validar se a busca foi bloqueada na origem.')
        logging.exception(e)
    finally:
        return rv

def get_driver():
    # Retorna um driver que será utilizado para fazer as buscas.
    try:
        opts = Options()
        user_agent = get_random_user_agent()
        logging.info('User agent utilizado: ' + user_agent)
        binary_path='./common/chromedriver.exe'
        #opts.add_argument("start-maximized")
        #opts.add_argument("disable-infobars")
        opts.add_argument("--headless")
        opts.add_argument("--disable-extensions")
        opts.add_argument('--incognito')
        opts.add_argument('--disable-plugins-discovery')
        opts.add_argument('--no-proxy-server')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--lang=pt-BR')
        opts.add_argument(f'user-agent={user_agent}')      
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_experimental_option('useAutomationExtension', False) 
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(executable_path=binary_path,options=opts) 
        return driver
    except Exception as e:
        logging.error('Ocorreu um erro ao criar um driver para navegação.')
        logging.exception(e)        
        raise e

def get_current_page(p):
    # Retorna o número da página atual
    try:
        pagina = None
        element = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudoLista"]/div[3]/div[2]/div[4]/div[2]')))

        if check_blocked_search(element):
            logging.warning('Leitura bloqueada na origem possívelmente por detecção da automação.')
            logging.warning('A execução será finalizada.')
            close_driver(p)
            raise SystemExit

        html = element.get_attribute('innerHTML')
        sub_html = BeautifulSoup(html,'html.parser') 
        ul = sub_html.find('ul')
        liPaginaAtual = ul.find('li',{'class': 'selected'})
        if liPaginaAtual is None:
            pagina = str('1')
            logging.info('Esta busca retornou apenas 1 página com resultados.')
        else:
            pagina = liPaginaAtual.text.strip()
    except TimeoutException as e:
        logging.error('Erro de timeout ao obter a página atual.')
    except Exception as e:
        logging.error('Ocorreu um erro ao obter a página atual.')
        logging.exception(e)
        raise
    finally:
        return pagina  

def get_advertisements(p):
    # Retorna a lista de anuncios encontrados na busca
    try:
        listaAnunciosResumida = []
        element = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*')))

        if check_blocked_search(element):
            logging.warning('Leitura bloqueada na origem possívelmente por detecção da automação.')
            logging.warning('A execução será finalizada.')
            close_driver(p)
            raise SystemExit

        html = element.get_attribute("outerHTML")
        soup = BeautifulSoup(html,'html.parser') 

        pagina_atual = get_current_page(p)

        for formTag in soup.find_all('form', {'id' : 'anunciosForm'}):
            for ul in formTag.find_all('ul', {'class': 'listavertical'}):
                for litag in ul.find_all('li'):
                    id = litag.get("id")
                    if id is not None:
                        aTag=litag.find('a')
                        url = 'https://www.icarros.com.br' + aTag.get("href")
                        anuncioResumido = AnuncioResumido(id,url,pagina_atual)
                        anuncioResumido.data_fim = datetime.now()
                        listaAnunciosResumida.append(anuncioResumido)
    except Exception as e:
        logging.error('Ocorreu um erro ao obter a lista de anúncios.')
        logging.exception(e)
        raise
    finally:
        return listaAnunciosResumida 

def get_next_page(p):
    # Retorna a url referente à próxima página
    try:
        url = None
        element = WebDriverWait(p, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudoLista"]/div[3]/div[2]/div[4]/div[2]')))

        if check_blocked_search(element):
            logging.warning('Leitura bloqueada na origem possívelmente por detecção da automação.')
            logging.warning('A execução será finalizada.')
            close_driver(p)
            raise SystemExit

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

def process(busca):
    # Função principal: executa a busca
    try:
        row_count=0
        has_pages = True
        logging.info('Iniciando busca: marca_id=' + busca.marca_id + ' marca='+ busca.marca + ' modelo_id=' + busca.modelo_id + ' modelo=' + busca.modelo)
        url = busca.url()
        logging.info("Url de busca: "+ url)
        driver = get_driver()

        while has_pages:
            intervalBetweenSearch=random.randint(3,12)
            logging.info('Utilizando um intervalo de ' + str(intervalBetweenSearch) + ' segundos na paginação de resultados.')
            time.sleep(intervalBetweenSearch)            
            driver.get(url)
            anunciosResumidos = get_advertisements(driver)
            row_count += len(anunciosResumidos)
            logging.info('Quantidade de anúncios obtidos: ' + str(row_count))
            for anuncio in anunciosResumidos:
                anuncio.Salva_CSV(busca.arquivo)

            url_next_page=get_next_page(driver)
            if url_next_page:
                has_pages = True
                url = url_next_page
                logging.info('Próxima url: ' + str(url_next_page))
            else:
                has_pages = False
                logging.info('Todas as páginas foram processadas para esta busca.')
                break
    except Exception as e:
        logging.error('Ocorreu um erro ao obter a próxima página.')
        logging.exception(e)        
        raise e
    finally:
        if driver is not None:
            close_driver(driver)
        logging.info('Esta busca retornou ' + str(row_count) + ' resultados.')
        return row_count

def main():
    try:
        init()
        input_file='d:/lista_carros_pesquisa.csv'
        logging.info('Lendo arquivo: ' + input_file)
        output_file='d:/output_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.txt'
        logging.info('Gravando arquivo: ' + output_file)
        data_to_scrap = get_data_to_scrap(input_file)
        qtBuscas=len(data_to_scrap.index)
        logging.info('Foram encontradas ' + str(qtBuscas) + ' buscas para serem realizadas.')
        row_count=0

        for index, row in data_to_scrap.iterrows():
            busca = Busca(row['marca_id'],row['marca'],row['modelo_id'],row['modelo'],output_file)
            rows_processed=process(busca)
            row_count+=rows_processed
            intervalBetweenSearch=random.randint(1,20)
            time.sleep(intervalBetweenSearch)
            logging.info('Subtotal de anúncios obtidos: '+ str(row_count))
            logging.info('Intervalo em segundos até uma nova busca: ' + str(intervalBetweenSearch))

        logging.info('Total de anúncios obtidos: '+ str(row_count))

    except Exception as e:
        logging.exception(e)        
        raise e
    finally:
        logging.info('Fim do processamento')

if __name__ == '__main__':
    main()