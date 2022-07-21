from re import X
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os,json
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()

opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
#opts.add_argument("window-size=200,100")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
prefs = {"profile.default_content_setting_values.notifications" : 2}
opts.add_experimental_option("prefs",prefs)
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
 

def xpath_type_enter(el,mount):
    wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_type(el,mount):
    el_get = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    el_get.send_keys(Keys.CONTROL, 'a')
    sleep(0.5)
    el_get.send_keys(Keys.BACKSPACE)
    sleep(0.5)
    wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)
 
def job(notifer):
    blacklist = ["ap-southeast-3","me-south-1","ap-east-1","eu-south-1"]
    script = "script.txt"
    script = open(f"{cwd}/{script}","r")
    script = script.read()
    urls_list = []
    browser.get('https://us-east-1.console.aws.amazon.com/gluestudio/home?region=us-east-1#/jobs')
    xpath_el('//button[@aria-controls="menu--regions"]')
    get_url_country = wait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href,"onsole.aws.amazon.com/gluestudio/home?region=")]')))
    for country in get_url_country:
        urls_list.append(country.get_attribute('href'))
 
    for url in urls_list:
        get_code_country = url.split(".console")[0].replace("https://","")
        
        if any(f'{get_code_country}' in s for s in blacklist): 
            pass
        else:
            for repeat in range(0,totalrepeat):
                browser.get(url)
                xpath_el('//label[@data-value="code_editor"]')
                xpath_el('//button[@id="glue__job-create-btn"]')
            
                script_el = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="ace_text-input"]')))
                script_el.send_keys(Keys.CONTROL, 'a')
                script_el.send_keys(Keys.BACKSPACE)
                for part in script.split('\n'):
                    script_el.send_keys(part)
                    sleep(0.5)
                    ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                    sleep(0.2)
                
                xpath_el('//a[@data-testid="details"]')
                sleep(0.2)
                xpath_type('(//input[@class="awsui-input awsui-input-type-text awsui-input-valid"])[1]',email+str(random.randint(10000,100000)))
                sleep(0.2)
                role = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '(//awsui-select-trigger)[1]')))
                role.click()
                sleep(0.2)
                browser.execute_script("arguments[0].scrollIntoView();", role)
                wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '(//li[@class="awsui-select-dropdown-option awsui-select-dropdown-option-selectable"])[1]'))).click()
                
                sleep(0.2)
                wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-value="G.1X"]'))).click()
                sleep(0.2)
                wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-value="G.2X"]'))).click()
                sleep(0.2)
                xpath_type('(//input[contains(@id,"number-input")])[3]',1000000)
                sleep(0.2)
                xpath_el('(//button[@class="awsui-button awsui-button-variant-normal awsui-hover-child-icons"])[1]')
                sleep(1)
                assertion1 = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="awsui-flash-header"]'))).text
                print(f"[{time.strftime('%d-%m-%y %X')}] {get_code_country} | {assertion1}!")
                sleep(1)
                xpath_el('//button[@class="awsui-button awsui-button-variant-primary awsui-hover-child-icons"]')
                sleep(1)
                assertion2 = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="awsui-flash-header"]'))).text 
                print(f"[{time.strftime('%d-%m-%y %X')}] {get_code_country} | {assertion2}!")
             
def open_browser(k):
    
    global browser
    global element
    global email
    global password
    k = k.split("|")
    url_access = k[0]
    email = k[1]
    password = k[2]
 
    #opts.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc)
    browser.get(url_access)
    # xpath_el('//input[@id="iam_user_radio_button"]')
    # print(f"[{time.strftime('%d-%m-%y %X')}] Trying to Login {email}")
    # sleep(0.5)
    # xpath_type_enter('//input[@id="resolving_input"]',access_key)
    # sleep(0.5)
    # xpath_type_enter('//input[@id="resolving_input"]',Keys.ENTER)
    # sleep(0.5)
    # xpath_type('//input[@id="account"]',access_key)
    # sleep(0.5)
    xpath_type_enter('//input[@id="username"]',email)
    sleep(0.5)
    xpath_type_enter('//input[@id="password"]',password)
    sleep(0.5)
    xpath_type_enter('//input[@id="password"]',Keys.ENTER)
    sleep(0.5)
    try:
        notifer = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Open account menu"]'))).text
        
        print(f"[{time.strftime('%d-%m-%y %X')}] Hello {notifer}!")
        print(f"[{time.strftime('%d-%m-%y %X')}] Trying to doing the Job!")
        job(notifer)
    except Exception as e:
        print(f"[{time.strftime('%d-%m-%y %X')}] Something Error {e}")
        
if __name__ == '__main__':
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation JOB AWS")
    data = input(f"[{time.strftime('%d-%m-%y %X')}] Input AccessID|username|password: ")
    totalrepeat = int(input(f"[{time.strftime('%d-%m-%y %X')}] Input Limit JOB: "))
    open_browser(data)
