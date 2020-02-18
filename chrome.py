from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import psutil
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

def check_unable(d):
    element = WebDriverWait(d, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
    if element.text.strip() == "401 Unauthorized! You aren't authorized to get this content.":
        return False
    else:
        return True

def close_driver(driver):
    try:
        if driver is not None:
            driver.quit()
        for process in psutil.process_iter():
            if process.name == 'chrome.exe':
                process.kill()
    except Exception as e:
        raise e

def get_random_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MACOS.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    return str(user_agent)

def get_driver():
    try:

        opts = Options()
        

        user_agent = get_random_user_agent()
        print('User agent utilizado: ' + user_agent)
        binary_path='d:/vendor/chromedriver_win32/chromedriver.exe'
        opts.add_argument("start-maximized")
        opts.add_argument("disable-infobars")
        opts.add_argument("--disable-extensions")
        opts.add_argument('--incognito')
        opts.add_argument('--disable-plugins-discovery')
        opts.add_argument('--no-proxy-server')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--lang=pt-BR')
        opts.add_argument(f'user-agent={user_agent}')      
        opts.add_experimental_option('useAutomationExtension', False) 
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(executable_path=binary_path,options=opts) 
        #driver.execute_cdp_cmd("Network.enable", {})
        #driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": user_agent}})
        #driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", { "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """ })        
        #c = driver.execute_script("return window.navigator.userLanguage || window.navigator.webdriver")
        #print('Navigator' + str(c))
        return driver
    except Exception as e:
        raise e


#url = 'https://www.icarros.com.br/principal/index.jsp?escopo=3&parceiro_id=86&midia_id=719&gclid=EAIaIQobChMI5ISe4YLc5wIVygeRCh1OhAL1EAAYASAAEgLpYfD_BwE'
#url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'
#url = 'http://www.google.com.br'
url = 'https://www.icarros.com.br'
driver = get_driver()
driver.get(url)


time.sleep(3)

#element = Select(driver.find_element_by_id('sltMake'))

#element.select_by_visible_text("Chevrolet")

#driver.find_element_by_id("sltMake").send_keys("Chevrolet");

element = driver.find_element_by_xpath('//*[@id="sltMake"]')
all_options = element.find_elements_by_tag_name("option")
for option in all_options:
    print("Value is: %s" % option.get_attribute("Chevrolet"))
    option.click()





WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sltMake"]')))



#print(check_unable(driver))


#try:
    #driver = get_driver()
    #driver.get(url)
#except Exception as e:
   #print(e)    



#close_driver(driver)


