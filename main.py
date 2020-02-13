from selenium import webdriver
import logging
import logging.handlers
from bs4 import BeautifulSoup

def init():
    logger = logging.getLogger()
    fh = logging.handlers.RotatingFileHandler('./app.log', maxBytes=10240, backupCount=5)
    fh.setLevel(logging.DEBUG)#no matter what level I set here
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logging.info("Log iniciado.")

def main():
    init()
    driver = webdriver.Chrome(executable_path="D:/Users/John.Medeiros/Downloads/chromedriver_win32/chromedriver.exe")
    url="https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&opcaocidade=1&foa=1&anunciosNovos=1&anunciosUsados=1&marca1=5&modelo1=2428&anomodeloinicial=2016&anomodelofinal=2021&precominimo=0&precomaximo=0&cidadeaberto=&escopo=2&locationSop=est_SP.1_-cid_9668.1_-esc_2.1_-rai_50.1_"
    driver.get(url)

    #element = browser.find.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[3]/div[3]/div[2]/div[5]/form/ul")
    dados = driver.find_element_by_class_name("listavertical")
    #print(type(dados))
    html = dados.get_attribute("innerHTML")
    soup = BeautifulSoup(html,lxml)

    for tag in soup.ul.find_all("li", recursive=True): 
        print(tag)
    

    
    driver.quit()


if __name__ == '__main__':
    main()