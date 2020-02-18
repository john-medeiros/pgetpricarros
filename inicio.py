from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
import psutil



def get_driver():
    try:
        opts = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 0)
        profile.set_preference('intl.accept_languages', 'pt-BR')
        profile.set_preference('network.proxy.Kind','Direct')
        profile.update_preferences()
        driver = webdriver.Firefox(executable_path=r"C:/Users/F0127173/git/pric-mego/vendor/geckodriver-v0.26.0-win64/geckodriver.exe", options=opts, firefox_profile=profile)
    except Exception as e:
        raise e



url = 'https://www.icarros.com.br'
driver = get_driver()
driver.get(url)



 